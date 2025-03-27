"""Implements Flake8 configurations."""
from typing import Optional

from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.files.sections import (
    ConfigurationFileParameter,
    flake8,
    is_not_none_value,
    WhereToolDefault,
)
from pyvelocity.configurations.tools import Tool


class Flake8(Tool):
    """Flake8 configurations."""

    NAME = "Flake8"

    def __init__(self, configuration_files: ConfigurationFiles) -> None:
        self.max_line_length = ConfigurationFileParameter(
            WhereToolDefault(self), ConfigurationFileParameter.NAME_TOOL_DEFAULT, 79
        )
        if configuration_files.setup_cfg:
            self.overwrite(configuration_files.setup_cfg.flake8)

    def overwrite(self, section_flake8: Optional[flake8.Flake8]) -> None:
        if section_flake8:
            if is_not_none_value(section_flake8.max_line_length):
                self.max_line_length = section_flake8.max_line_length
