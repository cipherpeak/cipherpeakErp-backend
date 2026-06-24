from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Role, SystemUser, ApprovalWorkflow, Delegation, LoginEvent, DeviceSession
from .serializers import (
    RoleSerializer, SystemUserSerializer, SystemUserListSerializer,
    ApprovalWorkflowSerializer, DelegationSerializer,
    LoginEventSerializer, DeviceSessionSerializer,
)
from . import services


# ===========================================================================
# ROLE VIEWSET
# ===========================================================================

class RoleViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Roles to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        roles = services.get_all_roles()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        role = get_object_or_404(Role, pk=pk)
        serializer = RoleSerializer(role)
        return Response(serializer.data)

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = services.create_role(serializer.validated_data)
        return Response(RoleSerializer(role).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        role = get_object_or_404(Role, pk=pk)
        serializer = RoleSerializer(role, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_role = services.update_role(role, serializer.validated_data)
        return Response(RoleSerializer(updated_role).data)

    def partial_update(self, request, pk=None):
        role = get_object_or_404(Role, pk=pk)
        serializer = RoleSerializer(role, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_role = services.update_role(role, serializer.validated_data)
        return Response(RoleSerializer(updated_role).data)

    def destroy(self, request, pk=None):
        role = get_object_or_404(Role, pk=pk)
        services.delete_role(role)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# SYSTEM USER VIEWSET
# ===========================================================================

class SystemUserViewSet(viewsets.ViewSet):
    """
    API endpoint that allows System Users to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        users = services.get_all_system_users()
        serializer = SystemUserListSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(SystemUser, pk=pk)
        serializer = SystemUserListSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        serializer = SystemUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.create_system_user(serializer.validated_data)
        return Response(SystemUserListSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = get_object_or_404(SystemUser, pk=pk)
        serializer = SystemUserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_user = services.update_system_user(user, serializer.validated_data)
        return Response(SystemUserListSerializer(updated_user).data)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(SystemUser, pk=pk)
        serializer = SystemUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = services.update_system_user(user, serializer.validated_data)
        return Response(SystemUserListSerializer(updated_user).data)

    def destroy(self, request, pk=None):
        user = get_object_or_404(SystemUser, pk=pk)
        services.deactivate_system_user(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# APPROVAL WORKFLOW VIEWSET
# ===========================================================================

class ApprovalWorkflowViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Approval Workflows to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        workflows = services.get_all_workflows()
        serializer = ApprovalWorkflowSerializer(workflows, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        workflow = get_object_or_404(ApprovalWorkflow, pk=pk)
        serializer = ApprovalWorkflowSerializer(workflow)
        return Response(serializer.data)

    def create(self, request):
        serializer = ApprovalWorkflowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workflow = services.create_workflow(serializer.validated_data)
        return Response(ApprovalWorkflowSerializer(workflow).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        workflow = get_object_or_404(ApprovalWorkflow, pk=pk)
        serializer = ApprovalWorkflowSerializer(workflow, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_workflow = services.update_workflow(workflow, serializer.validated_data)
        return Response(ApprovalWorkflowSerializer(updated_workflow).data)

    def partial_update(self, request, pk=None):
        workflow = get_object_or_404(ApprovalWorkflow, pk=pk)
        serializer = ApprovalWorkflowSerializer(workflow, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_workflow = services.update_workflow(workflow, serializer.validated_data)
        return Response(ApprovalWorkflowSerializer(updated_workflow).data)

    def destroy(self, request, pk=None):
        workflow = get_object_or_404(ApprovalWorkflow, pk=pk)
        services.delete_workflow(workflow)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# DELEGATION VIEWSET
# ===========================================================================

class DelegationViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Delegations to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        delegations = services.get_all_delegations()
        serializer = DelegationSerializer(delegations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        delegation = get_object_or_404(Delegation, pk=pk)
        serializer = DelegationSerializer(delegation)
        return Response(serializer.data)

    def create(self, request):
        serializer = DelegationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delegation = services.create_delegation(serializer.validated_data)
        return Response(DelegationSerializer(delegation).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        delegation = get_object_or_404(Delegation, pk=pk)
        serializer = DelegationSerializer(delegation, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_delegation = services.update_delegation(delegation, serializer.validated_data)
        return Response(DelegationSerializer(updated_delegation).data)

    def partial_update(self, request, pk=None):
        delegation = get_object_or_404(Delegation, pk=pk)
        serializer = DelegationSerializer(delegation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_delegation = services.update_delegation(delegation, serializer.validated_data)
        return Response(DelegationSerializer(updated_delegation).data)

    def destroy(self, request, pk=None):
        delegation = get_object_or_404(Delegation, pk=pk)
        services.delete_delegation(delegation)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# LOGIN EVENT VIEWSET
# ===========================================================================

class LoginEventViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Login Events to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        events = services.get_all_login_events()
        serializer = LoginEventSerializer(events, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        event = get_object_or_404(LoginEvent, pk=pk)
        serializer = LoginEventSerializer(event)
        return Response(serializer.data)

    def create(self, request):
        serializer = LoginEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = services.create_login_event(serializer.validated_data)
        return Response(LoginEventSerializer(event).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        event = get_object_or_404(LoginEvent, pk=pk)
        services.delete_login_event(event)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# DEVICE SESSION VIEWSET
# ===========================================================================

class DeviceSessionViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Device Sessions to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        sessions = services.get_all_device_sessions()
        serializer = DeviceSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        session = get_object_or_404(DeviceSession, pk=pk)
        serializer = DeviceSessionSerializer(session)
        return Response(serializer.data)

    def create(self, request):
        serializer = DeviceSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = services.create_device_session(serializer.validated_data)
        return Response(DeviceSessionSerializer(session).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        session = get_object_or_404(DeviceSession, pk=pk)
        serializer = DeviceSessionSerializer(session, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_session = services.update_device_session(session, serializer.validated_data)
        return Response(DeviceSessionSerializer(updated_session).data)

    def partial_update(self, request, pk=None):
        session = get_object_or_404(DeviceSession, pk=pk)
        serializer = DeviceSessionSerializer(session, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_session = services.update_device_session(session, serializer.validated_data)
        return Response(DeviceSessionSerializer(updated_session).data)

    def destroy(self, request, pk=None):
        session = get_object_or_404(DeviceSession, pk=pk)
        services.delete_device_session(session)
        return Response(status=status.HTTP_204_NO_CONTENT)
