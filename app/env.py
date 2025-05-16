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


############################
# Getters för Feature flags
############################


def feature_ddb_enabled() -> bool:
    return _get_flag("FEATURE_DDB", default="false")


def feature_admin_enabled() -> bool:
    return _get_flag("FEATURE_ADMIN", default="false")
