from archive_download_service.cli.dotenv_writer import write_kwargs_to_dotenv
from archive_download_service.cli.parser import (create_cli_parser,
                                                 parse_cli_args)
from archive_download_service.server import run_server


def main() -> None:
    cli_parser = create_cli_parser()
    cli_kwargs = parse_cli_args(cli_parser)
    if cli_kwargs:
        write_kwargs_to_dotenv(cli_kwargs)
    run_server()


if __name__ == "__main__":
    main()
