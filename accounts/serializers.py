from phonenumber_field.serializerfields import PhoneNumberField
import phonenumbers
from rest_framework import serializers

from accounts.models import User, UserRole
from core.serializers import EnumField


class UserSerializer(serializers.ModelSerializer):
    """
    Base serializer class for all users, for Retrieval (GET) endpoints
    """
    phone = PhoneNumberField()
    role = EnumField(UserRole)

    class Meta:
        model = User
        fields = ["id", "name", "email", "phone", "location", "role", "is_active", "is_staff", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["name", "email", "phone", "location"]

    def validate_phone(self, value):
        phone_input = str(value)
        raw = ''.join([c for c in phone_input if c.isdigit() or c == '+'])

        region_code = self.context.get("region_code", None)

        candidates = []
        if raw.startswith('+'):
            candidates.append((raw, None))
        else:
            candidates.append((f"+{raw}", None))
            candidates.append((raw, region_code))

        phone_number = None
        for num, region in candidates:
            try:
                parsed = phonenumbers.parse(num, region)
                if phonenumbers.is_valid_number(parsed):
                    phone_number = parsed
                    break
            except phonenumbers.NumberParseException:
                continue

        if not phone_number:
            raise serializers.ValidationError("Invalid phone number")

        normalized_phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        if User.objects.filter(phone=normalized_phone).exists():
            raise serializers.ValidationError("User with that phone already exists")

        return normalized_phone
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["name", "email", "phone", "location"]

    def validate_phone(self, value):
        if not value:
            return value

        phone_input = str(value)
        raw = ''.join([c for c in phone_input if c.isdigit() or c == '+'])

        region_code = self.context.get("region_code", None)

        candidates = []
        if raw.startswith('+'):
            candidates.append((raw, None))
        else:
            candidates.append((f"+{raw}", None))
            candidates.append((raw, region_code))

        phone_number = None
        for num, region in candidates:
            try:
                parsed = phonenumbers.parse(num, region)
                if phonenumbers.is_valid_number(parsed):
                    phone_number = parsed
                    break
            except phonenumbers.NumberParseException:
                continue

        if not phone_number:
            raise serializers.ValidationError("Invalid phone number")

        normalized_phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        if User.objects.filter(phone=normalized_phone).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("User with that phone already exists")

        return normalized_phone
