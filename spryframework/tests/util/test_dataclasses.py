import pytest
import dataclasses
import os

from spryframework.util.dataclasses import fill_dataclass_from_env


@dataclasses.dataclass
class DataClass:
    test: str


def test_fill_dataclass_from_env(monkeypatch):
    monkeypatch.setenv('DATACLASS_TEST', 'TEST')
    dataclass_object = fill_dataclass_from_env(DataClass)
    assert dataclass_object.test == 'TEST'
