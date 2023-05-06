from typing import Any, Dict, Reversible, Union

StrDict = Dict[str, object]
Key = Union[str, Reversible[str]]
Primitive = Union[str, int, float, bool, None]


def typesafeindex(dct: StrDict, key: str) -> StrDict:
    obj = dct[key]

    if not isinstance(obj, dict):
        raise KeyError(f"Dict does not contain a subdict at '{key}'.")

    return obj


def get(dct: StrDict, key: Key, sep: str = ".") -> Any:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))
    while len(key) > 1:
        popped = key.pop()
        dct = typesafeindex(dct, popped)

    return dct[key.pop()]


def contains(dct: StrDict, key: Key, sep: str = ".") -> bool:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))
    while len(key) > 1:
        popped = key.pop()
        if popped not in dct:
            return False

        try:
            dct = typesafeindex(dct, popped)
        except KeyError:
            return False

    return key[0] in dct


def delete(dct: StrDict, key: Key, sep: str = ".") -> None:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))

    while len(key) > 1:
        popped = key.pop()
        dct = typesafeindex(dct, popped)

    del dct[key[0]]


def set(dct: StrDict, key: Key, value: Any, sep: str = ".") -> None:
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))

    while len(key) > 1:
        k = key.pop()

        if k not in dct:
            dct[k] = {}

        dct = typesafeindex(dct, k)

    dct[key[0]] = value


def merge(*dcts: StrDict) -> StrDict:
    result: StrDict = {}
    for dct in dcts:
        for key, value in flattened(dct).items():
            set(result, key, value)

    return result


def flattened(dct: Dict[str, Any]) -> Dict[str, Primitive]:
    new = {}
    for key, value in dct.items():
        if isinstance(value, dict):
            for nested_key, nested_value in flattened(value).items():
                new[key + "." + nested_key] = nested_value
            continue

        new[key] = value

    return new


def pop(dct: Dict[str, Any], key: Key, sep: str = ".") -> Any:
    """
    Pops a field out of a dict.
    """
    if isinstance(key, str):
        key = key.split(sep)

    key = list(reversed(key))

    while len(key) > 1:
        dct = typesafeindex(dct, key.pop())

    value = dct[key[0]]

    del dct[key[0]]

    return value
