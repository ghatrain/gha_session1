import os

# Databricks Apps injects DATABRICKS_APP_PORT; Docker/local fall back to PORT or 5000.
bind = f"0.0.0.0:{os.getenv('DATABRICKS_APP_PORT') or os.getenv('PORT', '5000')}"
workers = 2
