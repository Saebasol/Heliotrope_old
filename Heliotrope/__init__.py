from collections import namedtuple

__version__ = "2.10.0"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")

version_info = VersionInfo(major=2, minor=10, micro=0, releaselevel="final", serial=0)
