import os
import time
import logging
import mysql.connector
from ldap3 import Server, Connection, ALL
from typing import List, Set

# Configuration (to be replaced with env vars or secrets in production)
AD_SERVER = os.getenv('AD_SERVER')
AD_USER = os.getenv('AD_USER')
AD_PASSWORD = os.getenv('AD_PASSWORD')
AD_GROUP = os.getenv('AD_GROUP', 'SmtpEnabledUsers')
AD_DOMAIN_FQDN = os.getenv('AD_DOMAIN_FQDN')  # e.g., 'your.domain.com'
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

logging.basicConfig(level=logging.INFO)

def get_ad_group_members() -> Set[str]:
    """
    Connect to AD and fetch group members. Returns a set of (ad_user_id, email) tuples.
    """
    server = Server(AD_SERVER, get_info=ALL)
    conn = Connection(server, user=AD_USER, password=AD_PASSWORD, auto_bind=True)
    # Convert FQDN to base DN (e.g., 'your.domain.com' -> 'dc=your,dc=domain,dc=com')
    if not AD_DOMAIN_FQDN:
        raise ValueError('AD_DOMAIN_FQDN environment variable must be set')
    search_base = ','.join([f'dc={part}' for part in AD_DOMAIN_FQDN.split('.')])
    # Search for the group
    conn.search(
        search_base=search_base,
        search_filter=f'(&(objectClass=group)(cn={AD_GROUP}))',
        attributes=['member']
    )
    if not conn.entries:
        logging.warning(f'Group {AD_GROUP} not found in AD.')
        return set()
    members_dns = conn.entries[0]['member'].values
    members = set()
    for dn in members_dns:
        conn.search(
            search_base=dn,
            search_filter='(objectClass=user)',
            attributes=['sAMAccountName', 'mail']
        )
        if conn.entries:
            user = conn.entries[0]
            ad_user_id = str(user['sAMAccountName'])
            email = str(user['mail']) if 'mail' in user else ''
            if ad_user_id and email:
                members.add((ad_user_id, email))
    conn.unbind()
    return members


def get_db_members(cursor) -> Set[str]:
    """
    Fetch current members from MySQL using a SELECT query. Returns a set of (ad_user_id, email) tuples.
    """
    cursor.execute("SELECT ad_user_id, email FROM smtp_enabled_users")
    rows = cursor.fetchall()
    return set((row[0], row[1]) for row in rows)


def spoc_add_user(cursor, ad_user_id, email):
    """
    Call stored procedure to add user.
    """
    cursor.callproc('sp_add_smtp_enabled_user', [ad_user_id, email])


def spoc_remove_user(cursor, ad_user_id):
    """
    Call stored procedure to remove user.
    """
    cursor.callproc('sp_remove_smtp_enabled_user', [ad_user_id])


def sync():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    cursor = conn.cursor()
    ad_members = get_ad_group_members()  # Set of (ad_user_id, email)
    db_members = get_db_members(cursor)  # Set of (ad_user_id, email)
    ad_user_ids = set(x[0] for x in ad_members)
    db_user_ids = set(x[0] for x in db_members)
    to_add_ids = ad_user_ids - db_user_ids
    to_remove_ids = db_user_ids - ad_user_ids
    ad_members_dict = {x[0]: x[1] for x in ad_members}
    for ad_user_id in to_add_ids:
        spoc_add_user(cursor, ad_user_id, ad_members_dict[ad_user_id])
    for ad_user_id in to_remove_ids:
        spoc_remove_user(cursor, ad_user_id)
    conn.commit()
    cursor.close()
    conn.close()

def main():
    sync_interval = int(os.getenv('SYNC_INTERVAL_MINUTES', '60'))
    while True:
        logging.info('Starting sync...')
        sync()
        logging.info(f'Sleeping for {sync_interval} minutes...')
        time.sleep(sync_interval * 60)  # Sleep for N minutes

if __name__ == '__main__':
    main()
