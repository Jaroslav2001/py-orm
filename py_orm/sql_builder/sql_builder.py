class SQLBuilder:
    @staticmethod
    def decorator_value(value):
        if isinstance(value, str):
            return f"\'{value}\'"
