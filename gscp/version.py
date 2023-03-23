import dataclasses
import os
from typing import Optional

import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("gscp").version
except pkg_resources.DistributionNotFound:
    __version__ = os.environ.get("gscp_version", "0.0.0+CI")


@dataclasses.dataclass
class ApplicationVersion:
    """
    Container for the application version
    """

    major: int
    minor: int
    patch: int
    build: Optional[str]

    @staticmethod
    def parse(version_str: str = __version__) -> "ApplicationVersion":
        # Because of the stupid docker tags, we have to support minuses as `+`. So...
        splat_on: str
        if "-" in version_str:
            splat_on = "-"
        else:
            splat_on = "+"

        splat = version_str.split(splat_on)

        if len(splat) > 1:
            build = splat[-1]
        else:
            build = None

        integer_parts = [int(part) for part in splat[0].split(".")]

        version = ApplicationVersion(
            major=integer_parts[0],
            minor=integer_parts[1],
            patch=integer_parts[2],
            build=build,
        )

        return version

    def __str__(self) -> str:
        build = f"+{self.build}" if self.build is not None else ""
        return f"{self.major}.{self.minor}.{self.patch}{build}"
