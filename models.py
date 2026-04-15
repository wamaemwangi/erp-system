from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ======================
# USER PROFILE
# ======================
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('REQUESTER', 'Requester'),
        ('APPROVER', 'Approver'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='REQUESTER')


# ======================
# INVENTORY / PROCUREMENT
# ======================
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"


# ======================
# STORE REQUISITION
# ======================
class StoreRequisition(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    APPROVAL_LEVELS = [
        ('HOD', 'Head of Department'),
        ('PROCUREMENT_OFFICER', 'Procurement Officer'),
        ('PROCUREMENT_MANAGER', 'Procurement Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]

    description = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100)
    requested_by = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    approval_level = models.CharField(max_length=25, choices=APPROVAL_LEVELS, default='HOD')
    hod_approved = models.BooleanField(default=False)
    hod_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hod_approved_at = models.DateTimeField(blank=True, null=True)
    
    procurement_officer_approved = models.BooleanField(default=False)
    procurement_officer_approved_by = models.CharField(max_length=100, blank=True, null=True)
    procurement_officer_approved_at = models.DateTimeField(blank=True, null=True)
    
    procurement_manager_approved = models.BooleanField(default=False)
    procurement_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    procurement_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Receiving fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_received = models.BooleanField(default=False)
    received_by = models.CharField(max_length=100, blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.requested_by} - {self.department}"


class StoreRequisitionItem(models.Model):
    store_requisition = models.ForeignKey(StoreRequisition, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.description} x {self.quantity}"


# ======================
# PURCHASE REQUISITION
# ======================
class PurchaseRequisition(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'HR'),
        ('FINANCE', 'Finance'),
        ('PROCUREMENT', 'Procurement'),
        ('IT', 'IT'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    APPROVAL_LEVELS = [
        ('HOD', 'Head of Department'),
        ('PROCUREMENT_OFFICER', 'Procurement Officer'),
        ('PROCUREMENT_MANAGER', 'Procurement Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]

    description = models.TextField(blank=True, null=True)
    requested_by = models.CharField(max_length=100)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='PROCUREMENT')
    purchase_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    approval_level = models.CharField(max_length=25, choices=APPROVAL_LEVELS, default='HOD')
    hod_approved = models.BooleanField(default=False)
    hod_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hod_approved_at = models.DateTimeField(blank=True, null=True)
    
    procurement_officer_approved = models.BooleanField(default=False)
    procurement_officer_approved_by = models.CharField(max_length=100, blank=True, null=True)
    procurement_officer_approved_at = models.DateTimeField(blank=True, null=True)
    
    procurement_manager_approved = models.BooleanField(default=False)
    procurement_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    procurement_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Receiving fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_received = models.BooleanField(default=False)
    received_by = models.CharField(max_length=100, blank=True, null=True)
    received_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.requested_by} - {self.department}"


class PurchaseRequisitionItem(models.Model):
    purchase_requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.description} x {self.quantity}"


# ======================
# HR MODULE
# ======================
class LeaveApplication(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('annual', 'Annual Leave'),
        ('casual', 'Casual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('exam', 'Exam Leave'),
        ('sick', 'Sick Leave'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    APPROVAL_LEVELS = [
        ('HOD', 'Head of Department'),
        ('HR', 'HR Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]

    employee_name = models.CharField(max_length=100)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES, default='annual')
    days = models.PositiveIntegerField(default=0)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    department = models.CharField(max_length=50, default='General')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Approval workflow fields
    approval_level = models.CharField(max_length=20, choices=APPROVAL_LEVELS, default='HOD')
    hod_approved = models.BooleanField(default=False)
    hod_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hod_approved_at = models.DateTimeField(blank=True, null=True)
    
    hr_approved = models.BooleanField(default=False)
    hr_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hr_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Settlement fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_settled = models.BooleanField(default=False)
    settled_by = models.CharField(max_length=100, blank=True, null=True)
    settled_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.employee_name} - {self.get_leave_type_display()}"


class Overtime(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]

    APPROVAL_LEVELS = [
        ('HOD', 'Head of Department'),
        ('HR', 'HR Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    employee_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=20, blank=True, null=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    reason = models.TextField()
    department = models.CharField(max_length=50, default='General')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Approval workflow fields
    approval_level = models.CharField(max_length=20, choices=APPROVAL_LEVELS, default='HOD')
    hod_approved = models.BooleanField(default=False)
    hod_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hod_approved_at = models.DateTimeField(blank=True, null=True)
    
    hr_approved = models.BooleanField(default=False)
    hr_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hr_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Settlement fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_settled = models.BooleanField(default=False)
    settled_by = models.CharField(max_length=100, blank=True, null=True)
    settled_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.employee_name} - {self.hours} hrs - {self.status}"


class Attendance(models.Model):
    employee_name = models.CharField(max_length=100)
    date = models.DateField()
    status = models.CharField(max_length=20)


# ======================
# FINANCE BASE MODEL
# ======================
class BaseRequest(models.Model):
    employee_name = models.CharField(max_length=100, default="Unknown")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(default="No description")
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=50, default="General")
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('APPROVED', 'Approved'),
            ('REJECTED', 'Rejected'),
            ('CANCELLED', 'Cancelled'),
        ],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# ======================
# PETTY CASH
# ======================
class PettyCash(BaseRequest):
    petty_cash_number = models.CharField(max_length=20, blank=True, null=True)
    employee_number = models.CharField(max_length=20, blank=True, null=True)
    request_type = models.CharField(max_length=20, blank=True, null=True)
    document = models.FileField(upload_to="petty_cash_docs/", blank=True, null=True)
    
    APPROVAL_LEVELS = [
        ('HOD', 'Head of Department'),
        ('FINANCE_OFFICER', 'Finance Officer'),
        ('FINANCE_MANAGER', 'Finance Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    approval_level = models.CharField(max_length=20, choices=APPROVAL_LEVELS, default='HOD')
    hod_approved = models.BooleanField(default=False)
    hod_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hod_approved_at = models.DateTimeField(blank=True, null=True)
    
    finance_officer_approved = models.BooleanField(default=False)
    finance_officer_approved_by = models.CharField(max_length=100, blank=True, null=True)
    finance_officer_approved_at = models.DateTimeField(blank=True, null=True)
    
    finance_manager_approved = models.BooleanField(default=False)
    finance_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    finance_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Surrender fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_surrendered = models.BooleanField(default=False)
    surrendered_by = models.CharField(max_length=100, blank=True, null=True)
    surrendered_at = models.DateTimeField(blank=True, null=True)
    balance_returned = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class PettyCashItem(models.Model):
    petty_cash = models.ForeignKey(PettyCash, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount}"


# ======================
# IMPREST
# ======================
class Imprest(BaseRequest):
    imprest_number = models.CharField(max_length=20, blank=True)
    document = models.FileField(upload_to='imprest_docs/', null=True, blank=True)
    
    APPROVAL_LEVELS = [
        ('HOD', 'Head of Department'),
        ('FINANCE_OFFICER', 'Finance Officer'),
        ('FINANCE_MANAGER', 'Finance Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    approval_level = models.CharField(max_length=20, choices=APPROVAL_LEVELS, default='HOD')
    hod_approved = models.BooleanField(default=False)
    hod_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hod_approved_at = models.DateTimeField(blank=True, null=True)
    
    finance_officer_approved = models.BooleanField(default=False)
    finance_officer_approved_by = models.CharField(max_length=100, blank=True, null=True)
    finance_officer_approved_at = models.DateTimeField(blank=True, null=True)
    
    finance_manager_approved = models.BooleanField(default=False)
    finance_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    finance_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Surrender fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_surrendered = models.BooleanField(default=False)
    surrendered_by = models.CharField(max_length=100, blank=True, null=True)
    surrendered_at = models.DateTimeField(blank=True, null=True)
    balance_returned = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.imprest_number or "Imprest"


class ImprestItem(models.Model):
    imprest = models.ForeignKey(Imprest, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.description} - {self.amount}"


# ======================
# SALARY ADVANCE
# ======================
class SalaryAdvance(BaseRequest):
    purpose = models.CharField(max_length=255, default="Not specified")
    date_required = models.DateField(null=True, blank=True)
    
    APPROVAL_LEVELS = [
        ('HR', 'HR Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    approval_level = models.CharField(max_length=20, choices=APPROVAL_LEVELS, default='HR')
    hr_approved = models.BooleanField(default=False)
    hr_approved_by = models.CharField(max_length=100, blank=True, null=True)
    hr_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Settlement fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_settled = models.BooleanField(default=False)
    settled_by = models.CharField(max_length=100, blank=True, null=True)
    settled_at = models.DateTimeField(blank=True, null=True)


# ======================
# IMPREST SURRENDER
# ======================
class ImprestSurrender(models.Model):
    imprest = models.ForeignKey(Imprest, on_delete=models.CASCADE)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    balance_returned = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved')],
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)


# ======================
# FLEET MANAGEMENT
# ======================
class DepartmentApprover(models.Model):
    APPROVER_ROLES = [
        ('HOD', 'Head of Department'),
        ('FINANCE_OFFICER', 'Finance Officer'),
        ('FINANCE_MANAGER', 'Finance Manager'),
        ('MANAGER', 'General Manager'),
        ('HR_MANAGER', 'HR Manager'),
        ('PROCUREMENT_OFFICER', 'Procurement Officer'),
        ('PROCUREMENT_MANAGER', 'Procurement Manager'),
        ('FLEET_MANAGER', 'Fleet Manager'),
        ('OPERATIONS_MANAGER', 'Operations Manager'),
    ]
    
    department = models.CharField(max_length=50)
    role = models.CharField(max_length=30, choices=APPROVER_ROLES)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approver_for')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['department', 'role']
    
    def __str__(self):
        return f"{self.department} - {self.role}: {self.user.username}"


class TransportRequisition(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    APPROVAL_LEVELS = [
        ('FLEET_MANAGER', 'Fleet Manager'),
        ('OPERATIONS_MANAGER', 'Operations Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]

    employee_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    destination = models.CharField(max_length=200)
    date_required = models.DateField()
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)
    
    approval_level = models.CharField(max_length=25, choices=APPROVAL_LEVELS, default='FLEET_MANAGER')
    fleet_manager_approved = models.BooleanField(default=False)
    fleet_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    fleet_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    operations_manager_approved = models.BooleanField(default=False)
    operations_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    operations_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Completion fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completed_by = models.CharField(max_length=100, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee_name} - {self.destination}"


class WorkTicket(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    APPROVAL_LEVELS = [
        ('FLEET_MANAGER', 'Fleet Manager'),
        ('OPERATIONS_MANAGER', 'Operations Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]

    employee_name = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    destination = models.CharField(max_length=255)
    date_required = models.DateField()
    purpose = models.TextField()
    document = models.FileField(upload_to='work_tickets/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    approval_level = models.CharField(max_length=25, choices=APPROVAL_LEVELS, default='FLEET_MANAGER')
    fleet_manager_approved = models.BooleanField(default=False)
    fleet_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    fleet_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    operations_manager_approved = models.BooleanField(default=False)
    operations_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    operations_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Completion fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completed_by = models.CharField(max_length=100, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee_name} - {self.destination}"


class FuelRequisition(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected')
    ]

    APPROVAL_LEVELS = [
        ('FLEET_MANAGER', 'Fleet Manager'),
        ('OPERATIONS_MANAGER', 'Operations Manager'),
        ('MANAGER', 'General Manager'),
        ('APPROVED', 'Fully Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    requested_by = models.CharField(max_length=100)
    employee_number = models.CharField(max_length=50, blank=True, null=True)
    employee_name = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=50, default='General')
    destination = models.CharField(max_length=200, blank=True, null=True)
    date_required = models.DateField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to='fuel_docs/', blank=True, null=True)
    vehicle = models.CharField(max_length=100)
    liters = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    
    approval_level = models.CharField(max_length=25, choices=APPROVAL_LEVELS, default='FLEET_MANAGER')
    fleet_manager_approved = models.BooleanField(default=False)
    fleet_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    fleet_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    operations_manager_approved = models.BooleanField(default=False)
    operations_manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    operations_manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    manager_approved = models.BooleanField(default=False)
    manager_approved_by = models.CharField(max_length=100, blank=True, null=True)
    manager_approved_at = models.DateTimeField(blank=True, null=True)
    
    rejection_reason = models.TextField(blank=True, null=True)
    rejected_by = models.CharField(max_length=100, blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    
    # Posting and Completion fields
    is_posted = models.BooleanField(default=False)
    posted_by = models.CharField(max_length=100, blank=True, null=True)
    posted_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    completed_by = models.CharField(max_length=100, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.employee_name} - {self.vehicle}"