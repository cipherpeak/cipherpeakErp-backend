from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class ActiveInactive(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class PriorityLevel(models.TextChoices):
    LOW = 'low', 'Low'
    NORMAL = 'normal', 'Normal'
    HIGH = 'high', 'High'
    URGENT = 'urgent', 'Urgent'


class CurrencyCode(models.TextChoices):
    AED = 'AED', 'AED'
    USD = 'USD', 'USD'
    EUR = 'EUR', 'EUR'
    GBP = 'GBP', 'GBP'
    INR = 'INR', 'INR'
    SAR = 'SAR', 'SAR'


class AccountType(models.TextChoices):
    PROSPECT = 'prospect', 'Prospect'
    CUSTOMER = 'customer', 'Customer'
    PARTNER = 'partner', 'Partner'
    COMPETITOR = 'competitor', 'Competitor'


class LeadStatus(models.TextChoices):
    NEW = 'new', 'New'
    CONTACTED = 'contacted', 'Contacted'
    QUALIFIED = 'qualified', 'Qualified'
    PROPOSAL_SENT = 'proposal_sent', 'Proposal Sent'
    WON = 'won', 'Won'
    LOST = 'lost', 'Lost'


class LeadSource(models.TextChoices):
    WEBSITE = 'website', 'Website'
    REFERRAL = 'referral', 'Referral'
    LINKEDIN = 'linkedin', 'LinkedIn'
    COLD_CALL = 'cold_call', 'Cold Call'
    EXHIBITION = 'exhibition', 'Exhibition'
    EMAIL_CAMPAIGN = 'email_campaign', 'Email Campaign'
    EVENT = 'event', 'Event'
    OTHER = 'other', 'Other'


class OppStage(models.TextChoices):
    PROSPECTING = 'prospecting', 'Prospecting'
    QUALIFICATION = 'qualification', 'Qualification'
    PROPOSAL = 'proposal', 'Proposal'
    NEGOTIATION = 'negotiation', 'Negotiation'
    WON = 'won', 'Won'
    LOST = 'lost', 'Lost'


class CRMActivityType(models.TextChoices):
    CALL = 'call', 'Call'
    EMAIL = 'email', 'Email'
    MEETING = 'meeting', 'Meeting'
    TASK = 'task', 'Task'
    NOTE = 'note', 'Note'
    WHATSAPP = 'whatsapp', 'WhatsApp'


class CRMActivityStatus(models.TextChoices):
    PLANNED = 'planned', 'Planned'
    DONE = 'done', 'Done'
    CANCELLED = 'cancelled', 'Cancelled'
    OVERDUE = 'overdue', 'Overdue'


class CRMRelatedTo(models.TextChoices):
    LEAD = 'lead', 'Lead'
    CONTACT = 'contact', 'Contact'
    ACCOUNT = 'account', 'Account'
    OPPORTUNITY = 'opportunity', 'Opportunity'


class CRMQuoteStatus(models.TextChoices):
    DRAFT = 'draft', 'Draft'
    SENT = 'sent', 'Sent'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
    EXPIRED = 'expired', 'Expired'


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------

class Account(models.Model):
    account_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.PROSPECT,
    )
    website = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    trn = models.CharField(max_length=30, blank=True, null=True)
    annual_revenue = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    employees = models.IntegerField(default=0)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='crm_accounts',
    )
    status = models.CharField(
        max_length=20,
        choices=ActiveInactive.choices,
        default=ActiveInactive.ACTIVE,
    )
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['name']

    def __str__(self):
        return f"{self.account_number} - {self.name}"


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

class Contact(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, blank=True, null=True, related_name='contacts',
    )
    account_name = models.CharField(max_length=200, blank=True, null=True)
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=120, blank=True, null=True)
    department = models.CharField(max_length=120, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    mobile = models.CharField(max_length=40, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=ActiveInactive.choices,
        default=ActiveInactive.ACTIVE,
    )
    tags = models.JSONField(default=list, blank=True)
    last_activity_type = models.CharField(max_length=50, blank=True, null=True)
    last_activity = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.account and not self.account_name:
            self.account_name = self.account.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# Lead
# ---------------------------------------------------------------------------

class Lead(models.Model):
    lead_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True, null=True)
    source = models.CharField(max_length=20, choices=LeadSource.choices, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
    )
    priority = models.CharField(
        max_length=20,
        choices=PriorityLevel.choices,
        default=PriorityLevel.NORMAL,
    )
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='crm_leads',
    )
    score = models.SmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    estimated_value = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tags = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.lead_number} - {self.name}"


# ---------------------------------------------------------------------------
# Opportunity
# ---------------------------------------------------------------------------

class Opportunity(models.Model):
    opp_number = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=200)
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, blank=True, null=True, related_name='opportunities',
    )
    account_name = models.CharField(max_length=200, blank=True, null=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, blank=True, null=True, related_name='opportunities',
    )
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    stage = models.CharField(
        max_length=20,
        choices=OppStage.choices,
        default=OppStage.PROSPECTING,
    )
    priority = models.CharField(
        max_length=20,
        choices=PriorityLevel.choices,
        default=PriorityLevel.NORMAL,
    )
    value = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    probability = models.SmallIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    expected_close = models.DateField(blank=True, null=True)
    source = models.CharField(max_length=60, blank=True, null=True)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='crm_opportunities',
    )
    next_step = models.CharField(max_length=300, blank=True, null=True)
    lost_reason = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Opportunity'
        verbose_name_plural = 'Opportunities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.opp_number} - {self.name}"

    def save(self, *args, **kwargs):
        if self.account and not self.account_name:
            self.account_name = self.account.name
        if self.contact and not self.contact_name:
            self.contact_name = self.contact.name
        super().save(*args, **kwargs)


# ---------------------------------------------------------------------------
# CRM Activity (polymorphic — related_to + related_id)
# ---------------------------------------------------------------------------

class CRMActivity(models.Model):
    type = models.CharField(max_length=20, choices=CRMActivityType.choices)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CRMActivityStatus.choices,
        default=CRMActivityStatus.PLANNED,
    )
    related_to = models.CharField(max_length=20, choices=CRMRelatedTo.choices)
    related_id = models.IntegerField(help_text='ID of the related lead/contact/account/opportunity')
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='crm_activities',
    )
    due_date = models.DateTimeField(blank=True, null=True)
    done_date = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'CRM Activity'
        verbose_name_plural = 'CRM Activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} - {self.subject}"


# ---------------------------------------------------------------------------
# CRM Quotation
# ---------------------------------------------------------------------------

class CRMQuotation(models.Model):
    quotation_number = models.CharField(max_length=40, unique=True)
    opportunity = models.ForeignKey(
        Opportunity, on_delete=models.SET_NULL, blank=True, null=True, related_name='quotations',
    )
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, blank=True, null=True, related_name='quotations',
    )
    account_name = models.CharField(max_length=200, blank=True, null=True)
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, blank=True, null=True, related_name='quotations',
    )
    contact_name = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=CRMQuoteStatus.choices,
        default=CRMQuoteStatus.DRAFT,
    )
    issue_date = models.DateField(blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    currency = models.CharField(max_length=10, choices=CurrencyCode.choices, default=CurrencyCode.AED)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    payment_terms = models.CharField(max_length=60, blank=True, null=True)
    assigned_to = models.ForeignKey(
        'hr.Employee', on_delete=models.SET_NULL, blank=True, null=True, related_name='crm_quotations',
    )
    notes = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'CRM Quotation'
        verbose_name_plural = 'CRM Quotations'
        ordering = ['-created_at']

    def __str__(self):
        return self.quotation_number

    def save(self, *args, **kwargs):
        if self.account and not self.account_name:
            self.account_name = self.account.name
        if self.contact and not self.contact_name:
            self.contact_name = self.contact.name
        super().save(*args, **kwargs)


class CRMQuotationLine(models.Model):
    quotation = models.ForeignKey(CRMQuotation, on_delete=models.CASCADE, related_name='lines')
    item_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    qty = models.DecimalField(max_digits=14, decimal_places=3)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        verbose_name = 'CRM Quotation Line'
        verbose_name_plural = 'CRM Quotation Lines'

    def __str__(self):
        return f"{self.quotation.quotation_number} - {self.item_name}"
