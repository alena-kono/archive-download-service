import psutil


def kill_process_tree(pid: int, including_parent: bool = True) -> None:
    timeout = 5
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    psutil.wait_procs(children, timeout=timeout)
    if including_parent:
        parent.kill()
        parent.wait(timeout)
