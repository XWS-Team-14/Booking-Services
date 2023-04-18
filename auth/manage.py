#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from auth.asgi import serve


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # if command is 'runserver' it runs it on port that can be passed after or on port 50051
    if sys.argv[1] == 'runserver':
        if sys.argv[2] is not None:
            serve(sys.argv[2])
        else:
            serve('50051')
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
