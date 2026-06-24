from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from typing import Dict, Any, List
from .models import Company, Branch, CompanyStatus, Plant, Department

# ===========================================================================
# COMPANY SERVICES
# ===========================================================================

def get_all_companies() -> List[Company]:
    return Company.objects.all()

def create_company(data: Dict[str, Any]) -> Company:
    return Company.objects.create(**data)

def update_company(company: Company, data: Dict[str, Any]) -> Company:
    for field, value in data.items():
        setattr(company, field, value)
    company.save()
    return company

def deactivate_company(company: Company) -> Company:
    """Soft deletes the company and cascades deactivation to its branches."""
    with transaction.atomic():
        company.status = CompanyStatus.INACTIVE
        company.save()
        company.branches.update(status=CompanyStatus.INACTIVE)
    return company

def delete_company(company: Company) -> None:
    """Hard deletes the company from the database."""
    company.delete()


# ===========================================================================
# BRANCH SERVICES
# ===========================================================================

def get_all_branches() -> List[Branch]:
    return Branch.objects.all()

def create_branch(data: Dict[str, Any]) -> Branch:
    # Example of potential business logic: 
    # Ensuring a branch isn't added to an INACTIVE company
    company = data.get('company')
    if company and company.status == CompanyStatus.INACTIVE:
        raise ValueError("Cannot add a branch to an inactive company.")
        
    return Branch.objects.create(**data)

def update_branch(branch: Branch, data: Dict[str, Any]) -> Branch:
    for field, value in data.items():
        setattr(branch, field, value)
    branch.save()
    return branch

def deactivate_branch(branch: Branch) -> Branch:
    """Soft deletes the branch."""
    branch.status = CompanyStatus.INACTIVE
    branch.save()
    # You could also cascade this to Plants/Departments here if needed
    return branch

def delete_branch(branch: Branch) -> None:
    """Hard deletes the branch from the database."""
    branch.delete()

# ===========================================================================
# PLANT SERVICES
# ===========================================================================

def get_all_plants() -> List[Plant]:
    """Fetch all plants."""
    return Plant.objects.all()

def create_plant(data: Dict[str, Any]) -> Plant:
    """Business logic for creating a physical facility plant."""
    branch = data.get('branch')
    if branch and branch.status == CompanyStatus.INACTIVE:
        raise ValueError("Cannot create a plant under an inactive branch.")
        
    return Plant.objects.create(**data)

def update_plant(plant: Plant, data: Dict[str, Any]) -> Plant:
    """Business logic for updating a plant."""
    for field, value in data.items():
        setattr(plant, field, value)
    
    # If the branch changed, reset branch_name so the model's save() updates it
    if 'branch' in data:
        plant.branch_name = None
        
    plant.save()
    return plant

def deactivate_plant(plant: Plant) -> Plant:
    """Soft deletes the plant by setting status to INACTIVE."""
    plant.status = CompanyStatus.INACTIVE
    plant.save()
    return plant

def delete_plant(plant: Plant) -> None:
    """Hard deletes the plant from the database."""
    plant.delete()


# ===========================================================================
# DEPARTMENT SERVICES
# ===========================================================================

def get_all_departments() -> List[Department]:
    """Fetch all organizational departments."""
    return Department.objects.all()

def create_department(data: Dict[str, Any]) -> Department:
    """Business logic for creating a department."""
    branch = data.get('branch')
    if branch and branch.status == CompanyStatus.INACTIVE:
        raise ValueError("Cannot assign a department to an inactive branch.")
        
    return Department.objects.create(**data)

def update_department(department: Department, data: Dict[str, Any]) -> Department:
    """Business logic for updating a department."""
    for field, value in data.items():
        setattr(department, field, value)
        
    # If the branch changed, reset branch_name so the model's save() updates it
    if 'branch' in data:
        department.branch_name = None
        
    department.save()
    return department

def deactivate_department(department: Department) -> Department:
    """Soft deletes the department by setting status to INACTIVE."""
    department.status = CompanyStatus.INACTIVE
    department.save()
    return department

def delete_department(department: Department) -> None:
    """Hard deletes the department from the database."""
    department.delete()    