from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Company, Branch, Plant, Department, Designation, Team, Shift, CostCenter
from .serializers import (
    CompanySerializer, BranchSerializer, PlantSerializer, DepartmentSerializer,
    DesignationSerializer, TeamSerializer, ShiftSerializer, CostCenterSerializer,
    OrgChartCompanySerializer, OrgChartBranchSerializer, OrgChartDepartmentSerializer, OrgChartTeamSerializer,
)
from . import services


# ===========================================================================
# COMPANY VIEWSET
# ===========================================================================

class CompanyViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Companies to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        companies = services.get_all_companies()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_company(serializer.validated_data)
            return Response({"message": "Company created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_company(company, serializer.validated_data)
            return Response({"message": "Company updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_company(company, serializer.validated_data)
            return Response({"message": "Company updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk)
        services.deactivate_company(company)
        return Response({"message": "Company deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# BRANCH VIEWSET
# ===========================================================================

class BranchViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Branches to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        company_id = request.query_params.get('company')
        if company_id:
            branches = Branch.objects.filter(company_id=company_id)
        else:
            branches = services.get_all_branches()
        serializer = BranchSerializer(branches, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = BranchSerializer(branch)
        return Response(serializer.data)

    def create(self, request):
        serializer = BranchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_branch(serializer.validated_data)
            return Response({"message": "Branch created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = BranchSerializer(branch, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_branch(branch, serializer.validated_data)
            return Response({"message": "Branch updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        branch = get_object_or_404(Branch, pk=pk)
        serializer = BranchSerializer(branch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_branch(branch, serializer.validated_data)
            return Response({"message": "Branch updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        branch = get_object_or_404(Branch, pk=pk)
        services.deactivate_branch(branch)
        return Response({"message": "Branch deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# PLANT VIEWSET
# ===========================================================================

class PlantViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Plants to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        plants = services.get_all_plants()
        serializer = PlantSerializer(plants, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        plant = get_object_or_404(Plant, pk=pk)
        serializer = PlantSerializer(plant)
        return Response(serializer.data)

    def create(self, request):
        serializer = PlantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_plant(serializer.validated_data)
            return Response({"message": "Plant created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        plant = get_object_or_404(Plant, pk=pk)
        serializer = PlantSerializer(plant, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_plant(plant, serializer.validated_data)
            return Response({"message": "Plant updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        plant = get_object_or_404(Plant, pk=pk)
        serializer = PlantSerializer(plant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_plant(plant, serializer.validated_data)
            return Response({"message": "Plant updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        plant = get_object_or_404(Plant, pk=pk)
        services.deactivate_plant(plant)
        return Response({"message": "Plant deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# DEPARTMENT VIEWSET
# ===========================================================================

class DepartmentViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Departments to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        departments = services.get_all_departments()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def create(self, request):
        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_department(serializer.validated_data)
            return Response({"message": "Department created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_department(department, serializer.validated_data)
            return Response({"message": "Department updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_department(department, serializer.validated_data)
            return Response({"message": "Department updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        department = get_object_or_404(Department, pk=pk)
        services.deactivate_department(department)
        return Response({"message": "Department deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# DESIGNATION VIEWSET
# ===========================================================================

class DesignationViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Designations to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        designations = services.get_all_designations()
        serializer = DesignationSerializer(designations, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        designation = get_object_or_404(Designation, pk=pk)
        serializer = DesignationSerializer(designation)
        return Response(serializer.data)

    def create(self, request):
        serializer = DesignationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_designation(serializer.validated_data)
            return Response({"message": "Designation created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        designation = get_object_or_404(Designation, pk=pk)
        serializer = DesignationSerializer(designation, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_designation(designation, serializer.validated_data)
            return Response({"message": "Designation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        designation = get_object_or_404(Designation, pk=pk)
        serializer = DesignationSerializer(designation, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_designation(designation, serializer.validated_data)
            return Response({"message": "Designation updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        designation = get_object_or_404(Designation, pk=pk)
        services.delete_designation(designation)
        return Response({"message": "Designation deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# TEAM VIEWSET
# ===========================================================================

class TeamViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Teams to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        teams = services.get_all_teams()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def create(self, request):
        serializer = TeamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_team(serializer.validated_data)
            return Response({"message": "Team created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_team(team, serializer.validated_data)
            return Response({"message": "Team updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        serializer = TeamSerializer(team, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_team(team, serializer.validated_data)
            return Response({"message": "Team updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        team = get_object_or_404(Team, pk=pk)
        services.delete_team(team)
        return Response({"message": "Team deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# SHIFT VIEWSET
# ===========================================================================

class ShiftViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Shifts to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        shifts = services.get_all_shifts()
        serializer = ShiftSerializer(shifts, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        shift = get_object_or_404(Shift, pk=pk)
        serializer = ShiftSerializer(shift)
        return Response(serializer.data)

    def create(self, request):
        serializer = ShiftSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_shift(serializer.validated_data)
            return Response({"message": "Shift created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        shift = get_object_or_404(Shift, pk=pk)
        serializer = ShiftSerializer(shift, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_shift(shift, serializer.validated_data)
            return Response({"message": "Shift updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        shift = get_object_or_404(Shift, pk=pk)
        serializer = ShiftSerializer(shift, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_shift(shift, serializer.validated_data)
            return Response({"message": "Shift updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        shift = get_object_or_404(Shift, pk=pk)
        services.delete_shift(shift)
        return Response({"message": "Shift deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# COST CENTER VIEWSET
# ===========================================================================

class CostCenterViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Cost Centers to be viewed or edited.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cost_centers = services.get_all_cost_centers()
        serializer = CostCenterSerializer(cost_centers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        cost_center = get_object_or_404(CostCenter, pk=pk)
        serializer = CostCenterSerializer(cost_center)
        return Response(serializer.data)

    def create(self, request):
        serializer = CostCenterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.create_cost_center(serializer.validated_data)
            return Response({"message": "Cost center created successfully."}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        cost_center = get_object_or_404(CostCenter, pk=pk)
        serializer = CostCenterSerializer(cost_center, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_cost_center(cost_center, serializer.validated_data)
            return Response({"message": "Cost center updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        cost_center = get_object_or_404(CostCenter, pk=pk)
        serializer = CostCenterSerializer(cost_center, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            services.update_cost_center(cost_center, serializer.validated_data)
            return Response({"message": "Cost center updated successfully."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cost_center = get_object_or_404(CostCenter, pk=pk)
        services.delete_cost_center(cost_center)
        return Response({"message": "Cost center deleted successfully."}, status=status.HTTP_200_OK)


# ===========================================================================
# ORG CHART VIEWSET
# ===========================================================================

class OrgChartViewSet(viewsets.ViewSet):
    """
    API endpoint for Org Chart hierarchy.
    - list: Full tree (companies → branches → departments → teams)
    - retrieve: Children of a specific node
    """
    permission_classes = [IsAuthenticated]

    def list(self, request):
        companies = services.get_org_chart()
        serializer = OrgChartCompanySerializer(companies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        node_type = request.query_params.get('type', 'company')

        if node_type == 'company':
            branches = services.get_company_children(int(pk))
            serializer = OrgChartBranchSerializer(branches, many=True)
        elif node_type == 'branch':
            departments = services.get_branch_children(int(pk))
            serializer = OrgChartDepartmentSerializer(departments, many=True)
        elif node_type == 'department':
            department = Department.objects.get(pk=pk)
            teams = services.get_department_children(department.name)
            serializer = OrgChartTeamSerializer(teams, many=True)
        else:
            return Response({"error": "Invalid type. Use: company, branch, or department"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)
