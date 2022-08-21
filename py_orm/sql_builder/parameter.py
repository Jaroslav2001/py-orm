from typing import Union, Iterable

from pypika import (
    Parameter as _Parameter,
)


def p(
        placeholder: Union[str, int, None] = None,
) -> _Parameter:
    if placeholder is None:
        placeholder = ''
    return _Parameter(f"{{{placeholder}}}")


def p_dict(
        placeholder: Iterable[str],
) -> _Parameter:
    return _Parameter(
        f"${' '.join(map(lambda x: f'{{{x}}}', placeholder))}"
    )
