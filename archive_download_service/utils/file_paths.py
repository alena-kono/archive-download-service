import os

from archive_download_service.settings import DEFAULT_FILES_DIR_PATH


def get_dir_full_path(
        target_dir: str,
        base_dir_path: str = DEFAULT_FILES_DIR_PATH,
) -> str:
    return os.path.join(
        os.getcwd(),
        base_dir_path,
        target_dir,
    )
