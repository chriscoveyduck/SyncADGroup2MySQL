import pytest
from sync_ad_group import get_ad_group_members, get_db_members

def test_get_ad_group_members():
    # Should return a set
    members = get_ad_group_members()
    assert isinstance(members, set)

def test_get_db_members():
    # Should return a set (mock DB connection)
    class DummyCursor:
        pass
    members = get_db_members(DummyCursor())
    assert isinstance(members, set)
