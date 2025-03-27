"""Implements docformatter configurations.

see:
  - Welcome to docformatter! — docformatter documentation
    https://docformatter.readthedocs.io/en/latest/
"""
from typing import Optional

from pyvelocity.configurations.files.aggregation import ConfigurationFiles
from pyvelocity.configurations.files.sections import (
    ConfigurationFileParameter,
    docformatter,
    is_not_none_value,
    WhereToolDefault,
)
from pyvelocity.configurations.tools import Tool


class Docformatter(Tool):
    """docformatter configurations."""

    NAME = "docformatter"

    def __init__(self, configuration_files: ConfigurationFiles) -> None:
        where_tool_default = WhereToolDefault(self)
        self.wrap_descriptions = ConfigurationFileParameter(
            where_tool_default, ConfigurationFileParameter.NAME_TOOL_DEFAULT, 72
        )
        self.wrap_summaries = ConfigurationFileParameter(
            where_tool_default, ConfigurationFileParameter.NAME_TOOL_DEFAULT, 79
        )
        if configuration_files.setup_cfg:
            self.overwrite(configuration_files.setup_cfg.docformatter)
        if configuration_files.py_project_toml:
            self.overwrite(configuration_files.py_project_toml.docformatter)

    def overwrite(self, section_docformatter: Optional[docformatter.Docformatter]) -> None:
        if section_docformatter:
            if is_not_none_value(section_docformatter.wrap_descriptions):
                self.wrap_descriptions = section_docformatter.wrap_descriptions
            if is_not_none_value(section_docformatter.wrap_summaries):
                self.wrap_summaries = section_docformatter.wrap_summaries
