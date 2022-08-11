from typing import TypedDict, NoReturn, Type


class Setting(TypedDict):
    driver: str
    url: str
    default_type_id: Type


setting: Setting


def set_setting(
    driver: str,
    url: str,
    *,
    default_type_id: Type = int,
) -> NoReturn:
    global setting
    setting: Setting = {
        'driver': driver,
        'url': url,
        'default_type_id': default_type_id,
    }
