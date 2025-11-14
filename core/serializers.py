from rest_framework import serializers


class EnumField(serializers.Field):
    def __init__(self, enum_class, *args, **kwargs):
        self.enum_class = enum_class
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        if isinstance(value, self.enum_class):
            return value.value
        return str(value)

    def to_internal_value(self, data):
        try:
            return self.enum_class(data)
        except ValueError:
            raise serializers.ValidationError(f"Invalid value for enum {self.enum_class.__name__}: {data}")

    def get_schema(self):
        return {
            "type": "string",
            "enum": [e.value for e in self.enum_class],
        }
