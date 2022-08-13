from py_orm import set_config


def test_config():
    set_config(
        config={
            'driver': '',
            'url': '',
            'migrate_files': '',
        }
    )
