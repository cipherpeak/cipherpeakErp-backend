import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.organization.models import CostCenter
from apps.hr.models import Employee

print("Seeding Cost Centers...")

# Get existing employees for owner references
employees = list(Employee.objects.all())
if not employees:
    print("  ERROR: No employees found. Run seed_data.py first.")
    sys.exit(1)

cc1 = CostCenter.objects.create(code="CC-ENG-001", name="Engineering Department", type="cost", owner=employees[0], budget=500000.00, spent=125000.00, status="active")
cc2 = CostCenter.objects.create(code="CC-HR-001", name="Human Resources", type="cost", owner=employees[3], budget=200000.00, spent=45000.00, status="active")
cc3 = CostCenter.objects.create(code="CC-OPS-001", name="Operations Hub", type="profit", owner=employees[2], budget=750000.00, spent=320000.00, status="active")
cc4 = CostCenter.objects.create(code="CC-SALES-001", name="Sales & Marketing", type="revenue", owner=employees[4], budget=300000.00, spent=85000.00, status="active")
cc5 = CostCenter.objects.create(code="CC-IT-001", name="IT Infrastructure", type="cost", owner=employees[5], budget=400000.00, spent=210000.00, status="active")
cc6 = CostCenter.objects.create(code="CC-FIN-001", name="Finance & Accounting", type="profit", owner=employees[4], budget=150000.00, spent=35000.00, status="active")
cc7 = CostCenter.objects.create(code="CC-PROD-001", name="Production Line A", type="cost", owner=employees[6], budget=1000000.00, spent=475000.00, status="active")
cc8 = CostCenter.objects.create(code="CC-PROD-002", name="Production Line B", type="cost", owner=employees[6], budget=800000.00, spent=290000.00, status="inactive")

print(f"  Created {CostCenter.objects.count()} cost centers")
print("\nDone!")
