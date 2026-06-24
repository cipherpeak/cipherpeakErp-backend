from rest_framework import serializers
from .models import Role, SystemUser, ApprovalWorkflow, Delegation, LoginEvent, DeviceSession


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class SystemUserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = SystemUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password_hash')
        user = SystemUser(**validated_data)
        from django.contrib.auth.hashers import make_password
        user.password_hash = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password_hash', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            from django.contrib.auth.hashers import make_password
            instance.password_hash = make_password(password)
        instance.save()
        return instance


class SystemUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemUser
        fields = '__all__'
        read_only_fields = ['password_hash']


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = '__all__'


class DelegationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delegation
        fields = '__all__'


class LoginEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginEvent
        fields = '__all__'


class DeviceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSession
        fields = '__all__'
