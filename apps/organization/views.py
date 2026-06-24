from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Company, Branch, Plant, Department
from .serializers import CompanySerializer, BranchSerializer, PlantSerializer, DepartmentSerializer
from . import services

# ===========================================================================
# COMPANY VIEWSET
# ===========================================================================

class CompanyViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Companies to be viewed or edited.
    """
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
        
        company = services.create_company(serializer.validated_data)
        return Response(CompanySerializer(company).data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """Handles full updates (PUT)"""
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_company = services.update_company(company, serializer.validated_data)
        return Response(CompanySerializer(updated_company).data)

    def partial_update(self, request, pk=None):
        """Handles partial updates (PATCH)"""
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_company = services.update_company(company, serializer.validated_data)
        return Response(CompanySerializer(updated_company).data)

    def destroy(self, request, pk=None):
        """Standard DELETE request mapped to a soft-delete."""
        company = get_object_or_404(Company, pk=pk)
        services.deactivate_company(company)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# BRANCH VIEWSET
# ===========================================================================

class BranchViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Branches to be viewed or edited.
    """
    def list(self, request):
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
            branch = services.create_branch(serializer.validated_data)
            return Response(BranchSerializer(branch).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            # Catching the business logic error from our service layer
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handles full updates (PUT)"""
        branch = get_object_or_404(Branch, pk=pk)
        serializer = BranchSerializer(branch, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_branch = services.update_branch(branch, serializer.validated_data)
        return Response(BranchSerializer(updated_branch).data)

    def partial_update(self, request, pk=None):
        """Handles partial updates (PATCH)"""
        branch = get_object_or_404(Branch, pk=pk)
        serializer = BranchSerializer(branch, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_branch = services.update_branch(branch, serializer.validated_data)
        return Response(BranchSerializer(updated_branch).data)

    def destroy(self, request, pk=None):
        """Standard DELETE request mapped to a soft-delete."""
        branch = get_object_or_404(Branch, pk=pk)
        services.deactivate_branch(branch)
        
        # If you prefer a hard delete instead, swap the line above for:
        # services.delete_branch(branch)
        
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# PLANT VIEWSET
# ===========================================================================

class PlantViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Plants to be viewed or edited via services.
    """
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
            plant = services.create_plant(serializer.validated_data)
            return Response(PlantSerializer(plant).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Full update (PUT)"""
        plant = get_object_or_404(Plant, pk=pk)
        serializer = PlantSerializer(plant, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_plant = services.update_plant(plant, serializer.validated_data)
        return Response(PlantSerializer(updated_plant).data)

    def partial_update(self, request, pk=None):
        """Partial update (PATCH)"""
        plant = get_object_or_404(Plant, pk=pk)
        serializer = PlantSerializer(plant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_plant = services.update_plant(plant, serializer.validated_data)
        return Response(PlantSerializer(updated_plant).data)

    def destroy(self, request, pk=None):
        """Standard DELETE request mapped to a soft-delete service."""
        plant = get_object_or_404(Plant, pk=pk)
        services.deactivate_plant(plant)
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===========================================================================
# DEPARTMENT VIEWSET
# ===========================================================================

class DepartmentViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Departments to be viewed or edited via services.
    """
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
            department = services.create_department(serializer.validated_data)
            return Response(DepartmentSerializer(department).data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Full update (PUT)"""
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        updated_dept = services.update_department(department, serializer.validated_data)
        return Response(DepartmentSerializer(updated_dept).data)

    def partial_update(self, request, pk=None):
        """Partial update (PATCH)"""
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        updated_dept = services.update_department(department, serializer.validated_data)
        return Response(DepartmentSerializer(updated_dept).data)

    def destroy(self, request, pk=None):
        """Standard DELETE request mapped to a soft-delete service."""
        department = get_object_or_404(Department, pk=pk)
        services.deactivate_department(department)
        return Response(status=status.HTTP_204_NO_CONTENT)        