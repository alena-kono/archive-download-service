from typing import Optional

import aiofiles

from archive_download_service.settings import STATIC_DIR_PATH


async def read_static_file(filename: str) -> Optional[str]:
    """Read file located at `filename`."""
    dir_path = _get_abs_file_path(filename)
    try:
        async with aiofiles.open(dir_path, mode="r") as output_file:
            file_contents = await output_file.read()
    except FileNotFoundError:
        return None
    return file_contents


def _get_abs_file_path(filename: str) -> str:
    return STATIC_DIR_PATH + "/" + filename
