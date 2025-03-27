"""Implements line length check."""
from collections import Counter
from typing import Any, Optional

from pyvelocity.checks import Check, Result
from pyvelocity.configurations.files.sections import ConfigurationFileParameter


class LineLength(Check):
    """Check about line length."""

    ID = "line-length"

    def execute(self) -> Result:
        target_configurations: list[ConfigurationFileParameter[int]] = []
        target_configurations = [
            self.configurations.docformatter.wrap_descriptions,
            self.configurations.docformatter.wrap_summaries,
            self.configurations.isort.line_length,
            self.configurations.black.line_length,
            self.configurations.flake8.max_line_length,
            self.configurations.pylint.format.max_line_length,
        ]
        counter = Counter([target_configuration.value for target_configuration in target_configurations])
        most_common = counter.most_common()[0]
        is_ok = most_common[1] == len(target_configurations)
        message = "" if is_ok else (self.build_message(most_common, target_configurations))
        return Result(self.ID, is_ok, message)

    @staticmethod
    def build_message(
        most_common: tuple[Optional[Any], int], target_configurations: list[ConfigurationFileParameter[int]]
    ) -> str:
        """Builds message."""
        error_messages = [
            f"{target_configuration.full_name} = {str(target_configuration.value)}"
            for target_configuration in target_configurations
            if target_configuration.value != most_common[0]
        ]
        return "Line length are not consistent.\n\t" f"Most common = {most_common[0]}\n\t" + "\n\t".join(error_messages)
