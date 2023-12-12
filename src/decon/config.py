from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class DependencySpec:
    """Dependency specification config"""

    apt: list[str]
    pip: list[str]


@dataclass(slots=True)
class BuildSpec:
    """Build configuration data"""

    base_image: str
    dependencies: DependencySpec

    def __post_init__(self):
        self.dependencies = DependencySpec(**self.dependencies)


@dataclass(slots=True)
class Config:
    """Main configuration data"""

    build: BuildSpec

    def __post_init__(self):
        self.build = BuildSpec(**self.build)


def load_config(config_path: Path | None = None) -> Config:
    """Load the YAML configuration file

    Parameters
    ----------
    config_path : Path | None, optional
        The path to the configuration file, by default ``decon.yaml``
        in the current working directory

    Returns
    -------
    Config
        The loaded configuration
    """
    if config_path is None:
        config_path = Path.cwd() / "decon.yaml"

    with config_path.open() as f:
        config_yaml = yaml.safe_load(f)

    return Config(**config_yaml)
