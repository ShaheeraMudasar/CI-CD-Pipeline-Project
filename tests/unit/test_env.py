from unittest.mock import patch

from hamcrest import assert_that, equal_to

from app import env


def test_get_admin_password_returns_default_when_unset():
    # resets the flag so it reloads env again
    env._loaded_env = False
    # Simulate empty environment (no ADMIN_PASSWORD)
    with patch.dict("os.environ", {}, clear=True):
        result = env.get_admin_password()
        assert_that(result, equal_to("admin1234"))


def test_get_admin_password_uses_env_var_when_set():
    env._loaded_env = False
    # Simulate ADMIN_PASSWORD set
    with patch.dict("os.environ", {"ADMIN_PASSWORD": "Super$ecret!"}, clear=True):
        result = env.get_admin_password()
        assert_that(result, equal_to("Super$ecret!"))


def test_get_admin_password_accepts_custom_default():
    env._loaded_env = False
    # Simulate empty env but pass custom default
    with patch.dict("os.environ", {}, clear=True):
        result = env.get_admin_password(default="fallback123")
        assert_that(result, equal_to("fallback123"))


def test_get_aws_region():
    env._loaded_env = False
    # simulates aws region
    with patch.dict("os.environ", {"AWS_REGION": "us-east"}):
        result = env.get_aws_region()
        assert_that(result, equal_to("us-east"))


def test_get_aws_region_returns_aws_endpoint_url():
    env._loaded_env = False
    # simulates aws endpoint utl
    with patch.dict("os.environ", {"AWS_ENDPOINT_URL": "http://test.com"}, clear=True):
        result = env.get_aws_endpoint_url()
        assert_that(result, equal_to("http://test.com"))


def test_get_aws_credentials_uses_env_vars():
    env._loaded_env = False
    with patch.dict(
        "os.environ",
        {
            "AWS_ACCESS_KEY_ID": "mykey",
            "AWS_SECRET_ACCESS_KEY": "mysecret",
            "AWS_REGION": "eu-north-1",
            "AWS_ENDPOINT_URL": "http://dynamodb:8000",
        },
        clear=True,
    ):
        result = env.get_aws_credentials()

        expected = {
            "aws_access_key_id": "mykey",
            "aws_secret_access_key": "mysecret",
            "region_name": "eu-north-1",
            "endpoint_url": "http://dynamodb:8000",
        }
        assert_that(result, equal_to(expected))
