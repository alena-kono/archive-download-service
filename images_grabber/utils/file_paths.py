import os

from aiohttp import web

DEBUG = True


def get_path_of_file(filename: str) -> str:
    dir_path = ""
    if DEBUG:
        dir_path = "images_grabber/test_photos"
    return os.path.join(
            os.getcwd(),
            dir_path,
            filename,
        )


def get_filename_from_request(
        request: web.Request,
        request_keyword: str,
) -> str:
    return request.match_info.get(request_keyword, "untitled")
