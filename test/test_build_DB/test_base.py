import pytest
import tempfile

from sqlalchemy import create_engine

from build_DB.base import BuildEmptyDB

@pytest.fixture
def build_db():
    # Create a temporary file with the desired content
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write("CREATE DATABASE IF NOT EXISTS `BASE`")
        temp_file_path = temp_file.name
    return BuildEmptyDB(temp_file_path)

class TestBuildEmptyDB:

    def test_read_sql_file(self, build_db):
        sql = build_db.read_sql_file()
        assert "CREATE DATABASE IF NOT EXISTS `BASE`" == sql

    def test_get_db_name(self, build_db):
        db_name = build_db.get_db_name()
        assert db_name == "BASE"


    def test_check_db_exists(self, build_db, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()
        
        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchall.return_value = [["BASE"]]
        mock_conn.execute.return_value = mock_results
        
        # Use the mocked connection to test check_db_exists
        exists = build_db.check_db_exists(mock_conn)
        
        # Assert that the database exists
        assert exists is True

    def test_check_db_not_exists(self, build_db, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()
        
        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchall.return_value = []
        mock_conn.execute.return_value = mock_results
        
        # Use the mocked connection to test check_db_exists
        exists = build_db.check_db_exists(mock_conn)
        
        # Assert that the database does not exist
        assert exists is False

