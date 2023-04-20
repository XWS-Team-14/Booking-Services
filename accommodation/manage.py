#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accommodation.settings')
    import django
    django.setup()
    try:
        from django.core.management import execute_from_command_line
        from accommodation.asgi import serve
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # if command is 'runserver' it runs it on port that can be passed after or on port 50051
    if sys.argv[1] == 'runserver':

        if len(sys.argv) == 3:
            serve(sys.argv[2])
        else:
            serve('50051')
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
