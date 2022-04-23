import asyncio
from asyncio.subprocess import Process

import loguru


async def create_zip_util_process(dir_to_be_zipped: str) -> Process:
    cmd_list = ["zip", "-rq", "-", "."]
    loguru.logger.info("Start zip process: cmd={cmd} at dir={dir}".format(
        cmd=cmd_list,
        dir=dir_to_be_zipped,
        ))
    return await asyncio.create_subprocess_exec(
            *cmd_list,
            cwd=dir_to_be_zipped,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
        )
