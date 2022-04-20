import asyncio
import os
from typing import NoReturn, Union

import loguru
from aiohttp import web, web_exceptions

from archive_download_service.settings import (ARCHIVE_CHUNK_SIZE_KB,
                                               ARCHIVE_URL_KEY_NAME,
                                               DEFAULT_DELAY_SECS,
                                               DEFAULT_FILES_DIR_PATH)
from archive_download_service.utils.file_paths import get_dir_full_path
from archive_download_service.utils.process import kill_process_tree
from archive_download_service.utils.request_headers import \
    get_headers_for_zip_file
from archive_download_service.utils.static import read_static_file
from archive_download_service.utils.zip_launcher import \
        create_zip_util_process


async def archive(
        request: web.Request,
) -> Union[web.StreamResponse, NoReturn]:
    loguru.logger.info("{0}".format(request))
 
    requested_dir_full_path: str = ""
    requested_dir_name = request.match_info.get(ARCHIVE_URL_KEY_NAME)
    if requested_dir_name:
        requested_dir_full_path = get_dir_full_path(requested_dir_name)
    if not os.path.exists(requested_dir_full_path) or not requested_dir_name:
        return await handle_archive_not_found(request)

    headers = get_headers_for_zip_file(requested_dir_name)
    response = web.StreamResponse(headers=headers)
    chunk_size_b = int(ARCHIVE_CHUNK_SIZE_KB * 1000)
    try:
        while True:
            process = await create_zip_util_process(requested_dir_full_path)
            parent_pid = process.pid
            if process.stdout is not None:
                while not process.stdout.at_eof():
                    file_content = await process.stdout.read(chunk_size_b)
                    await response.prepare(request)
                    await response.write(file_content)
                    delay_secs = request.app.get("delay")
                    if delay_secs:
                        await asyncio.sleep(float(delay_secs))
                loguru.logger.success("Complete download")
                return response
    except asyncio.CancelledError:
        loguru.logger.info("Cancel download (reason=user)")
    except BaseException as e:
        loguru.logger.error("{0}, args{1}".format(e.__class__, e.args))
        loguru.logger.error("Interrupt download (reason=error)")
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


def run_server(
        path: str = DEFAULT_FILES_DIR_PATH,
        logging_enabled: bool = False,
        delay_secs: float = DEFAULT_DELAY_SECS,
) -> None:
    if not logging_enabled:
        loguru.logger.remove()
    app = web.Application(middlewares=[web.normalize_path_middleware()])
    app["path"] = path
    app["delay"] = delay_secs
    app.add_routes([
        web.get("/", handle_index_page),
        web.get("/archive/{archive_hash}/", archive),
    ])
    web.run_app(app)
