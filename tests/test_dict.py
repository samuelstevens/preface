from .. import dict


def test_set_dict_without_nested_dict() -> None:
    dct: dict.StrDict = {}

    key = "a.b.c"

    value = 1

    expected: dict.StrDict = {"a": {"b": {"c": 1}}}
    dict.set(dct, key, value)

    assert dct == expected


def test_merge_dict_without_nested() -> None:
    a: dict.StrDict = {"a": 1}
    b: dict.StrDict = {"b": 2}

    expected: dict.StrDict = {"a": 1, "b": 2}
    actual = dict.merge(a, b)

    assert actual == expected


def test_merge_dict_with_nested() -> None:
    a: dict.StrDict = {"a": {"b": 1}}
    b: dict.StrDict = {"b": 2, "a": {"c": 3}}

    expected: dict.StrDict = {"a": {"b": 1, "c": 3}, "b": 2}
    actual = dict.merge(a, b)

    assert actual == expected
