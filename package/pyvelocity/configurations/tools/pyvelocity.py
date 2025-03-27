"""Implements pyvelocity configurations."""
from typing import Optional

from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.files.sections import (
    ConfigurationFileParameter,
    is_not_none_value,
    pyvelocity,
    WhereToolDefault,
)
from pyvelocity.configurations.tools import Tool


class Pyvelocity(Tool):
    """pyvelocity configurations."""

    NAME = "pyvelocity"

    def __init__(self, configuration_files: ConfigurationFiles) -> None:
        self.filter: ConfigurationFileParameter[list[str]] = ConfigurationFileParameter(
            WhereToolDefault(self), ConfigurationFileParameter.NAME_TOOL_DEFAULT, []
        )
        if configuration_files.py_project_toml:
            self.overwrite(configuration_files.py_project_toml.pyvelocity)

    def overwrite(self, section_pyvelocity: Optional[pyvelocity.Pyvelocity]) -> None:
        if section_pyvelocity:
            if is_not_none_value(section_pyvelocity.filter):
                self.filter = section_pyvelocity.filter
