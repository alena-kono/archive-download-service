import os

from aiohttp import web

from archive_download_service.settings import DEFAULT_FILES_DIR_PATH


def get_path_of_file(filename: str, files_dir_path: str) -> str:
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
