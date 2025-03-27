"""Implements Black configurations."""
from typing import Optional

from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.files.sections import (
    black,
    ConfigurationFileParameter,
    is_not_none_value,
    WhereToolDefault,
)
from pyvelocity.configurations.tools import Tool


class Black(Tool):
    """Black configurations."""

    NAME = "Black"

    def __init__(self, configuration_files: ConfigurationFiles) -> None:
        self.line_length = ConfigurationFileParameter(
            WhereToolDefault(self), ConfigurationFileParameter.NAME_TOOL_DEFAULT, 88
        )
        if configuration_files.py_project_toml:
            self.overwrite(configuration_files.py_project_toml.black)

    def overwrite(self, section_black: Optional[black.Black]) -> None:
        if section_black:
            if is_not_none_value(section_black.line_length):
                self.line_length = section_black.line_length
