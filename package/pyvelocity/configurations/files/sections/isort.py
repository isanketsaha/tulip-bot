"""Implements section for isort."""
from dataclasses import dataclass
from typing import ClassVar, Optional

from pyvelocity.configurations.files.sections import ConfigurationFileParameter, Section


@dataclass
class Isort(Section):
    NAME: ClassVar[str] = "isort"
    LIST_PARAMETER_NAME: ClassVar[list[str]] = ["line_length"]
    line_length: ConfigurationFileParameter[Optional[int]]
