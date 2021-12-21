""" This file is licensed under GPLv3, see https://www.gnu.org/licenses/ """

from os import path, listdir
from typing import Dict, List, cast
from .config import PikaurConfig
from .srcinfo import SrcInfo
from .aur import AURPackageInfo


class CustomPackageInfo(AURPackageInfo):
    @classmethod
    def from_srcinfo(cls, srcinfo) -> 'CustomPackageInfo':
        return cast(CustomPackageInfo, super().from_srcinfo(srcinfo))


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


def custom_pkg_search_name_desc(queries: List[str]) -> Dict[str, List[CustomPackageInfo]]:
    pkgs = get_custom_pkgs()
    if queries:
        results = {}
        for query in queries:
            for pkg in pkgs:
                base_srcinfo = pkg.srcinfo
                for name in base_srcinfo.pkgnames:
                    srcinfo = SrcInfo(
                        pkgbuild_path=pkg.pkgbuild_path,
                        package_name=name)
                    descs = srcinfo.get_values('pkgdesc')
                    desc = " ".join(descs)
                    if query in name or query in desc:
                        results.setdefault(query, []).append(
                            CustomPackageInfo.from_srcinfo(srcinfo))
    else:
        results = {'all': [CustomPackageInfo.from_srcinfo(pkg.srcinfo) for pkg in pkgs]}

    return results
