from rest_framework import serializers
from .models import Role, SystemUser, ApprovalWorkflow, Delegation, LoginEvent, DeviceSession


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class SystemUserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        source='role',
        allow_null=True,
        required=False
    )
    role = serializers.CharField(read_only=True)

    class Meta:
        model = SystemUser
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password_hash', None)
        user = SystemUser(**validated_data)
        from django.contrib.auth.hashers import make_password
        if not password:
            password = 'TempPassword123!'
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
    role = serializers.SerializerMethodField()
    role_id = serializers.SerializerMethodField()

    class Meta:
        model = SystemUser
        fields = '__all__'
        read_only_fields = ['password_hash']

    def get_role(self, obj):
        return obj.role.name if obj.role else None

    def get_role_id(self, obj):
        return obj.role.id if obj.role else None


class ApprovalWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalWorkflow
        fields = '__all__'


class DelegationSerializer(serializers.ModelSerializer):
    delegator = serializers.CharField(source='from_user.name', read_only=True)
    delegator_role = serializers.SerializerMethodField()
    delegate = serializers.CharField(source='to_user.name', read_only=True)
    delegate_role = serializers.SerializerMethodField()
    from_date = serializers.DateField(source='start_date')
    to_date = serializers.DateField(source='end_date')

    class Meta:
        model = Delegation
        fields = [
            'id', 'delegator', 'delegator_role', 'delegate', 'delegate_role',
            'from_date', 'to_date', 'reason', 'status', 'scope', 'created_at'
        ]

    def get_delegator_role(self, obj):
        return obj.from_user.role.name if obj.from_user and obj.from_user.role else None

    def get_delegate_role(self, obj):
        return obj.to_user.role.name if obj.to_user and obj.to_user.role else None

    def create(self, validated_data):
        request = self.context.get('request')
        raw_data = request.data if request else self.initial_data
        delegator_name = raw_data.get('delegator')
        delegate_name = raw_data.get('delegate')

        from_user = SystemUser.objects.filter(name__iexact=delegator_name).first()
        to_user = SystemUser.objects.filter(name__iexact=delegate_name).first()

        if not from_user:
            raise serializers.ValidationError({"delegator": f"SystemUser '{delegator_name}' not found."})
        if not to_user:
            raise serializers.ValidationError({"delegate": f"SystemUser '{delegate_name}' not found."})

        # Remove nested source fields if present
        validated_data.pop('from_user', None)
        validated_data.pop('to_user', None)

        delegation = Delegation.objects.create(
            from_user=from_user,
            to_user=to_user,
            **validated_data
        )
        return delegation

    def update(self, instance, validated_data):
        request = self.context.get('request')
        raw_data = request.data if request else self.initial_data
        
        delegator_name = raw_data.get('delegator')
        delegate_name = raw_data.get('delegate')

        if delegator_name:
            from_user = SystemUser.objects.filter(name__iexact=delegator_name).first()
            if not from_user:
                raise serializers.ValidationError({"delegator": f"SystemUser '{delegator_name}' not found."})
            instance.from_user = from_user

        if delegate_name:
            to_user = SystemUser.objects.filter(name__iexact=delegate_name).first()
            if not to_user:
                raise serializers.ValidationError({"delegate": f"SystemUser '{delegate_name}' not found."})
            instance.to_user = to_user

        validated_data.pop('from_user', None)
        validated_data.pop('to_user', None)

        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class LoginEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginEvent
        fields = '__all__'


class DeviceSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSession
        fields = '__all__'
