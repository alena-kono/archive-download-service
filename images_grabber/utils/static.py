from typing import Optional
import aiofiles


async def read_static_file(path: str) -> Optional[str]:
    """Read file located at `path`."""
    try:
        async with aiofiles.open(path, mode="r") as output_file:
            file_contents = await output_file.read()
    except FileNotFoundError:
        return None
    return file_contents
