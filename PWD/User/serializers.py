from rest_framework import serializers
from .models import official

class OfficialSerializer(serializers.ModelSerializer):
    class Meta:
        model = official
        fields = ['name','password','phone_number','email']

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