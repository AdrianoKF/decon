import logging
from pathlib import Path

from typer import Typer

from decon.assembler import DefaultAssembler
from decon.config import load_config

app = Typer(name="decon")


logging.basicConfig(level=logging.DEBUG)


@app.command()
def run(config_file: Path = None) -> None:
    config = load_config(config_path=config_file)
    assembler = DefaultAssembler(config)
    dockerfile = assembler.build_dockerfile()
    print(dockerfile)


if __name__ == "__main__":
    run()
