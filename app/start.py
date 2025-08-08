from app.env import feature_admin_enabled, feature_ddb_enabled, is_production
from app.main import create_app

print("[STARTUP] Creating FastAPI application")
print(f"[STARTUP] Environment - Production: {is_production()}")
print(f"[STARTUP] Feature flags - DDB: {feature_ddb_enabled()}, Admin: {feature_admin_enabled()}")

app = create_app()

print("[STARTUP] FastAPI application created successfully")
