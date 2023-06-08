#!/usr/bin/env python
"""Simple command-line utility for administrative tasks."""
import asyncio
import sys
import signal
from app.manage.run_server import serve, _cleanup_coroutines
from loguru import logger
import logging_loki


handler = logging_loki.LokiHandler(
    url="http://loki:3100/loki/api/v1/push", 
    tags={"application": "my-app"},
    version="1",
)

logger.add(
    handler,
    format="{level} {message}",
)

def main():
    """Run administrative tasks."""

    # if command is 'runserver' it runs it on
    # port that can be passed after or on port 50051
    if sys.argv[1] == "runserver":
        port = "50051"
        if len(sys.argv) == 3:
            port = sys.argv[2]
        start(port)
    elif sys.argv[1] == "help":
        print(
            "Commands: \n"
            + "\t runserver [port] - runs server on a given port (please provide a vaild port) or on a port 50051 if not provided\n"
            + "\t help - shows this help text\n"
        )
    else:
        print(
            f"Command '{sys.argv[1]}' is not yet implemented.\n"
            + "If you think it should be implemented contact me!\n"
            + "Run command 'help' to get list of all commands available."
        )


def start(port):
    def exit_gracefully_handler(signum, frame):
        raise SystemExit

    loop = asyncio.get_event_loop()
    signal.signal(signal.SIGINT, exit_gracefully_handler)
    signal.signal(signal.SIGTERM, exit_gracefully_handler)

    try:
        loop.run_until_complete(serve(port))
    except (
        KeyboardInterrupt,
        SystemExit,
    ) as e:
        logger.critical(f"Received signal = {e}")
        loop.run_until_complete(*_cleanup_coroutines)
    finally:
        loop.close()
        logger.critical("Closed loop.")


if __name__ == "__main__":
    main()
