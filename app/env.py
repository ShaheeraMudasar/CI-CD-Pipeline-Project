import os
from typing import Optional

from dotenv import load_dotenv

_loaded_env = False


def _ensure_env_loaded() -> None:
    """Load .env once, on first call."""
    global _loaded_env
    if not _loaded_env:
        load_dotenv()
        _loaded_env = True


def _get_flag(env_var_name: str, default: str = "false") -> bool:
    """Return a boolean feature flag from environment."""
    _ensure_env_loaded()
    return os.getenv(env_var_name, default).strip().lower() == "true"


def _get_env_var(env_var_name: str, default: Optional[str]) -> str:
    """Return a raw env var (or default)."""
    _ensure_env_loaded()
    return os.getenv(env_var_name, default)


############################
# Getters för miljövariabler
############################


def get_admin_password(default: str = "admin1234") -> str:
    """Fetch the admin password from env, or default."""
    return _get_env_var("ADMIN_PASSWORD", default)


def get_aws_region() -> str:
    return _get_env_var("AWS_REGION", "us-east-1")


def get_aws_endpoint_url() -> Optional[str]:
    return _get_env_var("AWS_ENDPOINT_URL", "http://localhost:4566")


def get_aws_credentials() -> dict:
    return {
        "aws_access_key_id": _get_env_var("AWS_ACCESS_KEY_ID", "test"),
        "aws_secret_access_key": _get_env_var("AWS_SECRET_ACCESS_KEY", "test"),
        "region_name": get_aws_region(),
        "endpoint_url": get_aws_endpoint_url(),
    }


############################
# Getters för Feature flags
############################


def feature_ddb_enabled() -> bool:
    return _get_flag("FEATURE_DDB", default="false")


def feature_admin_enabled() -> bool:
    return _get_flag("FEATURE_ADMIN", default="false")


############################
# Miljödetektering
############################


def is_production() -> bool:
    """Check if running in production environment (AppRunner)."""
    # Vid körning i AppRunner finns det en instansroll och AWS_ACCESS_KEY_ID är inte satt
    # Vid lokal körning är AWS nycklar satta (från .env eller miljövariabler)
    return _get_env_var("AWS_ACCESS_KEY_ID", None) is None


def get_dynamodb_config() -> dict:
    """Get DynamoDB configuration based on environment."""
    config = {"region_name": get_aws_region()}

    if is_production():
        # AppRunner: Använd IAM-roll, dvs inga explicita autentiseringsuppgifter
        return config
    # Lokal/Test: Använd explicita autentiseringsuppgifter + endpoint
    config.update(
        {
            "aws_access_key_id": _get_env_var("AWS_ACCESS_KEY_ID", "test"),
            "aws_secret_access_key": _get_env_var("AWS_SECRET_ACCESS_KEY", "test"),
        }
    )
    # Inkludera endast endpoint_url om den har ett värde
    endpoint_url = get_aws_endpoint_url()
    if endpoint_url:
        config["endpoint_url"] = endpoint_url
    return config
