from pathlib import Path

from decon.cli import run


def test_e2e():
    run(config_file=Path(__file__).parents[1] / "_data" / "example.yaml")
