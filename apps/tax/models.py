from django.db import models


# ---------------------------------------------------------------------------
# Choices / Enums
# ---------------------------------------------------------------------------

class TaxStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'


class TaxRateStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    EXPIRED = 'expired', 'Expired'
    SCHEDULED = 'scheduled', 'Scheduled'


class TaxCategoryType(models.TextChoices):
    GOODS = 'goods', 'Goods'
    SERVICES = 'services', 'Services'
    BOTH = 'both', 'Both'


class TaxRuleStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    DRAFT = 'draft', 'Draft'


class TaxJurStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    INACTIVE = 'inactive', 'Inactive'
    PENDING = 'pending', 'Pending'


class FilingFrequency(models.TextChoices):
    MONTHLY = 'monthly', 'Monthly'
    QUARTERLY = 'quarterly', 'Quarterly'
    ANNUALLY = 'annually', 'Annually'


class ExemptionType(models.TextChoices):
    FULL = 'full', 'Full'
    PARTIAL = 'partial', 'Partial'
    CONDITIONAL = 'conditional', 'Conditional'


class ExemptionStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    EXPIRED = 'expired', 'Expired'
    PENDING = 'pending', 'Pending'


class TaxReturnStatus(models.TextChoices):
    FILED = 'filed', 'Filed'
    PENDING = 'pending', 'Pending'
    DUE = 'due', 'Due'
    OVERDUE = 'overdue', 'Overdue'
    AMENDED = 'amended', 'Amended'


class RCMStatus(models.TextChoices):
    ACTIVE = 'active', 'Active'
    PENDING = 'pending', 'Pending'
    REVERSED = 'reversed', 'Reversed'


# ---------------------------------------------------------------------------
# Tax Jurisdiction
# ---------------------------------------------------------------------------

class TaxJurisdiction(models.Model):
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5, blank=True, null=True)
    authority = models.CharField(max_length=200, blank=True, null=True)
    currency_code = models.CharField(max_length=5, blank=True, null=True)
    registration_number = models.CharField(max_length=60, blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    filing_frequency = models.CharField(max_length=20, choices=FilingFrequency.choices, blank=True, null=True)
    last_filed = models.DateField(blank=True, null=True)
    next_due = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaxJurStatus.choices, default=TaxJurStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Jurisdiction'
        verbose_name_plural = 'Tax Jurisdictions'
        ordering = ['country']

    def __str__(self):
        return f"{self.country} - {self.authority}"


# ---------------------------------------------------------------------------
# Tax Type
# ---------------------------------------------------------------------------

class TaxType(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    applicable_to = models.CharField(max_length=30, blank=True, null=True, help_text='intra_state/inter_state/import/export/all')
    jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='tax_types',
    )
    rate_type = models.CharField(max_length=20, blank=True, null=True, help_text='percentage/fixed/tiered')
    default_rate = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    gov_authority = models.CharField(max_length=200, blank=True, null=True)
    filing_form = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaxStatus.choices, default=TaxStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Type'
        verbose_name_plural = 'Tax Types'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------------------------------------------------------------------
# HSN / SAC Code
# ---------------------------------------------------------------------------

class HSNCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    chapter = models.CharField(max_length=20, blank=True, null=True)
    chapter_name = models.CharField(max_length=200, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    tax_rate_code = models.CharField(max_length=20, blank=True, null=True)
    sac_code = models.CharField(max_length=20, blank=True, null=True)
    applicable_to = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=TaxStatus.choices, default=TaxStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'HSN/SAC Code'
        verbose_name_plural = 'HSN/SAC Codes'
        ordering = ['code']

    def __str__(self):
        return self.code


# ---------------------------------------------------------------------------
# Tax Rate
# ---------------------------------------------------------------------------

class TaxRate(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=150)
    tax_type = models.ForeignKey(
        TaxType, on_delete=models.SET_NULL, blank=True, null=True, related_name='rates',
    )
    jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='rates',
    )
    rate = models.DecimalField(max_digits=6, decimal_places=3)
    rate_type = models.CharField(max_length=20, default='percentage')
    effective_from = models.DateField(blank=True, null=True)
    effective_to = models.DateField(blank=True, null=True)
    priority = models.IntegerField(default=0)
    applicability = models.CharField(max_length=120, blank=True, null=True)
    hsn_codes = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=TaxRateStatus.choices, default=TaxRateStatus.ACTIVE)
    remarks = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Rate'
        verbose_name_plural = 'Tax Rates'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


# ---------------------------------------------------------------------------
# Tax Category
# ---------------------------------------------------------------------------

class TaxCategory(models.Model):
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, choices=TaxCategoryType.choices)
    description = models.TextField(blank=True, null=True)
    default_rate = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    applicable_jurisdictions = models.JSONField(default=list, blank=True)
    hsn_count = models.IntegerField(default=0)
    tags = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=TaxStatus.choices, default=TaxStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Category'
        verbose_name_plural = 'Tax Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Tax Group
# ---------------------------------------------------------------------------

class TaxGroup(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=150)
    jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='tax_groups',
    )
    composite_rate = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    applicability = models.CharField(max_length=120, blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaxStatus.choices, default=TaxStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Group'
        verbose_name_plural = 'Tax Groups'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class TaxGroupMember(models.Model):
    group = models.ForeignKey(TaxGroup, on_delete=models.CASCADE, related_name='members')
    tax_type = models.ForeignKey(
        TaxType, on_delete=models.SET_NULL, blank=True, null=True, related_name='group_members',
    )
    rate = models.DecimalField(max_digits=6, decimal_places=3)
    share = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)

    class Meta:
        verbose_name = 'Tax Group Member'
        verbose_name_plural = 'Tax Group Members'

    def __str__(self):
        return f"{self.group.code} - {self.tax_type}"


# ---------------------------------------------------------------------------
# Tax Rule
# ---------------------------------------------------------------------------

class TaxRule(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='rules',
    )
    priority = models.IntegerField(default=0)
    action_type = models.CharField(max_length=30, blank=True, null=True, help_text='apply_tax/apply_exemption/apply_reverse_charge/override_rate')
    action_tax_type = models.ForeignKey(
        TaxType, on_delete=models.SET_NULL, blank=True, null=True, related_name='rule_actions',
    )
    action_rate = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    validity_from = models.DateField(blank=True, null=True)
    validity_to = models.DateField(blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    usage_count = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=TaxRuleStatus.choices, default=TaxRuleStatus.DRAFT)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Rule'
        verbose_name_plural = 'Tax Rules'
        ordering = ['priority', 'code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class TaxRuleCondition(models.Model):
    rule = models.ForeignKey(TaxRule, on_delete=models.CASCADE, related_name='conditions')
    field = models.CharField(max_length=40, help_text='hsn_code/amount/customer_type/state/country/product_category/invoice_type')
    operator = models.CharField(max_length=20, help_text='equals/not_equals/greater_than/less_than/contains/in_list')
    value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Tax Rule Condition'
        verbose_name_plural = 'Tax Rule Conditions'

    def __str__(self):
        return f"{self.rule.code} - {self.field} {self.operator} {self.value}"


# ---------------------------------------------------------------------------
# Tax Exemption
# ---------------------------------------------------------------------------

class TaxExemption(models.Model):
    certificate_number = models.CharField(max_length=60, unique=True)
    holder_name = models.CharField(max_length=200)
    holder_type = models.CharField(max_length=20, blank=True, null=True, help_text='customer/vendor/organization')
    gstin = models.CharField(max_length=30, blank=True, null=True)
    exemption_type = models.CharField(max_length=20, choices=ExemptionType.choices)
    percentage = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    applicable_tax_type = models.ForeignKey(
        TaxType, on_delete=models.SET_NULL, blank=True, null=True, related_name='exemptions',
    )
    applicable_jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='exemptions',
    )
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    issuing_authority = models.CharField(max_length=200, blank=True, null=True)
    renewal_status = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ExemptionStatus.choices, default=ExemptionStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Exemption'
        verbose_name_plural = 'Tax Exemptions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.certificate_number} - {self.holder_name}"


# ---------------------------------------------------------------------------
# Reverse Charge Record
# ---------------------------------------------------------------------------

class ReverseChargeRecord(models.Model):
    invoice_number = models.CharField(max_length=40)
    vendor = models.ForeignKey(
        'procurement.Vendor', on_delete=models.SET_NULL, blank=True, null=True, related_name='reverse_charge_records',
    )
    vendor_gstin = models.CharField(max_length=30, blank=True, null=True)
    invoice_date = models.DateField(blank=True, null=True)
    invoice_amount = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    tax_type = models.ForeignKey(
        TaxType, on_delete=models.SET_NULL, blank=True, null=True, related_name='reverse_charge_records',
    )
    applicable_rule = models.CharField(max_length=150, blank=True, null=True)
    is_rcm = models.BooleanField(default=True)
    payment_status = models.CharField(max_length=20, blank=True, null=True, help_text='unpaid/partial/paid')
    reverse_charge_by = models.CharField(max_length=150, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=20, choices=RCMStatus.choices, default=RCMStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reverse Charge Record'
        verbose_name_plural = 'Reverse Charge Records'
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number


# ---------------------------------------------------------------------------
# Tax Return
# ---------------------------------------------------------------------------

class TaxReturn(models.Model):
    return_type = models.CharField(max_length=40, help_text='GSTR-1/GSTR-3B/VAT201...')
    form_name = models.CharField(max_length=60, blank=True, null=True)
    period = models.CharField(max_length=40, blank=True, null=True)
    period_start = models.DateField(blank=True, null=True)
    period_end = models.DateField(blank=True, null=True)
    filing_due_date = models.DateField(blank=True, null=True)
    filed_date = models.DateField(blank=True, null=True)
    tax_type = models.ForeignKey(
        TaxType, on_delete=models.SET_NULL, blank=True, null=True, related_name='returns',
    )
    jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='returns',
    )
    tax_payable = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tax_paid = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    interest = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    penalty = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    refund_claimed = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    refund_status = models.CharField(max_length=20, blank=True, null=True)
    arn = models.CharField(max_length=60, blank=True, null=True)
    file_by = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaxReturnStatus.choices, default=TaxReturnStatus.PENDING)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Return'
        verbose_name_plural = 'Tax Returns'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.return_type} - {self.period}"


# ---------------------------------------------------------------------------
# Tax Mapping Rule (cross-jurisdiction)
# ---------------------------------------------------------------------------

class TaxMappingRule(models.Model):
    source_jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='source_mapping_rules',
    )
    target_jurisdiction = models.ForeignKey(
        TaxJurisdiction, on_delete=models.SET_NULL, blank=True, null=True, related_name='target_mapping_rules',
    )
    source_field = models.CharField(max_length=80, blank=True, null=True)
    target_field = models.CharField(max_length=80, blank=True, null=True)
    source_rate = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    target_rate = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    mapping_type = models.CharField(max_length=60, blank=True, null=True)
    effective_from = models.DateField(blank=True, null=True)
    effective_to = models.DateField(blank=True, null=True)
    module = models.CharField(max_length=60, blank=True, null=True)
    status = models.CharField(max_length=20, choices=TaxJurStatus.choices, default=TaxJurStatus.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tax Mapping Rule'
        verbose_name_plural = 'Tax Mapping Rules'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.source_jurisdiction} -> {self.target_jurisdiction}"
