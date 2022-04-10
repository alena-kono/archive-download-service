import asyncio
import os
from typing import NoReturn, Union

import loguru
from aiohttp import web, web_exceptions

from archive_download_service.settings import (ARCHIVE_CHUNK_SIZE_KB,
                                               ARCHIVE_URL_KEY_NAME)
from archive_download_service.utils.file_paths import (
    get_filename_from_request, get_path_of_file)
from archive_download_service.utils.process import kill_process_tree
from archive_download_service.utils.request_headers import \
    get_headers_for_zip_file
from archive_download_service.utils.static import read_static_file
from archive_download_service.utils.zip_launcher import \
    create_zip_util_process


async def archive(
        request: web.Request
) -> Union[web.StreamResponse, NoReturn]:
    output_filename = get_filename_from_request(
            request,
            request_keyword=ARCHIVE_URL_KEY_NAME,
        )
    input_dir = get_path_of_file(output_filename)
    if not os.path.exists(input_dir):
        return await handle_archive_not_found(request)

    headers = get_headers_for_zip_file(output_filename)
    response = web.StreamResponse(headers=headers)
    chunk_size_b = ARCHIVE_CHUNK_SIZE_KB * 1000
    try:
        while True:
            process = await create_zip_util_process(input_dir)
            parent_pid = process.pid
            if process.stdout is not None:
                while not process.stdout.at_eof():
                    file_content = await process.stdout.read(chunk_size_b)
                    await response.prepare(request)
                    await response.write(file_content)
                loguru.logger.success("Download completed")
                return response
    except asyncio.CancelledError:
        loguru.logger.warning("Download was cancelled by user")
    except BaseException as e:
        loguru.logger.error("{0}, args{1}".format(e.__class__, e.args))
        loguru.logger.error("Download was cancelled due to error")
    finally:
        kill_process_tree(parent_pid)
        return response


async def handle_index_page(
        request: web.Request,
) -> Union[web.Response, NoReturn]:
    index_content = await read_static_file("index.html")
    if index_content:
        return web.Response(
                text=index_content,
                content_type="text/html",
            )
    raise web_exceptions.HTTPNotFound()


async def handle_archive_not_found(
        request: web.Request,
) -> Union[web.Response, NoReturn]:
    page_404_content = await read_static_file("404.html")
    if page_404_content:
        return web.Response(
                status=404,
                text=page_404_content,
                content_type="text/html",
            )
    raise web_exceptions.HTTPNotFound()


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", handle_index_page),
        web.get("/archive/{archive_hash}/", archive),
        web.get("/archive/{archive_hash}", archive),
    ])
    web.run_app(app)
