# SyncADGroup2MySQL

This project synchronizes the membership of the Active Directory group `SmtpEnabledUsers` with an Azure MySQL database table. It is designed to support a PostFix Submission service for SMTP 'Send As' permissions.

## Features
- Scheduled synchronization (configurable interval)
- Detects and applies changes (additions/removals) from AD to MySQL
- One-way sync: AD → MySQL
- All DB operations via stored procedures (SPOCs)
- Containerized with Docker
- Kubernetes deployment and secrets YAMLs
- Test automation with pytest

## Project Structure
- `sync_ad_group.py`: Main Python script
- `mysql_schema.sql`: MySQL table schema
- `tests/`: Pytest test cases
- `Dockerfile`: Containerization
- `deployment.yaml`, `secrets.yaml`: Kubernetes manifests

## MySQL Table Schema
See `mysql_schema.sql` for the table definition.

## Configuration
All configuration is via environment variables (see `secrets.yaml` for required values):
- `AD_SERVER`, `AD_USER`, `AD_PASSWORD`, `AD_GROUP`
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DB`
- `SYNC_INTERVAL_MINUTES`

## Running Locally
1. Install dependencies:
   ```bash
   pip install ldap3 mysql-connector-python pytest
   ```
2. Set environment variables (see above).
3. Run the script:
   ```bash
   python sync_ad_group.py
   ```

## Running Tests
```bash
pytest
```

## Docker Usage
Build and run the container:
```bash
docker build -t syncadgroup2mysql .
docker run --env-file .env syncadgroup2mysql
```

## Kubernetes Deployment
1. Update secrets in `secrets.yaml` (base64-encode values).
2. Deploy secrets and app:
   ```bash
   kubectl apply -f secrets.yaml
   kubectl apply -f deployment.yaml
   ```

## Notes
- The script expects stored procedures for add/remove operations in MySQL.
- AD and MySQL credentials must be securely managed.
- For production, ensure proper error handling and logging.