from rest_framework import serializers
from .models import official , User

class OfficialRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = official
        fields = ['username','password','phone_number','email']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)  # Ensure password is set correctly
        instance.save()
        return instance


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)  # Ensure password is set correctly
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class OfficialUpdateSerializer(serializers.Serializer):
    class Meta:
        model = official
        fields ="__all__"

class UserUpdateSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields ="__all__"