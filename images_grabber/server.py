import os
from typing import NoReturn, Union

import aiofiles
from aiohttp import web

from images_grabber.utils.file_paths import (get_filename_from_request,
                                             get_path_of_file)
from images_grabber.utils.request_headers import get_headers_for_zip_file
from images_grabber.utils.zip_launcher import create_zip_util_process


async def archive(
        request: web.Request
) -> Union[web.StreamResponse, NoReturn]:
    output_filename = get_filename_from_request(
            request,
            request_keyword="archive_hash",
        )
    input_dir = get_path_of_file(output_filename)
    if not os.path.exists(input_dir):
        # raise HTTPNotFound()
        return await handle_404(request)

    # Launch zip util that archives files
    process = await create_zip_util_process(input_dir)
    if process.stdout is not None:
        # Streaming response
        response = web.StreamResponse(
                headers=get_headers_for_zip_file(output_filename),
            )
        await response.prepare(request)

        while not process.stdout.at_eof():
            file_content = await process.stdout.read(n=500 * 1000)
            await response.write(file_content)
        return response
    raise web.HTTPError


async def handle_index_page(request: web.Request) -> web.Response:
    index_file_path = "./images_grabber/templates/index.html"
    async with aiofiles.open(index_file_path, mode="r") as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


async def handle_404(request: web.Request) -> web.Response:
    not_found_file_path = "./images_grabber/templates/404.html"
    async with aiofiles.open(not_found_file_path, mode="r") as page_404:
        contents = await page_404.read()
    return web.Response(status=404, text=contents, content_type="text/html")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", handle_index_page),
        web.get("/archive/{archive_hash}/", archive),
    ])
    web.run_app(app)
