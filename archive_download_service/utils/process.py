import psutil


def kill_process_tree(pid: int, including_parent: bool = True) -> None:
    timeout = 5
    try:
        parent = psutil.Process(pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    psutil.wait_procs(children, timeout=timeout)
    if parent.is_running() and including_parent:
        parent.kill()
        parent.wait(timeout)
