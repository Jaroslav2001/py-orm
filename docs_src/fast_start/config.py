from py_orm import set_config, Config

set_config(
    Config(
        url='sqlite://data.db',
        migrate_dir='data',
    )
)
