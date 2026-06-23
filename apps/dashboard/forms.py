from django import forms
from apps.authapp.models import Employee, Company

class NotificationForm(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Notification Title'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Notification Message'}))
    notification_type = forms.ChoiceField(
        choices=[
            ('common', 'Common (All Employees)'),
            ('company', 'Company Wise'),
            ('department', 'Department Wise'),
            ('individual', 'Individual Employee')
        ],
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'notificationType'})
    )
    
    # Dynamic fields
    company = forms.ModelChoiceField(
        queryset=Company.objects.filter(is_active=True),
        required=False,
        empty_label="Select Company",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'companySelect'})
    )
    
    department = forms.ChoiceField(
        choices=Employee.EMPLOYEE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'departmentSelect'})
    )
    
    employee = forms.ModelMultipleChoiceField(
        queryset=Employee.objects.filter(is_active=True, is_deleted=False).order_by('employee_name'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'employeeSelect', 'style': 'height: 150px;'})
    )
