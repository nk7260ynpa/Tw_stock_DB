import os
import shutil
import pytest
import tempfile

from sqlalchemy import create_engine

from build_DB.base import BuildEmptyDB, BaseBuildTABLE

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

    def test_build_pass(self, build_db, mocker):
        mocker_conn_server = mocker.Mock()
        mocker_conn_server.execute.return_value = None
        mocker_conn_server.commit.return_value = None
        mocker_conn_server.close.return_value = None

        mocker.patch.object(build_db, 'check_db_exists', return_value=False)
        build_db.build(mocker_conn_server)

    def test_build_fail(self, build_db, mocker):
        mocker_conn_server = mocker.Mock()
        mocker_conn_server.execute.return_value = None
        mocker_conn_server.commit.return_value = None
        mocker_conn_server.close.return_value = None

        mocker.patch.object(build_db, 'check_db_exists', return_value=True)
        build_db.build(mocker_conn_server)
        
class BuildTEMPTABLETemp(BaseBuildTABLE):
    def post_process(self, conn):
        """
        No post-processing steps are defined in this class.
        """
        pass

@pytest.fixture
def build_temp_table():
    temp_file_path = "build_DB/TEMP_sql/temp.sql"
    # Ensure the directory exists before creating the file
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)
    
    # Create and write to the file
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write("CREATE TABLE IF NOT EXISTS `TEMP` (id INT PRIMARY KEY, name VARCHAR(50))")
    build_obj = BuildTEMPTABLETemp()

    # Remove the build_DB/TEMP_sql directory and its contents if it exists
    temp_dir_path = "build_DB/TEMP_sql"
    if os.path.exists(temp_dir_path):
        shutil.rmtree(temp_dir_path)
    return build_obj

class TestBaseBuildTABLE:
    def test_read_sql_file(self, build_temp_table):
        sql = build_temp_table.sql
        assert "CREATE TABLE IF NOT EXISTS `TEMP` (id INT PRIMARY KEY, name VARCHAR(50))" == sql

    def test_check_table_exists(self, build_temp_table, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()
        
        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchone.return_value = [1]
        mock_conn.execute.return_value = mock_results
        
        # Use the mocked connection to test check_table_exists
        exists = build_temp_table.check_table_exists(mock_conn)
        
        # Assert that the table exists
        assert exists is True

    def test_check_table_not_exists(self, build_temp_table, mocker):
        # Mock the connection object
        mock_conn = mocker.Mock()
        
        # Mock the execute method to return a mock result
        mock_results = mocker.Mock()
        mock_results.fetchone.return_value = [0]
        mock_conn.execute.return_value = mock_results
        
        # Use the mocked connection to test check_table_exists
        exists = build_temp_table.check_table_exists(mock_conn)
        
        # Assert that the table does not exist
        assert exists is False

    def test_build_pass(self, build_temp_table, mocker):
        mocker_conn_server = mocker.Mock()
        mocker_conn_server.execute.return_value = None
        mocker_conn_server.commit.return_value = None
        mocker_conn_server.close.return_value = None

        mocker.patch.object(build_temp_table, 'check_table_exists', return_value=False)
        build_temp_table.build(mocker_conn_server)
    
    def test_build_fail(self, build_temp_table, mocker):
        mocker_conn_server = mocker.Mock()
        mocker_conn_server.execute.return_value = None
        mocker_conn_server.commit.return_value = None
        mocker_conn_server.close.return_value = None

        mocker.patch.object(build_temp_table, 'check_table_exists', return_value=True)
        build_temp_table.build(mocker_conn_server)
