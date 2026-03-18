import os

import pytest

from build_DB.base import BaseBuildTABLE
from build_DB.special_info import (BuildSPECIAL_INFO, BuildSPECIAL_INFOTABLE,
                                    BuildSPECIAL_INFOTABLEOilPrice,
                                    BuildSPECIAL_INFOTABLEOilPriceUploaded)


class TestBuildSPECIAL_INFO:
    """測試 BuildSPECIAL_INFO 資料庫建構類別。"""

    def test_name(self):
        """BuildSPECIAL_INFO 的名稱應為 'SPECIAL_INFO'。"""
        build_special_info = BuildSPECIAL_INFO()
        assert build_special_info.name == "SPECIAL_INFO"

    def test_typeclass(self):
        """BuildSPECIAL_INFO 的 typeclass 應為 BuildSPECIAL_INFOTABLE。"""
        build_special_info = BuildSPECIAL_INFO()
        assert build_special_info.typeclass is BuildSPECIAL_INFOTABLE

    def test_build_db(self, mocker):
        """應正確呼叫 BuildEmptyDB 建立 SPECIAL_INFO 資料庫。"""
        build_special_info = BuildSPECIAL_INFO()
        mock_conn_server = mocker.Mock()
        mock_build_empty_db = mocker.Mock()
        mock_build_empty_db.build.return_value = None
        mocker.patch('build_DB.base.BuildEmptyDB', return_value=mock_build_empty_db)

        build_special_info.build_db(mock_conn_server)

        mock_build_empty_db.build.assert_called_once_with(mock_conn_server)

    def test_build_table_discovers_subclasses(self, mocker):
        """build_table 應自動發現並建構 BuildSPECIAL_INFOTABLE 的子類別。"""
        build_special_info = BuildSPECIAL_INFO()
        mock_conn = mocker.Mock()

        subclasses = BuildSPECIAL_INFOTABLE.__subclasses__()
        assert len(subclasses) >= 2
        assert BuildSPECIAL_INFOTABLEOilPrice in subclasses
        assert BuildSPECIAL_INFOTABLEOilPriceUploaded in subclasses

        # mock 每個子類別的 build 方法
        for subclass in subclasses:
            mocker.patch.object(subclass, 'build', return_value=None)

        build_special_info.build_table(mock_conn)

        for subclass in subclasses:
            subclass.build.assert_called_once()


class TestBuildSPECIAL_INFOTABLE:
    """測試 BuildSPECIAL_INFOTABLE 資料表基類。"""

    def test_is_subclass_of_base(self):
        """BuildSPECIAL_INFOTABLE 應繼承自 BaseBuildTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLE, BaseBuildTABLE)


class TestBuildSPECIAL_INFOTABLEOilPrice:
    """測試 BuildSPECIAL_INFOTABLEOilPrice 資料表建構類別。"""

    def test_table_name(self):
        """OilPrice 資料表名稱應為 'OilPrice'。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        assert build_oil_price.table_name == "OilPrice"

    def test_sql_file_path(self):
        """OilPrice 的 SQL 檔案路徑應正確。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        assert build_oil_price.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "OilPrice.sql"
        )

    def test_sql_content(self):
        """OilPrice 的 SQL 內容應包含 CREATE TABLE 語句與所有欄位。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        assert "CREATE TABLE" in build_oil_price.sql
        assert "`SPECIAL_INFO`.`OilPrice`" in build_oil_price.sql
        assert "`Date`" in build_oil_price.sql
        assert "`Product`" in build_oil_price.sql
        assert "`Open`" in build_oil_price.sql
        assert "`High`" in build_oil_price.sql
        assert "`Low`" in build_oil_price.sql
        assert "`Close`" in build_oil_price.sql
        assert "`Volume`" in build_oil_price.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEOilPrice 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEOilPrice, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 OilPrice SQL 中所有欄位名稱。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        columns = build_oil_price._get_defined_columns()

        expected_columns = {'Date', 'Product', 'Open', 'High', 'Low', 'Close', 'Volume'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 OilPrice 欄位的型別與約束。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        columns = build_oil_price._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL"
        assert columns['Product'] == "VARCHAR(10) NOT NULL COMMENT '原油類型: WTI, Brent'"
        assert columns['Open'] == "DECIMAL(10, 2) COMMENT '開盤價'"
        assert columns['High'] == "DECIMAL(10, 2) COMMENT '最高價'"
        assert columns['Low'] == "DECIMAL(10, 2) COMMENT '最低價'"
        assert columns['Close'] == "DECIMAL(10, 2) COMMENT '收盤價'"
        assert columns['Volume'] == "BIGINT COMMENT '成交量'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_oil_price, 'check_table_exists', return_value=False)
        mocker.patch.object(build_oil_price, 'post_process')

        build_oil_price.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_oil_price.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_oil_price, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_oil_price, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_oil_price, 'post_alter')

        build_oil_price.build(mock_conn)

        build_oil_price._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_oil_price.post_alter.assert_not_called()

    def test_build_existing_table_with_missing_columns(self, mocker):
        """資料表已存在且有缺少欄位時，應呼叫 post_alter。"""
        build_oil_price = BuildSPECIAL_INFOTABLEOilPrice()
        mock_conn = mocker.Mock()
        missing = {'Volume'}
        mocker.patch.object(build_oil_price, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_oil_price, '_alter_table_add_columns', return_value=missing
        )
        mocker.patch.object(build_oil_price, 'post_alter')

        build_oil_price.build(mock_conn)

        build_oil_price.post_alter.assert_called_once_with(mock_conn, missing)


class TestBuildSPECIAL_INFOTABLEOilPriceUploaded:
    """測試 BuildSPECIAL_INFOTABLEOilPriceUploaded 資料表建構類別。"""

    def test_table_name(self):
        """OilPriceUploaded 資料表名稱應為 'OilPriceUploaded'。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        assert build_uploaded.table_name == "OilPriceUploaded"

    def test_sql_file_path(self):
        """OilPriceUploaded 的 SQL 檔案路徑應正確。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        assert build_uploaded.sql_file_path == os.path.join(
            "build_DB", "SPECIAL_INFO_sql", "OilPriceUploaded.sql"
        )

    def test_sql_content(self):
        """OilPriceUploaded 的 SQL 內容應包含 CREATE TABLE 語句。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        assert "CREATE TABLE" in build_uploaded.sql
        assert "`SPECIAL_INFO`.`OilPriceUploaded`" in build_uploaded.sql
        assert "`Date`" in build_uploaded.sql

    def test_is_subclass(self):
        """BuildSPECIAL_INFOTABLEOilPriceUploaded 應繼承自 BuildSPECIAL_INFOTABLE。"""
        assert issubclass(BuildSPECIAL_INFOTABLEOilPriceUploaded, BuildSPECIAL_INFOTABLE)

    def test_get_defined_columns(self):
        """應正確解析 OilPriceUploaded SQL 中所有欄位名稱。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        expected_columns = {'Date'}
        assert set(columns.keys()) == expected_columns

    def test_column_definitions(self):
        """應正確解析 OilPriceUploaded 欄位的型別與約束。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        columns = build_uploaded._get_defined_columns()

        assert columns['Date'] == "DATE NOT NULL PRIMARY KEY COMMENT '已上傳日期'"

    def test_build_creates_table(self, mocker):
        """資料表不存在時，應執行 CREATE TABLE、commit 並呼叫 post_process。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=False)
        mocker.patch.object(build_uploaded, 'post_process')

        build_uploaded.build(mock_conn)

        mock_conn.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        build_uploaded.post_process.assert_called_once_with(mock_conn)

    def test_build_existing_table(self, mocker):
        """資料表已存在時，應呼叫 _alter_table_add_columns 而非 CREATE TABLE。"""
        build_uploaded = BuildSPECIAL_INFOTABLEOilPriceUploaded()
        mock_conn = mocker.Mock()
        mocker.patch.object(build_uploaded, 'check_table_exists', return_value=True)
        mocker.patch.object(
            build_uploaded, '_alter_table_add_columns', return_value=set()
        )
        mocker.patch.object(build_uploaded, 'post_alter')

        build_uploaded.build(mock_conn)

        build_uploaded._alter_table_add_columns.assert_called_once_with(mock_conn)
        build_uploaded.post_alter.assert_not_called()
