from rest_framework import serializers
from .models import (
    Project, Milestone, ProjectTask, Site, SiteVisitor, SiteIncident, SiteProgress,
    Resource, ResourceAllocation, Timesheet, TimesheetEntry,
    ProjectBilling, ProjectBillingInvoice, ProjectCosting, ProjectCostComponent,
)


# ===========================================================================
# PROJECT SERIALIZER
# ===========================================================================

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


# ===========================================================================
# MILESTONE SERIALIZER
# ===========================================================================

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'


# ===========================================================================
# PROJECT TASK SERIALIZER
# ===========================================================================

class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = '__all__'


# ===========================================================================
# SITE SERIALIZERS
# ===========================================================================

class SiteVisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteVisitor
        fields = '__all__'
        extra_kwargs = {'site': {'required': False}}


class SiteIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteIncident
        fields = '__all__'
        extra_kwargs = {'site': {'required': False}}


class SiteProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteProgress
        fields = '__all__'
        extra_kwargs = {'site': {'required': False}}


class SiteSerializer(serializers.ModelSerializer):
    visitors = SiteVisitorSerializer(many=True, required=False)
    incidents = SiteIncidentSerializer(many=True, required=False)
    progress = SiteProgressSerializer(many=True, required=False)

    class Meta:
        model = Site
        fields = '__all__'


# ===========================================================================
# RESOURCE SERIALIZERS
# ===========================================================================

class ResourceAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceAllocation
        fields = '__all__'
        extra_kwargs = {'resource': {'required': False}}


class ResourceSerializer(serializers.ModelSerializer):
    allocations = ResourceAllocationSerializer(many=True, required=False)

    class Meta:
        model = Resource
        fields = '__all__'


# ===========================================================================
# TIMESHEET SERIALIZERS
# ===========================================================================

class TimesheetEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimesheetEntry
        fields = '__all__'
        extra_kwargs = {'timesheet': {'required': False}}


class TimesheetSerializer(serializers.ModelSerializer):
    entries = TimesheetEntrySerializer(many=True, required=False)

    class Meta:
        model = Timesheet
        fields = '__all__'


# ===========================================================================
# PROJECT BILLING SERIALIZERS
# ===========================================================================

class ProjectBillingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectBillingInvoice
        fields = '__all__'
        extra_kwargs = {'billing': {'required': False}}


class ProjectBillingSerializer(serializers.ModelSerializer):
    invoices = ProjectBillingInvoiceSerializer(many=True, required=False)

    class Meta:
        model = ProjectBilling
        fields = '__all__'


# ===========================================================================
# PROJECT COSTING SERIALIZERS
# ===========================================================================

class ProjectCostComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCostComponent
        fields = '__all__'
        extra_kwargs = {'costing': {'required': False}}


class ProjectCostingSerializer(serializers.ModelSerializer):
    components = ProjectCostComponentSerializer(many=True, required=False)

    class Meta:
        model = ProjectCosting
        fields = '__all__'
