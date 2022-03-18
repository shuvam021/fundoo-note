from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'is_verified')
        read_only_fields = ('id',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'password', 'is_verified')
        read_only_fields = ('id', 'is_verified')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
