import asyncio
from asyncio.subprocess import Process

import loguru


async def create_zip_util_process(dir_to_be_zipped: str) -> Process:
    cmd = "zip -rjq - {dir}".format(dir=dir_to_be_zipped)
    loguru.logger.info("Start zip process: {0}".format(cmd))
    return await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
        )
