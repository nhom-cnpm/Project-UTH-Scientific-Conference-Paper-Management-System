import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.bases_settings")
django.setup()

from apps.accounts.models import ID

ID.objects.create(Ten="Bao Nhu")

print("✅ Insert OK")
