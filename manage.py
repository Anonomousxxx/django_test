#!/usr/bin/env python
import os
import sys
from django.core.management.commands.runserver import Command as runserver

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demigosTest.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    runserver.default_port = "7000"
    execute_from_command_line(sys.argv)
