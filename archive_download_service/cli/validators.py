import argparse
import os
from typing import NoReturn, Union


def validate_path(path: str) -> Union[str, NoReturn]:
    if not os.path.exists(path):
        msg = "{0} does not exist.".format(path)
        raise argparse.ArgumentError(message=msg, argument=None)
    return path


def validate_delay(
        delay_secs: Union[int, float, str],
) -> Union[float, NoReturn]:
    try:
        delay_secs_float = float(delay_secs)
    except ValueError:
        msg = "{0} cannot be converted into float.".format(delay_secs)
        raise argparse.ArgumentError(message=msg, argument=None)
    if delay_secs_float < 0:
        msg = "{0} cannot be less than 0.".format(delay_secs)
        raise argparse.ArgumentError(message=msg, argument=None)
    return delay_secs_float
