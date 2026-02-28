import os
import shutil
import pytest

from build_DB.base import BaseBuildTABLE
from build_DB.news import (BuildNEWS, BuildNEWSTABLE, BuildNEWSTABLECTEE,
                            BuildNEWSTABLECNYES, BuildNEWSTABLECNYESUploaded,
                            BuildNEWSTABLEPTT, BuildNEWSTABLEPTTUploaded,
                            BuildNEWSTABLEMoneyUDN,
                            BuildNEWSTABLEMoneyUDNUploaded)


class TestBuildNEWS:
    """測試 BuildNEWS 資料庫建構類別。"""

    def test_name(self):
        """BuildNEWS 的名稱應為 'NEWS'。"""
        build_news = BuildNEWS()
        assert build_news.name == "NEWS"

    def test_typeclass(self):
        """BuildNEWS 的 typeclass 應為 BuildNEWSTABLE。"""
        build_news = BuildNEWS()
        assert build_news.typeclass is BuildNEWSTABLE

    def test_build_db(self, mocker):
        """應正確呼叫 BuildEmptyDB 建立 NEWS 資料庫。"""
        build_news = BuildNEWS()
        mock_conn_server = mocker.Mock()
        mock_build_empty_db = mocker.Mock()
        mock_build_empty_db.build.return_value = None
        mocker.patch('build_DB.base.BuildEmptyDB', return_value=mock_build_empty_db)

        build_news.build_db(mock_conn_server)

        mock_build_empty_db.build.assert_called_once_with(mock_conn_server)

    def test_build_table_discovers_subclasses(self, mocker):
        """build_table 應自動發現並建構 BuildNEWSTABLE 的子類別。"""
        build_news = BuildNEWS()
        mock_conn = mocker.Mock()

        subclasses = BuildNEWSTABLE.__subclasses__()
        assert len(subclasses) >= 1
        assert BuildNEWSTABLECTEE in subclasses

        # mock 每個子類別的 build 方法
        for subclass in subclasses:
            mocker.patch.object(subclass, 'build', return_value=None)

        build_news.build_table(mock_conn)

        for subclass in subclasses:
            subclass.build.assert_called_once()


class TestBuildNEWSTABLE:
    """測試 BuildNEWSTABLE 資料表基類。"""

    def test_is_subclass_of_base(self):
        """BuildNEWSTABLE 應繼承自 BaseBuildTABLE。"""
        assert issubclass(BuildNEWSTABLE, BaseBuildTABLE)


class TestBuildNEWSTABLECTEE:
    """測試 BuildNEWSTABLECTEE 資料表建構類別。"""

    def test_table_name(self):
        """CTEE 資料表名稱應為 'CTEE'。"""
        build_ctee = BuildNEWSTABLECTEE()
        assert build_ctee.table_name == "CTEE"

    def test_sql_file_path(self):
        """CTEE 的 SQL 檔案路徑應正確。"""
        build_ctee = BuildNEWSTABLECTEE()
        assert build_ctee.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "CTEE.sql"
        )

    def test_sql_content(self):
        """CTEE 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_ctee = BuildNEWSTABLECTEE()
        assert "CREATE TABLE" in build_ctee.sql
        assert "`NEWS`.`CTEE`" in build_ctee.sql
        assert "`Date`" in build_ctee.sql
        assert "`url`" in build_ctee.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLECTEE 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLECTEE, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 CTEE SQL 中所有欄位名稱。"""
        build_ctee = BuildNEWSTABLECTEE()
        columns = build_ctee._get_defined_columns()

        expected_columns = {'Date', 'Time', 'Author', 'Head', 'SubHead', 'HashTag', 'url', 'ContentFile'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 CTEE 欄位的型別與約束。"""
        build_ctee = BuildNEWSTABLECTEE()
        columns = build_ctee._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'
        assert columns['Time'] == 'TIME DEFAULT NULL'
        assert columns['Author'] == 'VARCHAR(100) DEFAULT NULL'
        assert columns['Head'] == 'VARCHAR(500) NOT NULL'
        assert columns['SubHead'] == 'TEXT DEFAULT NULL'
        assert columns['HashTag'] == 'VARCHAR(500) DEFAULT NULL'
        assert columns['url'] == 'VARCHAR(1000) NOT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_ctee = BuildNEWSTABLECTEE()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_ctee, 'check_table_exists', return_value=False)
        mocker.patch.object(build_ctee, 'post_process')

        build_ctee.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_ctee.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_ctee = BuildNEWSTABLECTEE()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_ctee, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_ctee, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_ctee, 'post_alter')

        build_ctee.build(mock_conn)

        build_ctee._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_ctee.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_ctee = BuildNEWSTABLECTEE()
        mock_conn = mocker.Mock()
        missing = {'HashTag'}
        mocker.patch.object(build_ctee, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_ctee, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_ctee, 'post_alter')

        build_ctee.build(mock_conn)

        build_ctee.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildNEWSTABLECNYES:
    """測試 BuildNEWSTABLECNYES 資料表建構類別。"""

    def test_table_name(self):
        """CNYES 資料表名稱應為 'CNYES'。"""
        build_cnyes = BuildNEWSTABLECNYES()
        assert build_cnyes.table_name == "CNYES"

    def test_sql_file_path(self):
        """CNYES 的 SQL 檔案路徑應正確。"""
        build_cnyes = BuildNEWSTABLECNYES()
        assert build_cnyes.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "CNYES.sql"
        )

    def test_sql_content(self):
        """CNYES 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_cnyes = BuildNEWSTABLECNYES()
        assert "CREATE TABLE" in build_cnyes.sql
        assert "`NEWS`.`CNYES`" in build_cnyes.sql
        assert "`Date`" in build_cnyes.sql
        assert "`url`" in build_cnyes.sql

    def test_sql_no_subhead(self):
        """CNYES 的 SQL 不應包含 SubHead 欄位。"""
        build_cnyes = BuildNEWSTABLECNYES()
        assert "SubHead" not in build_cnyes.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLECNYES 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLECNYES, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 CNYES SQL 中所有欄位名稱。"""
        build_cnyes = BuildNEWSTABLECNYES()
        columns = build_cnyes._get_defined_columns()

        expected_columns = {'Date', 'Time', 'Author', 'Head', 'HashTag', 'url',
                            'ContentFile'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 CNYES 欄位的型別與約束。"""
        build_cnyes = BuildNEWSTABLECNYES()
        columns = build_cnyes._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'
        assert columns['Time'] == 'TIME DEFAULT NULL'
        assert columns['Author'] == 'VARCHAR(100) DEFAULT NULL'
        assert columns['Head'] == 'VARCHAR(500) NOT NULL'
        assert columns['HashTag'] == 'VARCHAR(500) DEFAULT NULL'
        assert columns['url'] == 'VARCHAR(1000) NOT NULL'
        assert columns['ContentFile'] == 'VARCHAR(100) DEFAULT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_cnyes = BuildNEWSTABLECNYES()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_cnyes, 'check_table_exists', return_value=False)
        mocker.patch.object(build_cnyes, 'post_process')

        build_cnyes.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_cnyes.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_cnyes = BuildNEWSTABLECNYES()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_cnyes, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_cnyes, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_cnyes, 'post_alter')

        build_cnyes.build(mock_conn)

        build_cnyes._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_cnyes.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_cnyes = BuildNEWSTABLECNYES()
        mock_conn = mocker.Mock()
        missing = {'HashTag'}
        mocker.patch.object(build_cnyes, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_cnyes, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_cnyes, 'post_alter')

        build_cnyes.build(mock_conn)

        build_cnyes.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildNEWSTABLECNYESUploaded:
    """測試 BuildNEWSTABLECNYESUploaded 資料表建構類別。"""

    def test_table_name(self):
        """CNYESUploaded 資料表名稱應為 'CNYESUploaded'。"""
        build_cnyes_uploaded = BuildNEWSTABLECNYESUploaded()
        assert build_cnyes_uploaded.table_name == "CNYESUploaded"

    def test_sql_file_path(self):
        """CNYESUploaded 的 SQL 檔案路徑應正確。"""
        build_cnyes_uploaded = BuildNEWSTABLECNYESUploaded()
        assert build_cnyes_uploaded.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "CNYESUploaded.sql"
        )

    def test_sql_content(self):
        """CNYESUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_cnyes_uploaded = BuildNEWSTABLECNYESUploaded()
        assert "CREATE TABLE" in build_cnyes_uploaded.sql
        assert "`NEWS`.`CNYESUploaded`" in build_cnyes_uploaded.sql
        assert "`Date`" in build_cnyes_uploaded.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLECNYESUploaded 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLECNYESUploaded, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 CNYESUploaded SQL 中所有欄位名稱。"""
        build_cnyes_uploaded = BuildNEWSTABLECNYESUploaded()
        columns = build_cnyes_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 CNYESUploaded 欄位的型別與約束。"""
        build_cnyes_uploaded = BuildNEWSTABLECNYESUploaded()
        columns = build_cnyes_uploaded._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_cnyes_uploaded = BuildNEWSTABLECNYESUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(
            build_cnyes_uploaded, 'check_table_exists', return_value=False
        )
        mocker.patch.object(build_cnyes_uploaded, 'post_process')

        build_cnyes_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_cnyes_uploaded.post_process.assert_called_once_with(mock_conn)


class TestBuildNEWSTABLEPTT:
    """測試 BuildNEWSTABLEPTT 資料表建構類別。"""

    def test_table_name(self):
        """PTT 資料表名稱應為 'PTT'。"""
        build_ptt = BuildNEWSTABLEPTT()
        assert build_ptt.table_name == "PTT"

    def test_sql_file_path(self):
        """PTT 的 SQL 檔案路徑應正確。"""
        build_ptt = BuildNEWSTABLEPTT()
        assert build_ptt.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "PTT.sql"
        )

    def test_sql_content(self):
        """PTT 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_ptt = BuildNEWSTABLEPTT()
        assert "CREATE TABLE" in build_ptt.sql
        assert "`NEWS`.`PTT`" in build_ptt.sql
        assert "`Date`" in build_ptt.sql
        assert "`url`" in build_ptt.sql

    def test_sql_no_hashtag(self):
        """PTT 的 SQL 不應包含 HashTag 欄位。"""
        build_ptt = BuildNEWSTABLEPTT()
        assert "HashTag" not in build_ptt.sql

    def test_sql_no_subhead(self):
        """PTT 的 SQL 不應包含 SubHead 欄位。"""
        build_ptt = BuildNEWSTABLEPTT()
        assert "SubHead" not in build_ptt.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLEPTT 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLEPTT, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 PTT SQL 中所有欄位名稱。"""
        build_ptt = BuildNEWSTABLEPTT()
        columns = build_ptt._get_defined_columns()

        expected_columns = {'Date', 'Time', 'Author', 'Head', 'url',
                            'ContentFile'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 PTT 欄位的型別與約束。"""
        build_ptt = BuildNEWSTABLEPTT()
        columns = build_ptt._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'
        assert columns['Time'] == 'TIME DEFAULT NULL'
        assert columns['Author'] == 'VARCHAR(100) DEFAULT NULL'
        assert columns['Head'] == 'VARCHAR(500) NOT NULL'
        assert columns['url'] == 'VARCHAR(1000) NOT NULL'
        assert columns['ContentFile'] == 'VARCHAR(100) DEFAULT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_ptt = BuildNEWSTABLEPTT()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_ptt, 'check_table_exists', return_value=False)
        mocker.patch.object(build_ptt, 'post_process')

        build_ptt.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_ptt.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_ptt = BuildNEWSTABLEPTT()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_ptt, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_ptt, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_ptt, 'post_alter')

        build_ptt.build(mock_conn)

        build_ptt._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_ptt.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_ptt = BuildNEWSTABLEPTT()
        mock_conn = mocker.Mock()
        missing = {'ContentFile'}
        mocker.patch.object(build_ptt, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_ptt, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_ptt, 'post_alter')

        build_ptt.build(mock_conn)

        build_ptt.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildNEWSTABLEPTTUploaded:
    """測試 BuildNEWSTABLEPTTUploaded 資料表建構類別。"""

    def test_table_name(self):
        """PTTUploaded 資料表名稱應為 'PTTUploaded'。"""
        build_ptt_uploaded = BuildNEWSTABLEPTTUploaded()
        assert build_ptt_uploaded.table_name == "PTTUploaded"

    def test_sql_file_path(self):
        """PTTUploaded 的 SQL 檔案路徑應正確。"""
        build_ptt_uploaded = BuildNEWSTABLEPTTUploaded()
        assert build_ptt_uploaded.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "PTTUploaded.sql"
        )

    def test_sql_content(self):
        """PTTUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_ptt_uploaded = BuildNEWSTABLEPTTUploaded()
        assert "CREATE TABLE" in build_ptt_uploaded.sql
        assert "`NEWS`.`PTTUploaded`" in build_ptt_uploaded.sql
        assert "`Date`" in build_ptt_uploaded.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLEPTTUploaded 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLEPTTUploaded, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 PTTUploaded SQL 中所有欄位名稱。"""
        build_ptt_uploaded = BuildNEWSTABLEPTTUploaded()
        columns = build_ptt_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 PTTUploaded 欄位的型別與約束。"""
        build_ptt_uploaded = BuildNEWSTABLEPTTUploaded()
        columns = build_ptt_uploaded._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_ptt_uploaded = BuildNEWSTABLEPTTUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(
            build_ptt_uploaded, 'check_table_exists', return_value=False
        )
        mocker.patch.object(build_ptt_uploaded, 'post_process')

        build_ptt_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_ptt_uploaded.post_process.assert_called_once_with(mock_conn)


class TestBuildNEWSTABLEMoneyUDN:
    """測試 BuildNEWSTABLEMoneyUDN 資料表建構類別。"""

    def test_table_name(self):
        """MoneyUDN 資料表名稱應為 'MoneyUDN'。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        assert build_moneyudn.table_name == "MoneyUDN"

    def test_sql_file_path(self):
        """MoneyUDN 的 SQL 檔案路徑應正確。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        assert build_moneyudn.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "MoneyUDN.sql"
        )

    def test_sql_content(self):
        """MoneyUDN 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        assert "CREATE TABLE" in build_moneyudn.sql
        assert "`NEWS`.`MoneyUDN`" in build_moneyudn.sql
        assert "`Date`" in build_moneyudn.sql
        assert "`url`" in build_moneyudn.sql

    def test_sql_no_hashtag(self):
        """MoneyUDN 的 SQL 不應包含 HashTag 欄位。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        assert "HashTag" not in build_moneyudn.sql

    def test_sql_no_subhead(self):
        """MoneyUDN 的 SQL 不應包含 SubHead 欄位。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        assert "SubHead" not in build_moneyudn.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLEMoneyUDN 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLEMoneyUDN, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 MoneyUDN SQL 中所有欄位名稱。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        columns = build_moneyudn._get_defined_columns()

        expected_columns = {'Date', 'Time', 'Author', 'Head', 'url',
                            'ContentFile'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 MoneyUDN 欄位的型別與約束。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        columns = build_moneyudn._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'
        assert columns['Time'] == 'TIME DEFAULT NULL'
        assert columns['Author'] == 'VARCHAR(100) DEFAULT NULL'
        assert columns['Head'] == 'VARCHAR(500) NOT NULL'
        assert columns['url'] == 'VARCHAR(1000) NOT NULL'
        assert columns['ContentFile'] == 'VARCHAR(100) DEFAULT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_moneyudn, 'check_table_exists', return_value=False)
        mocker.patch.object(build_moneyudn, 'post_process')

        build_moneyudn.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_moneyudn.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_moneyudn, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_moneyudn, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_moneyudn, 'post_alter')

        build_moneyudn.build(mock_conn)

        build_moneyudn._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_moneyudn.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_moneyudn = BuildNEWSTABLEMoneyUDN()
        mock_conn = mocker.Mock()
        missing = {'ContentFile'}
        mocker.patch.object(build_moneyudn, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_moneyudn, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_moneyudn, 'post_alter')

        build_moneyudn.build(mock_conn)

        build_moneyudn.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildNEWSTABLEMoneyUDNUploaded:
    """測試 BuildNEWSTABLEMoneyUDNUploaded 資料表建構類別。"""

    def test_table_name(self):
        """MoneyUDNUploaded 資料表名稱應為 'MoneyUDNUploaded'。"""
        build_moneyudn_uploaded = BuildNEWSTABLEMoneyUDNUploaded()
        assert build_moneyudn_uploaded.table_name == "MoneyUDNUploaded"

    def test_sql_file_path(self):
        """MoneyUDNUploaded 的 SQL 檔案路徑應正確。"""
        build_moneyudn_uploaded = BuildNEWSTABLEMoneyUDNUploaded()
        assert build_moneyudn_uploaded.sql_file_path == os.path.join(
            "build_DB", "NEWS_sql", "MoneyUDNUploaded.sql"
        )

    def test_sql_content(self):
        """MoneyUDNUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_moneyudn_uploaded = BuildNEWSTABLEMoneyUDNUploaded()
        assert "CREATE TABLE" in build_moneyudn_uploaded.sql
        assert "`NEWS`.`MoneyUDNUploaded`" in build_moneyudn_uploaded.sql
        assert "`Date`" in build_moneyudn_uploaded.sql

    def test_is_subclass_of_news_table(self):
        """BuildNEWSTABLEMoneyUDNUploaded 應繼承自 BuildNEWSTABLE。"""
        assert issubclass(BuildNEWSTABLEMoneyUDNUploaded, BuildNEWSTABLE)

    def test_get_defined_columns(self):
        """應正確解析 MoneyUDNUploaded SQL 中所有欄位名稱。"""
        build_moneyudn_uploaded = BuildNEWSTABLEMoneyUDNUploaded()
        columns = build_moneyudn_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 MoneyUDNUploaded 欄位的型別與約束。"""
        build_moneyudn_uploaded = BuildNEWSTABLEMoneyUDNUploaded()
        columns = build_moneyudn_uploaded._get_defined_columns()

        assert columns['Date'] == 'DATE NOT NULL'

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_moneyudn_uploaded = BuildNEWSTABLEMoneyUDNUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(
            build_moneyudn_uploaded, 'check_table_exists', return_value=False
        )
        mocker.patch.object(build_moneyudn_uploaded, 'post_process')

        build_moneyudn_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_moneyudn_uploaded.post_process.assert_called_once_with(mock_conn)
