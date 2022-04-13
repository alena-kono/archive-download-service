import os

import dotenv
from aiohttp import web

from archive_download_service.settings import (DEFAULT_ENV_PATH,
                                               DEFAULT_FILES_DIR_PATH)


def get_path_of_file(filename: str) -> str:
    files_dir_path = dotenv.get_key(DEFAULT_ENV_PATH, "path")
    return os.path.join(
        os.getcwd(),
        files_dir_path or DEFAULT_FILES_DIR_PATH,
        filename,
    )


def get_filename_from_request(
        request: web.Request,
        request_keyword: str,
) -> str:
    return request.match_info.get(request_keyword, "untitled")
