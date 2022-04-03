import asyncio
from asyncio.subprocess import Process


async def create_zip_util_process(dir_to_be_zipped: str) -> Process:
    cmd = "zip -rj - {dir}".format(dir=dir_to_be_zipped)
    return await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
        )
