""" This file is licensed under GPLv3, see https://www.gnu.org/licenses/ """

from os import path, listdir
from .config import PikaurConfig
from .srcinfo import SrcInfo


class CustomPackage:
    def __init__(self, custom_path: str, name: str):
        self.name = name
        self.pkgbuild_path = path.join(custom_path, name, 'PKGBUILD')
        self.srcinfo = SrcInfo(pkgbuild_path=self.pkgbuild_path)


def get_custom_pkg_path():
    custom_path = PikaurConfig().misc.CustomPackagePath.get_str()
    custom_path = path.expandvars(custom_path)
    custom_path = path.expanduser(custom_path)
    custom_path = path.abspath(custom_path)
    return custom_path


def get_custom_pkgs():
    custom_path = get_custom_pkg_path()
    ret = []
    if path.exists(custom_path):
        for pkg_name in listdir(custom_path):
            ret.append(CustomPackage(custom_path, pkg_name))
    return ret
