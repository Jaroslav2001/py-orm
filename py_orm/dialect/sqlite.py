from .abstract import DialectSQL


sqlite: DialectSQL = {
    'list_table': "SELECT name FROM sqlite_schema WHERE type == 'table';",
    'schema_table': "SELECT sql FROM sqlite_schema WHERE type == 'table' AND name = {name};",
    'create_table': 'CREATE TABLE',
    'alter_table': 'ALTER TABLE',
    'drop_table': 'DROP TABLE',
}
