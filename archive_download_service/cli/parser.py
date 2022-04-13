import argparse
from typing import Dict, Optional

from archive_download_service.cli.validators import (validate_delay,
                                                     validate_path)
from archive_download_service.settings import (DEFAULT_DELAY_SECS,
                                               DEFAULT_FILES_DIR_PATH)


def create_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
            description="Microservice",
            exit_on_error=False,
        )
    parser.add_argument(
            "-p",
            "--path",
            metavar="path",
            action="store",
            type=validate_path,
            nargs="?",
            help="Path to files directory.",
            default=DEFAULT_FILES_DIR_PATH,
        )
    parser.add_argument(
            "-l",
            "--logging",
            action="store_true",
            help="Enable logging.",
        )
    parser.add_argument(
            "-d",
            "--delay",
            metavar="secs_float",
            action="store",
            type=validate_delay,
            nargs="?",
            help="Response delay in seconds.",
            default=DEFAULT_DELAY_SECS,
        )
    return parser


def parse_cli_args(
        parser: argparse.ArgumentParser,
) -> Optional[Dict[str, str]]:
    try:
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        raise SystemExit
    return args.__dict__
