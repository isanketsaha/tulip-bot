"""Implements section for Black."""
from dataclasses import dataclass
from typing import ClassVar, Optional

from pyvelocity.configurations.files.sections import ConfigurationFileParameter, Section


@dataclass
class Black(Section):
    NAME: ClassVar[str] = "black"
    LIST_PARAMETER_NAME: ClassVar[list[str]] = ["line-length"]
    line_length: ConfigurationFileParameter[Optional[int]]
