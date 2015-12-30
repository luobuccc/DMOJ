import os
import sys

fs_encoding = os.environ.get('DMOJ_ENCODING', sys.getfilesystemencoding())


def unicodify(string):
    if isinstance(string, str):
        return string.decode(fs_encoding)
    return string


def configure(object):
    global env, problem_path
    env = object

    dirs = object['problem_storage_root']
    if isinstance(dirs, list):
        problem_path = [unicodify(os.path.normpath(dir)) for dir in dirs]
    else:
        problem_path = [unicodify(os.path.normpath(dirs))]
