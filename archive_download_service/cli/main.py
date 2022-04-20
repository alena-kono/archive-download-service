import argparse
from typing import Dict, NoReturn, Optional

from archive_download_service.cli.parser import (create_cli_parser,
                                                 parse_cli_args)
from archive_download_service.server import run_server
from archive_download_service.settings import (DEFAULT_DELAY_SECS,
                                               DEFAULT_FILES_DIR_PATH)


def main() -> Optional[NoReturn]:
    cli_parser = create_cli_parser()
    cli_kwargs: Dict[str, str] = {}
    try:
        cli_kwargs = parse_cli_args(cli_parser)
    except argparse.ArgumentError as e:
        print(e)
        raise SystemExit
    run_server(
            path=cli_kwargs.get("path", DEFAULT_FILES_DIR_PATH),
            logging_enabled=bool(cli_kwargs.get("logging", False)),
            delay_secs=float(cli_kwargs.get("delay", DEFAULT_DELAY_SECS)),
        )
    return None


if __name__ == "__main__":
    main()
