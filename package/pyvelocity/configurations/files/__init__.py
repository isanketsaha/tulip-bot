"""Implements configuration files."""
from abc import ABC, abstractmethod


class ConfigurationFile(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError  # pragma: no cover
