import json
import os
from datetime import datetime
from . import ABBREV
from . import git


template = """# AUTOMATICALLY GENERATED BY 'RELIC':
# * DO NOT EDIT THIS MODULE MANUALLY.
# * DO NOT COMMIT THIS MODULE TO YOUR GIT REPOSITORY

__all__ = [
    '__version__',
    '__version_short__',
    '__version_long__',
    '__version_post__',
    '__version_commit__',
    '__version_date__',
    '__version_dirty__',
    '__build_date__',
    '__build_time__',
    '__build_status__'
]

__version__ = '{0}'
__version_short__ = '{1}'
__version_long__ = '{2}'
__version_post__ = '{3}'
__version_commit__ = '{4}'
__version_date__ = '{5}'
__version_dirty__ = {6}
__build_date__ = '{7}'
__build_time__ = '{8}'
__build_status__ = 'release' if not int(__version_post__) > 0 \\
    and not __version_dirty__ \\
    else 'development'
"""


def write_template(info, module_path, filename='version.py'):
    assert isinstance(info, git.GitVersion)
    path = os.path.join(module_path, filename)
    build_date = datetime.now().date()
    build_time = datetime.now().time()
    with open(path, 'w+') as f:
        output = template.format(
            info.pep386,
            info.short,
            info.long,
            info.post,
            info.commit,
            info.date,
            info.dirty,
            build_date,
            build_time
        )
        f.write(output)


def write_info(version):
    info = version

    if isinstance(version, git.GitVersion):
        info = version._asdict()

    with open('RELIC-INFO', 'w+') as f:
        f.write(json.dumps(info))
        f.write('\n')


def read_info():
    try:
        with open('RELIC-INFO', 'r') as f:
            data = json.loads(f.read())
            return git.GitVersion(**data)
    except (OSError, IOError):
        return None


def get_info(remove_pattern='release_'):
    relic_data = read_info()
    git_data = git.git_version_info(remove_pattern=remove_pattern)

    if not relic_data and not git_data:
        print('warning: no version data available!')
        return _fallback()

    elif git_data != relic_data and git_data:
        write_info(git_data)
        return git_data

    return relic_data


def _fallback():
    no_ver = '0.0.0'
    data = dict(
        pep386=no_ver,
        short=no_ver,
        long=no_ver,
        date='',
        dirty=True,
        commit='',
        post='-1',
    )
    return git.GitVersion(**data)
