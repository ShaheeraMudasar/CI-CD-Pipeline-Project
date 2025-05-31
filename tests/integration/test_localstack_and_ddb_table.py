import boto3
import pytest
from hamcrest import assert_that, equal_to, is_, contains_string

from app.env import feature_ddb_enabled, get_aws_credentials

TABLE_NAME = "DevOps1_Posts"

def test_feature_ddb_flag_is_enabled():
    # GIVEN att environment har laddats
    # WHEN vi kollar feature flag för DDB
    flag = feature_ddb_enabled()

    # THEN ska DDB-flaggan vara på
    assert_that(flag, is_(True))


def test_aws_env_variables_are_set_to_use_localstack():
    # GIVEN att vi använder get_aws_credentials
    creds = get_aws_credentials()

    # WHEN vi hämtar access key, secret och endpoint
    # THEN ska de ha förväntade värden
    assert_that(creds["aws_access_key_id"], equal_to("test"))
    assert_that(creds["aws_secret_access_key"], equal_to("test"))
    assert_that(creds["endpoint_url"], contains_string("localhost"))


def test_localstack_is_reachable():
    # GIVEN en dynamodb klient med localstack endpoint
    ddb = boto3.client("dynamodb", **get_aws_credentials())

    # WHEN vi listar tabeller
    tables = ddb.list_tables()

    # THEN ska vi få ett svar som innehåller en lista
    assert_that(tables, "TableNames" in tables)
    assert_that(isinstance(tables["TableNames"], list), is_(True))


def test_ddb_table_exists():
    # GIVEN en dynamodb klient med localstack endpoint
    ddb = boto3.client("dynamodb", **get_aws_credentials())

    # WHEN vi listar tabeller
    tables = ddb.list_tables()["TableNames"]

    # THEN ska DevOps1_Posts-tabellen finnas
    assert_that(TABLE_NAME in tables, is_(True))