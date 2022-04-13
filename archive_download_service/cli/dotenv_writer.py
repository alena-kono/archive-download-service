import os
from typing import Any, Dict

import dotenv

from archive_download_service.settings import DEFAULT_ENV_PATH


def write_kwargs_to_dotenv(
        kwargs: Dict[str, Any],
        path: str = DEFAULT_ENV_PATH,
) -> None:
    _clean_dotenv(path)
    for arg_name, arg_value in kwargs.items():
        dotenv.set_key(path, arg_name, str(arg_value))


def _clean_dotenv(path: str) -> None:
    if os.path.exists(path):
        os.remove(path)
