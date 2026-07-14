from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import (
    Project, Milestone, ProjectTask, Site, Resource, Timesheet, ProjectBilling, ProjectCosting,
)
from .serializers import (
    ProjectSerializer, MilestoneSerializer, ProjectTaskSerializer, SiteSerializer,
    ResourceSerializer, TimesheetSerializer, ProjectBillingSerializer, ProjectCostingSerializer,
)
from . import services


# ===========================================================================
# PROJECT VIEWSET
# ===========================================================================

class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        projects = services.get_all_projects()
        return Response(ProjectSerializer(projects, many=True).data)

    def retrieve(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        return Response(ProjectSerializer(project).data)

    def create(self, request):
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_project(serializer.validated_data)
            return Response({"message": "Project created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_project(project, serializer.validated_data)
            return Response({"message": "Project updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_project(project, serializer.validated_data)
            return Response({"message": "Project updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        services.delete_project(project)
        return Response({"message": "Project deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# MILESTONE VIEWSET
# ===========================================================================

class MilestoneViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        milestones = services.get_all_milestones()
        return Response(MilestoneSerializer(milestones, many=True).data)

    def retrieve(self, request, pk=None):
        milestone = get_object_or_404(Milestone, pk=pk)
        return Response(MilestoneSerializer(milestone).data)

    def create(self, request):
        serializer = MilestoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_milestone(serializer.validated_data)
            return Response({"message": "Milestone created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        milestone = get_object_or_404(Milestone, pk=pk)
        serializer = MilestoneSerializer(milestone, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_milestone(milestone, serializer.validated_data)
            return Response({"message": "Milestone updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        milestone = get_object_or_404(Milestone, pk=pk)
        serializer = MilestoneSerializer(milestone, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_milestone(milestone, serializer.validated_data)
            return Response({"message": "Milestone updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        milestone = get_object_or_404(Milestone, pk=pk)
        services.delete_milestone(milestone)
        return Response({"message": "Milestone deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PROJECT TASK VIEWSET
# ===========================================================================

class ProjectTaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        tasks = services.get_all_tasks()
        return Response(ProjectTaskSerializer(tasks, many=True).data)

    def retrieve(self, request, pk=None):
        task = get_object_or_404(ProjectTask, pk=pk)
        return Response(ProjectTaskSerializer(task).data)

    def create(self, request):
        serializer = ProjectTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_task(serializer.validated_data)
            return Response({"message": "Task created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        task = get_object_or_404(ProjectTask, pk=pk)
        serializer = ProjectTaskSerializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_task(task, serializer.validated_data)
            return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        task = get_object_or_404(ProjectTask, pk=pk)
        serializer = ProjectTaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_task(task, serializer.validated_data)
            return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        task = get_object_or_404(ProjectTask, pk=pk)
        services.delete_task(task)
        return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SITE VIEWSET
# ===========================================================================

class SiteViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        sites = services.get_all_sites()
        return Response(SiteSerializer(sites, many=True).data)

    def retrieve(self, request, pk=None):
        site = services.get_site_with_details(pk)
        return Response(SiteSerializer(site).data)

    def create(self, request):
        serializer = SiteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_site(serializer.validated_data)
            return Response({"message": "Site created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        site = get_object_or_404(Site, pk=pk)
        serializer = SiteSerializer(site, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_site(site, serializer.validated_data)
            return Response({"message": "Site updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        site = get_object_or_404(Site, pk=pk)
        serializer = SiteSerializer(site, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_site(site, serializer.validated_data)
            return Response({"message": "Site updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        site = get_object_or_404(Site, pk=pk)
        services.delete_site(site)
        return Response({"message": "Site deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# RESOURCE VIEWSET
# ===========================================================================

class ResourceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        resources = services.get_all_resources()
        return Response(ResourceSerializer(resources, many=True).data)

    def retrieve(self, request, pk=None):
        resource = services.get_resource_with_allocations(pk)
        return Response(ResourceSerializer(resource).data)

    def create(self, request):
        serializer = ResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_resource(serializer.validated_data)
            return Response({"message": "Resource created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        resource = get_object_or_404(Resource, pk=pk)
        serializer = ResourceSerializer(resource, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_resource(resource, serializer.validated_data)
            return Response({"message": "Resource updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        resource = get_object_or_404(Resource, pk=pk)
        serializer = ResourceSerializer(resource, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_resource(resource, serializer.validated_data)
            return Response({"message": "Resource updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        resource = get_object_or_404(Resource, pk=pk)
        services.delete_resource(resource)
        return Response({"message": "Resource deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TIMESHEET VIEWSET
# ===========================================================================

class TimesheetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        timesheets = services.get_all_timesheets()
        return Response(TimesheetSerializer(timesheets, many=True).data)

    def retrieve(self, request, pk=None):
        timesheet = services.get_timesheet_with_entries(pk)
        return Response(TimesheetSerializer(timesheet).data)

    def create(self, request):
        serializer = TimesheetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_timesheet(serializer.validated_data)
            return Response({"message": "Timesheet created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        timesheet = get_object_or_404(Timesheet, pk=pk)
        serializer = TimesheetSerializer(timesheet, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_timesheet(timesheet, serializer.validated_data)
            return Response({"message": "Timesheet updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        timesheet = get_object_or_404(Timesheet, pk=pk)
        serializer = TimesheetSerializer(timesheet, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_timesheet(timesheet, serializer.validated_data)
            return Response({"message": "Timesheet updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        timesheet = get_object_or_404(Timesheet, pk=pk)
        services.delete_timesheet(timesheet)
        return Response({"message": "Timesheet deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PROJECT BILLING VIEWSET
# ===========================================================================

class ProjectBillingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        billings = services.get_all_billings()
        return Response(ProjectBillingSerializer(billings, many=True).data)

    def retrieve(self, request, pk=None):
        billing = services.get_billing_with_invoices(pk)
        return Response(ProjectBillingSerializer(billing).data)

    def create(self, request):
        serializer = ProjectBillingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_billing(serializer.validated_data)
            return Response({"message": "Project billing created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        billing = get_object_or_404(ProjectBilling, pk=pk)
        serializer = ProjectBillingSerializer(billing, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_billing(billing, serializer.validated_data)
            return Response({"message": "Project billing updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        billing = get_object_or_404(ProjectBilling, pk=pk)
        serializer = ProjectBillingSerializer(billing, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_billing(billing, serializer.validated_data)
            return Response({"message": "Project billing updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        billing = get_object_or_404(ProjectBilling, pk=pk)
        services.delete_billing(billing)
        return Response({"message": "Project billing deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PROJECT COSTING VIEWSET
# ===========================================================================

class ProjectCostingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        costings = services.get_all_costings()
        return Response(ProjectCostingSerializer(costings, many=True).data)

    def retrieve(self, request, pk=None):
        costing = services.get_costing_with_components(pk)
        return Response(ProjectCostingSerializer(costing).data)

    def create(self, request):
        serializer = ProjectCostingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_costing(serializer.validated_data)
            return Response({"message": "Project costing created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        costing = get_object_or_404(ProjectCosting, pk=pk)
        serializer = ProjectCostingSerializer(costing, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_costing(costing, serializer.validated_data)
            return Response({"message": "Project costing updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        costing = get_object_or_404(ProjectCosting, pk=pk)
        serializer = ProjectCostingSerializer(costing, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_costing(costing, serializer.validated_data)
            return Response({"message": "Project costing updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        costing = get_object_or_404(ProjectCosting, pk=pk)
        services.delete_costing(costing)
        return Response({"message": "Project costing deleted successfully."}, status=status.HTTP_200_OK)
