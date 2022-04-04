import os
from typing import NoReturn, Union

import loguru
from aiohttp import web, web_exceptions
from archive_download_service.settings import ARCHIVE_CHUNK_SIZE_KB, ARCHIVE_URL_KEY_NAME

from archive_download_service.utils.file_paths import (
    get_filename_from_request, get_path_of_file)
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

    # Launch zip util that archives files
    process = await create_zip_util_process(input_dir)
    if process.stdout is not None:
        # Streaming response
        response = web.StreamResponse(
                headers=get_headers_for_zip_file(output_filename),
            )
        await response.prepare(request)

        while not process.stdout.at_eof():
            file_content = await process.stdout.read(
                    n=ARCHIVE_CHUNK_SIZE_KB * 1000
                )
            loguru.logger.info("Sending archive chunk")
            await response.write(file_content)
        return response
    return await handle_archive_not_found(request)


async def handle_index_page(
        request: web.Request
) -> Union[web.Response, NoReturn]:
    index_content = await read_static_file("index.html")
    if index_content:
        return web.Response(
                text=index_content,
                content_type="text/html",
            )
    raise web_exceptions.HTTPNotFound()


async def handle_archive_not_found(
        request: web.Request
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