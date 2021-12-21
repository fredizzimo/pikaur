""" This file is licensed under GPLv3, see https://www.gnu.org/licenses/ """

from os import path, listdir
from typing import Dict, List, cast
from .config import PikaurConfig
from .srcinfo import SrcInfo
from .aur import AURPackageInfo


class CustomPackageInfo(AURPackageInfo):
    @property
    def repository(self) -> str:
        return PikaurConfig().misc.CustomPackagePrefix.get_str()

    @property
    def git_url(self):
        return None

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


def get_custom_package_infos() -> Dict[str, CustomPackageInfo]:
    pkgs = get_custom_pkgs()
    results = {}
    for pkg in pkgs:
        base_srcinfo = pkg.srcinfo
        for name in base_srcinfo.pkgnames:
            srcinfo = SrcInfo(
                pkgbuild_path=pkg.pkgbuild_path,
                package_name=name)
            results[name] = CustomPackageInfo.from_srcinfo(srcinfo)

    return results


def custom_pkg_search_name_desc(queries: List[str]) -> Dict[str, List[CustomPackageInfo]]:
    pkgs = get_custom_package_infos().values()
    if queries:
        results = {}
        for query in queries:
            for pkg in pkgs:
                name = pkg.name if pkg.name is not None else ''
                desc = pkg.desc if pkg.desc is not None else ''
                if query in name or query in desc:
                    results.setdefault(query, []).append(pkg)
    else:
        results = {'all': list(pkgs)}

    return results
