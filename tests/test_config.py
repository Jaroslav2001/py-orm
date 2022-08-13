from py_orm import BaseModel


def test_config():
    BaseModel.set_config(
        config={
            'driver': '',
            'url': '',
            'migrate_files': '',
        }
    )
