import dataclasses
import os
from typing import Type, TypeVar, get_type_hints

T = TypeVar('T')


def fill_dataclass_from_env(cls: Type[T]) -> T:
    cls_name = cls.__name__.upper()
    kwargs = {}
    for var_name, var_type in get_type_hints(cls).items():
        env_name = f"{cls_name}_{var_name.upper()}"
        env_val = os.getenv(env_name)
        kwargs[var_name] = var_type(env_val)
    return cls(**kwargs)
