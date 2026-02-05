from django.apps import AppConfig
from django.db import connection

class CoreConfig(AppConfig):
    name = 'config'

    def ready(self):
        try:
            connection.ensure_connection()
            print("✅ Connected to SQL Server (AppDB)")
        except Exception as e:
            print("❌ SQL Connection Failed:", e)