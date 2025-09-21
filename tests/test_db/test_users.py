import pytest
import allure


@allure.story("用户数据库操作")
class TestUserDB:
    @allure.title("测试用户插入")
    def test_insert_user(self, db_ops, test_users):
        test_data = test_users[0]
        with allure.step("插入用户数据"):
            user_id = db_ops.insert_user(
                test_data["name"],
                test_data["email"],
                test_data["age"]
            )

        with allure.step("验证插入结果"):
            assert user_id is not None
            user = db_ops.get_user_by_id(user_id)
            assert user["name"] == test_data["name"]
            assert user["email"] == test_data["email"]
            assert user["age"] == test_data["age"]

    @allure.title("测试重复邮箱插入")
    def test_duplicate_email(self, db_ops, test_users):
        test_data = test_users[0]
        db_ops.insert_user(test_data["name"], test_data["email"], test_data["age"])

        with allure.step("尝试插入重复邮箱"):
            result = db_ops.insert_user(
                "另一个名字",
                test_data["email"],
                40
            )
            assert result is None