"""Implements section for docformatter."""
from dataclasses import dataclass
from typing import ClassVar, Optional

from pyvelocity.configurations.files.sections import ConfigurationFileParameter, Section


@dataclass
class Docformatter(Section):
    """Section of docformatter."""

    NAME: ClassVar[str] = "docformatter"
    LIST_PARAMETER_NAME: ClassVar[list[str]] = [
        "wrap-descriptions",
        "wrap-summaries",
    ]
    wrap_descriptions: ConfigurationFileParameter[Optional[int]]
    wrap_summaries: ConfigurationFileParameter[Optional[int]]
