import os

from aiohttp import web

from archive_download_service.settings import TEST_FILES_DIR_PATH


def get_path_of_file(filename: str) -> str:
    return os.path.join(
        os.getcwd(),
        TEST_FILES_DIR_PATH,
        filename,
    )


def get_filename_from_request(
        request: web.Request,
        request_keyword: str,
) -> str:
    return request.match_info.get(request_keyword, "untitled")
