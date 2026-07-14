from typing import Dict, Any, List
from .models import (
    Project, Milestone, ProjectTask, Site, SiteVisitor, SiteIncident, SiteProgress,
    Resource, ResourceAllocation, Timesheet, TimesheetEntry,
    ProjectBilling, ProjectBillingInvoice, ProjectCosting, ProjectCostComponent,
)


# ===========================================================================
# PROJECT SERVICES
# ===========================================================================

def get_all_projects() -> List[Project]:
    return Project.objects.filter(is_deleted=False)

def create_project(data: Dict[str, Any]) -> Project:
    code = data.get('code')
    if Project.objects.filter(code__iexact=code).exists():
        raise ValueError(f"Project code '{code}' already exists.")
    return Project.objects.create(**data)

def update_project(project: Project, data: Dict[str, Any]) -> Project:
    code = data.get('code')
    if code and Project.objects.filter(code__iexact=code).exclude(id=project.id).exists():
        raise ValueError(f"Project code '{code}' already exists.")
    for field, value in data.items():
        setattr(project, field, value)
    project.save()
    return project

def delete_project(project: Project) -> None:
    project.is_deleted = True
    project.save()


# ===========================================================================
# MILESTONE SERVICES
# ===========================================================================

def get_all_milestones() -> List[Milestone]:
    return Milestone.objects.filter(is_deleted=False)

def create_milestone(data: Dict[str, Any]) -> Milestone:
    milestone_number = data.get('milestone_number')
    if Milestone.objects.filter(milestone_number__iexact=milestone_number).exists():
        raise ValueError(f"Milestone number '{milestone_number}' already exists.")
    return Milestone.objects.create(**data)

def update_milestone(milestone: Milestone, data: Dict[str, Any]) -> Milestone:
    milestone_number = data.get('milestone_number')
    if milestone_number and Milestone.objects.filter(
        milestone_number__iexact=milestone_number,
    ).exclude(id=milestone.id).exists():
        raise ValueError(f"Milestone number '{milestone_number}' already exists.")
    for field, value in data.items():
        setattr(milestone, field, value)
    milestone.save()
    return milestone

def delete_milestone(milestone: Milestone) -> None:
    milestone.is_deleted = True
    milestone.save()


# ===========================================================================
# PROJECT TASK SERVICES
# ===========================================================================

def get_all_tasks() -> List[ProjectTask]:
    return ProjectTask.objects.filter(is_deleted=False)

def create_task(data: Dict[str, Any]) -> ProjectTask:
    task_number = data.get('task_number')
    if ProjectTask.objects.filter(task_number__iexact=task_number).exists():
        raise ValueError(f"Task number '{task_number}' already exists.")
    return ProjectTask.objects.create(**data)

def update_task(task: ProjectTask, data: Dict[str, Any]) -> ProjectTask:
    task_number = data.get('task_number')
    if task_number and ProjectTask.objects.filter(task_number__iexact=task_number).exclude(id=task.id).exists():
        raise ValueError(f"Task number '{task_number}' already exists.")
    for field, value in data.items():
        setattr(task, field, value)
    task.save()
    return task

def delete_task(task: ProjectTask) -> None:
    task.is_deleted = True
    task.save()


# ===========================================================================
# SITE SERVICES
# ===========================================================================

def get_all_sites() -> List[Site]:
    return Site.objects.filter(is_deleted=False)

def get_site_with_details(site_id: int) -> Site:
    return Site.objects.prefetch_related('visitors', 'incidents', 'progress').get(pk=site_id)

def create_site(data: Dict[str, Any]) -> Site:
    site_code = data.get('site_code')
    if Site.objects.filter(site_code__iexact=site_code).exists():
        raise ValueError(f"Site code '{site_code}' already exists.")
    visitors_data = data.pop('visitors', [])
    incidents_data = data.pop('incidents', [])
    progress_data = data.pop('progress', [])
    site = Site.objects.create(**data)
    for v_data in visitors_data:
        SiteVisitor.objects.create(site=site, **v_data)
    for i_data in incidents_data:
        SiteIncident.objects.create(site=site, **i_data)
    for p_data in progress_data:
        SiteProgress.objects.create(site=site, **p_data)
    return site

def update_site(site: Site, data: Dict[str, Any]) -> Site:
    site_code = data.get('site_code')
    if site_code and Site.objects.filter(site_code__iexact=site_code).exclude(id=site.id).exists():
        raise ValueError(f"Site code '{site_code}' already exists.")
    data.pop('visitors', None)
    data.pop('incidents', None)
    data.pop('progress', None)
    for field, value in data.items():
        setattr(site, field, value)
    site.save()
    return site

def delete_site(site: Site) -> None:
    site.is_deleted = True
    site.save()


# ===========================================================================
# RESOURCE SERVICES
# ===========================================================================

def get_all_resources() -> List[Resource]:
    return Resource.objects.filter(is_deleted=False)

def get_resource_with_allocations(resource_id: int) -> Resource:
    return Resource.objects.prefetch_related('allocations').get(pk=resource_id)

def create_resource(data: Dict[str, Any]) -> Resource:
    resource_number = data.get('resource_number')
    if Resource.objects.filter(resource_number__iexact=resource_number).exists():
        raise ValueError(f"Resource number '{resource_number}' already exists.")
    allocations_data = data.pop('allocations', [])
    resource = Resource.objects.create(**data)
    for alloc_data in allocations_data:
        ResourceAllocation.objects.create(resource=resource, **alloc_data)
    return resource

def update_resource(resource: Resource, data: Dict[str, Any]) -> Resource:
    resource_number = data.get('resource_number')
    if resource_number and Resource.objects.filter(
        resource_number__iexact=resource_number,
    ).exclude(id=resource.id).exists():
        raise ValueError(f"Resource number '{resource_number}' already exists.")
    data.pop('allocations', None)
    for field, value in data.items():
        setattr(resource, field, value)
    resource.save()
    return resource

def delete_resource(resource: Resource) -> None:
    resource.is_deleted = True
    resource.save()


# ===========================================================================
# TIMESHEET SERVICES
# ===========================================================================

def get_all_timesheets() -> List[Timesheet]:
    return Timesheet.objects.filter(is_deleted=False)

def get_timesheet_with_entries(timesheet_id: int) -> Timesheet:
    return Timesheet.objects.prefetch_related('entries').get(pk=timesheet_id)

def create_timesheet(data: Dict[str, Any]) -> Timesheet:
    timesheet_number = data.get('timesheet_number')
    if Timesheet.objects.filter(timesheet_number__iexact=timesheet_number).exists():
        raise ValueError(f"Timesheet number '{timesheet_number}' already exists.")
    entries_data = data.pop('entries', [])
    timesheet = Timesheet.objects.create(**data)
    for entry_data in entries_data:
        TimesheetEntry.objects.create(timesheet=timesheet, **entry_data)
    return timesheet

def update_timesheet(timesheet: Timesheet, data: Dict[str, Any]) -> Timesheet:
    timesheet_number = data.get('timesheet_number')
    if timesheet_number and Timesheet.objects.filter(
        timesheet_number__iexact=timesheet_number,
    ).exclude(id=timesheet.id).exists():
        raise ValueError(f"Timesheet number '{timesheet_number}' already exists.")
    data.pop('entries', None)
    for field, value in data.items():
        setattr(timesheet, field, value)
    timesheet.save()
    return timesheet

def delete_timesheet(timesheet: Timesheet) -> None:
    timesheet.is_deleted = True
    timesheet.save()


# ===========================================================================
# PROJECT BILLING SERVICES
# ===========================================================================

def get_all_billings() -> List[ProjectBilling]:
    return ProjectBilling.objects.filter(is_deleted=False)

def get_billing_with_invoices(billing_id: int) -> ProjectBilling:
    return ProjectBilling.objects.prefetch_related('invoices').get(pk=billing_id)

def create_billing(data: Dict[str, Any]) -> ProjectBilling:
    billing_number = data.get('billing_number')
    if ProjectBilling.objects.filter(billing_number__iexact=billing_number).exists():
        raise ValueError(f"Billing number '{billing_number}' already exists.")
    invoices_data = data.pop('invoices', [])
    billing = ProjectBilling.objects.create(**data)
    for inv_data in invoices_data:
        ProjectBillingInvoice.objects.create(billing=billing, **inv_data)
    return billing

def update_billing(billing: ProjectBilling, data: Dict[str, Any]) -> ProjectBilling:
    billing_number = data.get('billing_number')
    if billing_number and ProjectBilling.objects.filter(
        billing_number__iexact=billing_number,
    ).exclude(id=billing.id).exists():
        raise ValueError(f"Billing number '{billing_number}' already exists.")
    data.pop('invoices', None)
    for field, value in data.items():
        setattr(billing, field, value)
    billing.save()
    return billing

def delete_billing(billing: ProjectBilling) -> None:
    billing.is_deleted = True
    billing.save()


# ===========================================================================
# PROJECT COSTING SERVICES
# ===========================================================================

def get_all_costings() -> List[ProjectCosting]:
    return ProjectCosting.objects.all()

def get_costing_with_components(costing_id: int) -> ProjectCosting:
    return ProjectCosting.objects.prefetch_related('components').get(pk=costing_id)

def create_costing(data: Dict[str, Any]) -> ProjectCosting:
    components_data = data.pop('components', [])
    costing = ProjectCosting.objects.create(**data)
    for comp_data in components_data:
        ProjectCostComponent.objects.create(costing=costing, **comp_data)
    return costing

def update_costing(costing: ProjectCosting, data: Dict[str, Any]) -> ProjectCosting:
    data.pop('components', None)
    for field, value in data.items():
        setattr(costing, field, value)
    costing.save()
    return costing

def delete_costing(costing: ProjectCosting) -> None:
    costing.delete()
