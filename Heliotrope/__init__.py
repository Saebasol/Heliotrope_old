from collections import namedtuple

__version__ = "3.5.1"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=3, minor=5, micro=1, releaselevel="final", serial=0)
