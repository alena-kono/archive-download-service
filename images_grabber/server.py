from aiohttp import web
import aiofiles


async def archive(request: web.Request) -> Exception:
    raise NotImplementedError


async def handle_index_page(request: web.Request) -> web.Response:
    index_file_path = "./images_grabber/index.html"
    async with aiofiles.open(index_file_path, mode="r") as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type="text/html")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([
        web.get("/", handle_index_page),
        web.get("/archive/{archive_hash}/", archive),
    ])
    web.run_app(app)
