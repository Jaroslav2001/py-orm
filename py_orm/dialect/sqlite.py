from .abstract import DialectSQL


sqlite: DialectSQL = {
    'schema_table': '',
    'create_table': 'CREATE TABLE',
    'alter_table': 'ALTER TABLE',
    'drop_table': 'DROP TABLE',
}
