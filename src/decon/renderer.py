import logging
import textwrap
from abc import ABC, abstractmethod

from typing_extensions import override

from decon.config import Config


class Renderer(ABC):
    """Base class for all renderers."""

    def __init__(self, config: Config):
        self.config = config

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}@{id(self):x}"

    @classmethod
    @abstractmethod
    def accepts(cls, config: Config) -> bool:
        """Whether this renderer can render the given configuration."""

    @abstractmethod
    def render(self) -> str:
        """Render a container image specification."""


class BaseImageRenderer(Renderer):
    """Renderer for a base image specification."""

    @override
    @classmethod
    def accepts(cls, config: Config) -> bool:
        try:
            return config.build.base_image is not None
        except AttributeError:
            logging.warning("Could not validate config", exc_info=True)
            return False

    @override
    def render(self) -> str | None:
        return f"FROM {self.config.build.base_image}"


class AptDependencyRenderer(Renderer):
    """Renderer for installation of Debian/Ubuntu (apt) dependencies."""

    @override
    @classmethod
    def accepts(cls, config: Config) -> bool:
        try:
            return config.build.dependencies.apt is not None
        except AttributeError:
            logging.warning("Could not validate config", exc_info=True)
            return False

    @override
    def render(self) -> str | None:
        packages = self.config.build.dependencies.apt
        return textwrap.dedent(
            f"""
        RUN apt-get update && \\
            apt-get install -y --no-install-recommends {' '.join(packages)} && \\
            apt-get clean && \\
            rm -rf /var/lib/apt/lists/*
        """
        ).strip()


class PythonDependencyRenderer(Renderer):
    """Renderer for installation of Python (pip) dependencies."""

    @override
    @classmethod
    def accepts(cls, config: Config) -> bool:
        try:
            return config.build.dependencies.pip is not None
        except AttributeError:
            logging.warning("Could not validate config", exc_info=True)
            return False

    @override
    def render(self) -> str | None:
        packages = self.config.build.dependencies.pip
        return f"RUN pip install {' '.join(packages)}"


# All renderer implementations must be listed here - ordering is significant.
RENDERERS = [
    BaseImageRenderer,
    AptDependencyRenderer,
    PythonDependencyRenderer,
]
