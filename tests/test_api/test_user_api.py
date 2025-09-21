import pytest
import allure


@allure.feature("用户API测试")
class TestUserAPI:
    @allure.story("获取用户信息")
    @allure.title("测试获取存在的用户")
    def test_get_existing_user(self, api_client):
        with allure.step("发送GET请求"):
            user = api_client.get_user(1)

        with allure.step("验证响应数据"):
            assert user is not None
            assert "id" in user
            assert "name" in user

    @allure.story("获取用户信息")
    @allure.title("测试获取不存在的用户")
    def test_get_nonexistent_user(self, api_client):
        with allure.step("发送GET请求"):
            user = api_client.get_user(99999)
            assert user is None