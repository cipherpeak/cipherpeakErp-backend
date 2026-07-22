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
        from collections import defaultdict
        from .models import ApprovalWorkflow
        
        all_records = ApprovalWorkflow.objects.all().order_by('module', 'step_order')
        grouped = defaultdict(list)
        for rec in all_records:
            grouped[rec.module].append(rec)
            
        data = []
        for module, recs in grouped.items():
            first_rec = recs[0]
            name = f"{module} Flow" if "Management" in module or "Permissions" in module else f"{module} Approval"
            is_active = any(r.status == 'active' for r in recs)
            
            levels = []
            for r in recs:
                levels.append({
                    "step": r.step_order,
                    "approver_role": r.approver_role or "Manager",
                    "label": f"{r.approver_role or 'Manager'} Approval"
                })
                
            data.append({
                "id": first_rec.id,
                "name": name,
                "module": module,
                "description": f"Approval workflow steps for {module} module.",
                "is_active": is_active,
                "levels": levels
            })
        return Response(data)

    def retrieve(self, request, pk=None):
        from .models import ApprovalWorkflow
        first_rec = get_object_or_404(ApprovalWorkflow, pk=pk)
        module = first_rec.module
        recs = ApprovalWorkflow.objects.filter(module=module).order_by('step_order')
        
        name = f"{module} Flow" if "Management" in module or "Permissions" in module else f"{module} Approval"
        is_active = any(r.status == 'active' for r in recs)
        
        levels = []
        for r in recs:
            levels.append({
                "step": r.step_order,
                "approver_role": r.approver_role or "Manager",
                "label": f"{r.approver_role or 'Manager'} Approval"
            })
            
        data = {
            "id": first_rec.id,
            "name": name,
            "module": module,
            "description": f"Approval workflow steps for {module} module.",
            "is_active": is_active,
            "levels": levels
        }
        return Response(data)

    def create(self, request):
        from .models import ApprovalWorkflow
        from django.db import transaction
        
        payload = request.data
        module = payload.get("module")
        levels = payload.get("levels", [])
        is_active = payload.get("is_active", True)
        
        if not module:
            return Response({"module": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
            
        with transaction.atomic():
            # Delete any existing workflow steps for this module
            ApprovalWorkflow.objects.filter(module=module).delete()
            
            created_recs = []
            for lvl in levels:
                rec = ApprovalWorkflow.objects.create(
                    module=module,
                    step_order=lvl.get("step", 1),
                    approver_role=lvl.get("approver_role", "Manager"),
                    status="active" if is_active else "inactive",
                    threshold=None,
                    auto_approve_under=None
                )
                created_recs.append(rec)
                
        if not created_recs:
            return Response({"error": "No levels provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        first_rec = created_recs[0]
        name = f"{module} Flow" if "Management" in module or "Permissions" in module else f"{module} Approval"
        return Response({
            "id": first_rec.id,
            "name": name,
            "module": module,
            "description": f"Approval workflow steps for {module} module.",
            "is_active": is_active,
            "levels": levels
        }, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        from .models import ApprovalWorkflow
        from django.db import transaction
        
        target_rec = get_object_or_404(ApprovalWorkflow, pk=pk)
        target_module = target_rec.module
        
        payload = request.data
        
        # If payload specifies is_active only (toggle active):
        if "is_active" in payload and len(payload) == 1:
            is_active = payload.get("is_active")
            recs = ApprovalWorkflow.objects.filter(module=target_module)
            for r in recs:
                r.status = "active" if is_active else "inactive"
                r.save()
                
            levels = [{
                "step": r.step_order,
                "approver_role": r.approver_role or "Manager",
                "label": f"{r.approver_role or 'Manager'} Approval"
            } for r in recs.order_by('step_order')]
            
            name = f"{target_module} Flow" if "Management" in target_module or "Permissions" in target_module else f"{target_module} Approval"
            return Response({
                "id": target_rec.id,
                "name": name,
                "module": target_module,
                "description": f"Approval workflow steps for {target_module} module.",
                "is_active": is_active,
                "levels": levels
            })
            
        module = payload.get("module", target_module)
        levels = payload.get("levels", [])
        is_active = payload.get("is_active", True)
        
        with transaction.atomic():
            # Delete old records for the target module (and the new one if renamed)
            ApprovalWorkflow.objects.filter(module=target_module).delete()
            if module != target_module:
                ApprovalWorkflow.objects.filter(module=module).delete()
                
            created_recs = []
            for lvl in levels:
                rec = ApprovalWorkflow.objects.create(
                    module=module,
                    step_order=lvl.get("step", 1),
                    approver_role=lvl.get("approver_role", "Manager"),
                    status="active" if is_active else "inactive",
                    threshold=None,
                    auto_approve_under=None
                )
                created_recs.append(rec)
                
        if not created_recs:
            return Response({"error": "No levels provided"}, status=status.HTTP_400_BAD_REQUEST)
            
        first_rec = created_recs[0]
        name = f"{module} Flow" if "Management" in module or "Permissions" in module else f"{module} Approval"
        return Response({
            "id": first_rec.id,
            "name": name,
            "module": module,
            "description": f"Approval workflow steps for {module} module.",
            "is_active": is_active,
            "levels": levels
        })

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        from .models import ApprovalWorkflow
        workflow = get_object_or_404(ApprovalWorkflow, pk=pk)
        ApprovalWorkflow.objects.filter(module=workflow.module).delete()
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
        # Use serializer.save() so the serializer's create() resolves the
        # delegator/delegate names into from_user/to_user. Calling the service
        # directly with validated_data would omit those FKs and raise a
        # NOT NULL IntegrityError (500).
        delegation = serializer.save()
        return Response(DelegationSerializer(delegation).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        delegation = get_object_or_404(Delegation, pk=pk)
        serializer = DelegationSerializer(delegation, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_delegation = serializer.save()
        return Response(DelegationSerializer(updated_delegation).data)

    def partial_update(self, request, pk=None):
        delegation = get_object_or_404(Delegation, pk=pk)
        serializer = DelegationSerializer(delegation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_delegation = serializer.save()
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
