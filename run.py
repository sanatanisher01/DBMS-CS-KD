import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sportsphere.settings")
    try:
        execute_from_command_line(["manage.py", "runserver"])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
