import multiprocessing
def join_path(path, name):
    path = path.replace('\\', '/')
    path = path.rstrip('/')
    path = path + "/" + name
    return path


