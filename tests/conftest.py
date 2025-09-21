import pytest
import yaml
from src.db_operations import DBOperations
from src.api_client import APIClient

@pytest.fixture(scope="session")
def db_config():
    with open("config/db_config.yaml") as f:
        return yaml.safe_load(f)["test"]


@pytest.fixture(scope="function")
def db_ops(db_config):
    ops = DBOperations("test")
    if not ops.connect():
        pytest.fail("数据库连接失败")

    # 清空表数据
    with ops.conn.cursor() as cursor:
        cursor.execute("DELETE FROM users")
        ops.conn.commit()

    # 确保表存在
    if not ops.create_table():
        pytest.fail("创建表失败")

    yield ops
    ops.close()
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_users():
    with open("tests/test_data/test_users.yaml") as f:
        return yaml.safe_load(f)