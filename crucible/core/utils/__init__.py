import uuid
from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import TypeVar

TDefault = TypeVar("TDefault")


def get_timestamped_id() -> str:
    """A unique, roughly-sortable id: a readable timestamp plus a 4-char uppercase random string."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%b-%d_%H-%M-%S")
    rand_suffix = uuid.uuid4().hex[:4].upper()
    return f"{timestamp}_{rand_suffix}"


def smart_getattr(
    obj: object | Mapping[str, object],
    keypath: str | Sequence[str],
    default: TDefault | None = None,
    sep: str = ".",
) -> object | TDefault | None:
    """Returns the value of the attribute or key if it exists,
    otherwise the specified default value.
    """
    keys = keypath.split(sep) if isinstance(keypath, str) else keypath

    for key in keys:
        if isinstance(obj, Mapping):
            obj = obj.get(key)
        elif hasattr(obj, key):
            obj = getattr(obj, key)
        else:
            return default

        if obj is None:
            return default
    return obj
