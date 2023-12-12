import logging
from io import StringIO

from decon.config import Config
from decon.renderer import RENDERERS


class DefaultAssembler:
    """Default (framework-agnostic) assembler."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def build_dockerfile(self) -> str:
        renderers = [cls(self.config) for cls in RENDERERS if cls.accepts(self.config)]
        logging.debug("Applicable renderers: %s", renderers)

        dockerfile = StringIO()

        for r in renderers:
            dockerfile.write(r.render())
            dockerfile.write("\n")

        return dockerfile.getvalue().strip()
