from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from .models import (
    LeaveApplication,
    StoreRequisition,
    StoreRequisitionItem,
    PurchaseRequisition,
    PurchaseRequisitionItem,
    PettyCash,
    PettyCashItem,
    Imprest,
    ImprestItem,
    SalaryAdvance,
    ImprestSurrender,
    InventoryItem,
    TransportRequisition,
    WorkTicket,
    FuelRequisition,
    Overtime,
)

from .forms import PettyCashForm, ImprestForm, SalaryAdvanceForm


# ======================
# DECORATOR
# ======================
def approver_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'APPROVER':
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


# ======================
# DASHBOARD
# ======================
@login_required
def dashboard(request):
    context = {
        'pending_leaves': LeaveApplication.objects.filter(status='PENDING').count(),
        'pending_overtime': Overtime.objects.filter(status='PENDING').count(),
        'pending_store': StoreRequisition.objects.filter(status='PENDING').count(),
        'pending_purchase': PurchaseRequisition.objects.filter(status='PENDING').count(),
        'pending_petty_cash': PettyCash.objects.filter(status='PENDING').count(),
        'pending_imprest': Imprest.objects.filter(status='PENDING').count(),
        'pending_salary_advance': SalaryAdvance.objects.filter(status='PENDING').count(),
        'pending_imprest_surrender': ImprestSurrender.objects.filter(status='PENDING').count(),
        'pending_transport': TransportRequisition.objects.filter(status='PENDING').count(),
        'pending_work_ticket': WorkTicket.objects.filter(status='PENDING').count(),
        'pending_fuel': FuelRequisition.objects.filter(status='PENDING').count(),
        'pending_petty_imprest': PettyCash.objects.filter(status='PENDING').count() + Imprest.objects.filter(status='PENDING').count(),
    }
    return render(request, 'frontend/dashboard.html', context)


# ======================
# INVENTORY
# ======================
@login_required
def inventory(request):
    items = InventoryItem.objects.all()
    return render(request, 'frontend/inventory.html', {'items': items})


# ======================
# HR MODULE
# ======================
@login_required
def hr(request):
    return render(request, 'frontend/hr.html')


@login_required
def apply_leave(request):
    if request.method == "POST":
        LeaveApplication.objects.create(
            employee_name=request.user.get_full_name() or request.user.username,
            leave_type=request.POST.get("leave_type"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            days=request.POST.get("days", 0),
            reason=request.POST.get("reason"),
            status="PENDING",
            approval_level="HOD"
        )
        messages.success(request, 'Leave application submitted successfully! Waiting for HOD approval.')
        return redirect('leave_apply')
    
    leaves = LeaveApplication.objects.filter(
        employee_name=request.user.get_full_name() or request.user.username
    ).order_by('-id')
    
    leave_limits = {'annual': 30, 'casual': 21, 'maternity': 150, 'paternity': 45, 'exam': 90, 'sick': 14}
    for leave in leaves:
        leave.balance_remaining = leave_limits.get(leave.leave_type, 0) - (leave.days or 0)
    
    return render(request, 'frontend/leave_apply.html', {'leaves': leaves})


@login_required
def leave_approval(request):
    leaves = LeaveApplication.objects.filter(status='PENDING').order_by('-id')
    leave_limits = {'annual': 30, 'casual': 21, 'maternity': 150, 'paternity': 45, 'exam': 90, 'sick': 14}
    for leave in leaves:
        leave.balance_remaining = leave_limits.get(leave.leave_type, 0) - (leave.days or 0)
    return render(request, 'frontend/leave_approval.html', {'leaves': leaves})


@login_required
def approve_leave(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    obj.status = "APPROVED"
    obj.save()
    messages.success(request, 'Leave application approved!')
    return redirect('leave_approval')


@login_required
def reject_leave(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    obj.status = "REJECTED"
    obj.save()
    messages.success(request, 'Leave application rejected!')
    return redirect('leave_approval')


@login_required
def payslips(request):
    return render(request, 'frontend/payslips.html')


@login_required
def overtime(request):
    overtime_requests = Overtime.objects.filter(
        employee_name=request.user.get_full_name() or request.user.username
    ).order_by('-created_at')
    
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        if edit_id:
            obj = get_object_or_404(Overtime, id=edit_id)
            obj.hours = request.POST.get('hours')
            obj.reason = request.POST.get('reason')
            obj.department = request.POST.get('department')
            obj.save()
            messages.success(request, 'Overtime request updated successfully!')
        else:
            hours = request.POST.get('hours')
            reason = request.POST.get('reason')
            department = request.POST.get('department', 'General')
            if not hours or not reason:
                messages.error(request, 'Please fill all required fields!')
                return redirect('overtime')
            Overtime.objects.create(
                employee_name=request.user.get_full_name() or request.user.username,
                employee_number=f"EMP{request.user.id:03d}",
                hours=hours,
                reason=reason,
                department=department,
                status='PENDING',
                approval_level='HOD'
            )
            messages.success(request, 'Overtime request submitted successfully! Waiting for HOD approval.')
        return redirect('overtime')
    
    return render(request, 'frontend/overtime.html', {'overtime_requests': overtime_requests})


@login_required
def overtime_approval(request):
    overtime_requests = Overtime.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/overtime_approval.html', {'overtime_requests': overtime_requests})


@login_required
def approve_overtime(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    obj.status = "APPROVED"
    obj.save()
    messages.success(request, 'Overtime request approved!')
    return redirect('overtime_approval')


@login_required
def reject_overtime(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    obj.status = "REJECTED"
    obj.save()
    messages.success(request, 'Overtime request rejected!')
    return redirect('overtime_approval')


@login_required
def cancel_overtime(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    obj.status = "CANCELLED"
    obj.save()
    messages.success(request, 'Overtime request cancelled!')
    return redirect('overtime')


@login_required
def profile(request):
    return render(request, 'frontend/profile.html')


@login_required
def attendance(request):
    return render(request, 'frontend/attendance.html')


# ======================
# LEAVE APPROVAL - HOD
# ======================
@login_required
def leave_approval_hod(request):
    user_department = None
    if hasattr(request.user, 'userprofile'):
        user_department = request.user.userprofile.department
    
    if user_department:
        requests = LeaveApplication.objects.filter(
            department=user_department,
            approval_level='HOD',
            hod_approved=False,
            status='PENDING'
        ).order_by('-created_at')
    else:
        requests = LeaveApplication.objects.none()
        messages.warning(request, 'Your profile does not have a department assigned.')
    
    return render(request, 'frontend/leave_approval_hod.html', {'requests': requests})


@login_required
def approve_leave_hod(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    obj.hod_approved = True
    obj.hod_approved_by = request.user.username
    obj.hod_approved_at = timezone.now()
    obj.approval_level = 'HR'
    obj.save()
    messages.success(request, f'Leave request approved. Sent to HR Manager.')
    return redirect('leave_approval_hod')


@login_required
def reject_leave_hod(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Leave request rejected.')
        return redirect('leave_approval_hod')
    return render(request, 'frontend/leave_reject_modal.html', {'request': obj})


# ======================
# LEAVE APPROVAL - HR MANAGER
# ======================
@login_required
def leave_approval_hr(request):
    requests = LeaveApplication.objects.filter(
        approval_level='HR',
        hod_approved=True,
        hr_approved=False,
        status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/leave_approval_hr.html', {'requests': requests})


@login_required
def approve_leave_hr(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    obj.hr_approved = True
    obj.hr_approved_by = request.user.username
    obj.hr_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Leave request approved. Sent to General Manager.')
    return redirect('leave_approval_hr')


@login_required
def reject_leave_hr(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Leave request rejected.')
        return redirect('leave_approval_hr')
    return render(request, 'frontend/leave_reject_modal.html', {'request': obj})


# ======================
# LEAVE APPROVAL - GENERAL MANAGER
# ======================
@login_required
def leave_approval_manager(request):
    requests = LeaveApplication.objects.filter(
        approval_level='MANAGER',
        hod_approved=True,
        hr_approved=True,
        manager_approved=False,
        status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/leave_approval_manager.html', {'requests': requests})


@login_required
def approve_leave_manager(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Leave request fully approved!')
    return redirect('leave_approval_manager')


@login_required
def reject_leave_manager(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Leave request rejected.')
        return redirect('leave_approval_manager')
    return render(request, 'frontend/leave_reject_modal.html', {'request': obj})


# ======================
# LEAVE POSTING & SETTLEMENT
# ======================
@login_required
def leave_approved_list(request):
    requests = LeaveApplication.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/leave_approved_list.html', {'requests': requests})


@login_required
def leave_posted_list(request):
    requests = LeaveApplication.objects.filter(is_posted=True, is_settled=False).order_by('-created_at')
    return render(request, 'frontend/leave_posted_list.html', {'requests': requests})


@login_required
def leave_settled_list(request):
    requests = LeaveApplication.objects.filter(is_settled=True).order_by('-created_at')
    return render(request, 'frontend/leave_settled_list.html', {'requests': requests})


@login_required
def post_leave(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Leave for {obj.employee_name} posted successfully!')
    return redirect('leave_approved_list')


@login_required
def settle_leave(request, pk):
    obj = get_object_or_404(LeaveApplication, pk=pk)
    if request.method == 'POST':
        obj.is_settled = True
        obj.settled_by = request.user.username
        obj.settled_at = timezone.now()
        obj.save()
        messages.success(request, f'Leave for {obj.employee_name} settled successfully!')
        return redirect('leave_posted_list')
    return render(request, 'frontend/leave_settle_modal.html', {'request': obj})


# ======================
# OVERTIME APPROVAL - HOD
# ======================
@login_required
def overtime_approval_hod(request):
    user_department = None
    if hasattr(request.user, 'userprofile'):
        user_department = request.user.userprofile.department
    
    if user_department:
        requests = Overtime.objects.filter(
            department=user_department,
            approval_level='HOD',
            hod_approved=False,
            status='PENDING'
        ).order_by('-created_at')
    else:
        requests = Overtime.objects.none()
        messages.warning(request, 'Your profile does not have a department assigned.')
    
    return render(request, 'frontend/overtime_approval_hod.html', {'requests': requests})


@login_required
def approve_overtime_hod(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    obj.hod_approved = True
    obj.hod_approved_by = request.user.username
    obj.hod_approved_at = timezone.now()
    obj.approval_level = 'HR'
    obj.save()
    messages.success(request, f'Overtime request approved. Sent to HR Manager.')
    return redirect('overtime_approval_hod')


@login_required
def reject_overtime_hod(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Overtime request rejected.')
        return redirect('overtime_approval_hod')
    return render(request, 'frontend/overtime_reject_modal.html', {'request': obj})


# ======================
# OVERTIME APPROVAL - HR MANAGER
# ======================
@login_required
def overtime_approval_hr(request):
    requests = Overtime.objects.filter(
        approval_level='HR',
        hod_approved=True,
        hr_approved=False,
        status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/overtime_approval_hr.html', {'requests': requests})


@login_required
def approve_overtime_hr(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    obj.hr_approved = True
    obj.hr_approved_by = request.user.username
    obj.hr_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Overtime request approved. Sent to General Manager.')
    return redirect('overtime_approval_hr')


@login_required
def reject_overtime_hr(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Overtime request rejected.')
        return redirect('overtime_approval_hr')
    return render(request, 'frontend/overtime_reject_modal.html', {'request': obj})


# ======================
# OVERTIME APPROVAL - GENERAL MANAGER
# ======================
@login_required
def overtime_approval_manager(request):
    requests = Overtime.objects.filter(
        approval_level='MANAGER',
        hod_approved=True,
        hr_approved=True,
        manager_approved=False,
        status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/overtime_approval_manager.html', {'requests': requests})


@login_required
def approve_overtime_manager(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Overtime request fully approved!')
    return redirect('overtime_approval_manager')


@login_required
def reject_overtime_manager(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Overtime request rejected.')
        return redirect('overtime_approval_manager')
    return render(request, 'frontend/overtime_reject_modal.html', {'request': obj})


# ======================
# OVERTIME POSTING & SETTLEMENT
# ======================
@login_required
def overtime_approved_list(request):
    requests = Overtime.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/overtime_approved_list.html', {'requests': requests})


@login_required
def overtime_posted_list(request):
    requests = Overtime.objects.filter(is_posted=True, is_settled=False).order_by('-created_at')
    return render(request, 'frontend/overtime_posted_list.html', {'requests': requests})


@login_required
def overtime_settled_list(request):
    requests = Overtime.objects.filter(is_settled=True).order_by('-created_at')
    return render(request, 'frontend/overtime_settled_list.html', {'requests': requests})


@login_required
def post_overtime(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Overtime for {obj.employee_name} posted successfully!')
    return redirect('overtime_approved_list')


@login_required
def settle_overtime(request, pk):
    obj = get_object_or_404(Overtime, pk=pk)
    if request.method == 'POST':
        obj.is_settled = True
        obj.settled_by = request.user.username
        obj.settled_at = timezone.now()
        obj.save()
        messages.success(request, f'Overtime for {obj.employee_name} settled successfully!')
        return redirect('overtime_posted_list')
    return render(request, 'frontend/overtime_settle_modal.html', {'request': obj})


# ======================
# STORE REQUISITIONS
# ======================
@login_required
def store_requisition(request):
    requisitions = StoreRequisition.objects.filter(requested_by=request.user.username).order_by('-created_at')
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        if edit_id:
            obj = get_object_or_404(StoreRequisition, id=edit_id)
            obj.description = request.POST.get('description', '')
            obj.department = request.POST.get('department')
            obj.save()
            messages.success(request, 'Store requisition updated successfully!')
        else:
            obj = StoreRequisition.objects.create(
                description=request.POST.get('description', ''),
                department=request.POST.get('department'),
                requested_by=request.user.username,
                status="PENDING",
                approval_level="HOD"
            )
            descriptions = request.POST.getlist('item_description[]')
            quantities = request.POST.getlist('item_quantity[]')
            for i in range(len(descriptions)):
                desc = descriptions[i]
                qty = quantities[i]
                if desc and qty:
                    try:
                        quantity = int(qty)
                        StoreRequisitionItem.objects.create(store_requisition=obj, description=desc, quantity=quantity)
                    except Exception as e:
                        print(f"Error saving item: {e}")
            messages.success(request, 'Store requisition created successfully! Waiting for HOD approval.')
        return redirect('store_requisition')
    return render(request, 'frontend/store_requisition.html', {'requisitions': requisitions})


@login_required
def store_approval(request):
    requisitions = StoreRequisition.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/store_approval.html', {'requisitions': requisitions})


@login_required
def approve_store_requisition(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, 'Store requisition approved!')
    return redirect('store_approval')


@login_required
def reject_store_requisition(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.status = 'REJECTED'
    obj.save()
    messages.success(request, 'Store requisition rejected!')
    return redirect('store_approval')


@login_required
def cancel_store_requisition(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.status = "CANCELLED"
    obj.save()
    messages.success(request, 'Store requisition cancelled!')
    return redirect('store_requisition')


# ======================
# STORE REQUISITION APPROVAL - MULTI LEVEL
# ======================
@login_required
def store_approval_hod(request):
    user_department = None
    if hasattr(request.user, 'userprofile'):
        user_department = request.user.userprofile.department
    if user_department:
        requests = StoreRequisition.objects.filter(
            department=user_department, approval_level='HOD', hod_approved=False, status='PENDING'
        ).order_by('-created_at')
    else:
        requests = StoreRequisition.objects.none()
        messages.warning(request, 'Your profile does not have a department assigned.')
    return render(request, 'frontend/store_approval_hod.html', {'requests': requests})


@login_required
def approve_store_hod(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.hod_approved = True
    obj.hod_approved_by = request.user.username
    obj.hod_approved_at = timezone.now()
    obj.approval_level = 'PROCUREMENT_OFFICER'
    obj.save()
    messages.success(request, f'Store requisition SR-{obj.id} approved. Sent to Procurement Officer.')
    return redirect('store_approval_hod')


@login_required
def reject_store_hod(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Store requisition SR-{obj.id} rejected.')
        return redirect('store_approval_hod')
    return render(request, 'frontend/store_reject_modal.html', {'request': obj})


@login_required
def store_approval_procurement_officer(request):
    requests = StoreRequisition.objects.filter(
        approval_level='PROCUREMENT_OFFICER', hod_approved=True, procurement_officer_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/store_approval_procurement_officer.html', {'requests': requests})


@login_required
def approve_store_procurement_officer(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.procurement_officer_approved = True
    obj.procurement_officer_approved_by = request.user.username
    obj.procurement_officer_approved_at = timezone.now()
    obj.approval_level = 'PROCUREMENT_MANAGER'
    obj.save()
    messages.success(request, f'Store requisition SR-{obj.id} approved. Sent to Procurement Manager.')
    return redirect('store_approval_procurement_officer')


@login_required
def reject_store_procurement_officer(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Store requisition SR-{obj.id} rejected.')
        return redirect('store_approval_procurement_officer')
    return render(request, 'frontend/store_reject_modal.html', {'request': obj})


@login_required
def store_approval_procurement_manager(request):
    requests = StoreRequisition.objects.filter(
        approval_level='PROCUREMENT_MANAGER', hod_approved=True, procurement_officer_approved=True, procurement_manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/store_approval_procurement_manager.html', {'requests': requests})


@login_required
def approve_store_procurement_manager(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.procurement_manager_approved = True
    obj.procurement_manager_approved_by = request.user.username
    obj.procurement_manager_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Store requisition SR-{obj.id} approved. Sent to General Manager.')
    return redirect('store_approval_procurement_manager')


@login_required
def reject_store_procurement_manager(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Store requisition SR-{obj.id} rejected.')
        return redirect('store_approval_procurement_manager')
    return render(request, 'frontend/store_reject_modal.html', {'request': obj})


@login_required
def store_approval_manager(request):
    requests = StoreRequisition.objects.filter(
        approval_level='MANAGER', hod_approved=True, procurement_officer_approved=True, procurement_manager_approved=True, manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/store_approval_manager.html', {'requests': requests})


@login_required
def approve_store_manager(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Store requisition SR-{obj.id} fully approved!')
    return redirect('store_approval_manager')


@login_required
def reject_store_manager(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Store requisition SR-{obj.id} rejected.')
        return redirect('store_approval_manager')
    return render(request, 'frontend/store_reject_modal.html', {'request': obj})


# ======================
# STORE POSTING & RECEIVING
# ======================
@login_required
def store_approved_list(request):
    requests = StoreRequisition.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/store_approved_list.html', {'requests': requests})


@login_required
def store_posted_list(request):
    requests = StoreRequisition.objects.filter(is_posted=True, is_received=False).order_by('-created_at')
    return render(request, 'frontend/store_posted_list.html', {'requests': requests})


@login_required
def store_received_list(request):
    requests = StoreRequisition.objects.filter(is_received=True).order_by('-created_at')
    return render(request, 'frontend/store_received_list.html', {'requests': requests})


@login_required
def post_store_requisition(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Store requisition SR-{obj.id} posted successfully!')
    return redirect('store_approved_list')


@login_required
def receive_store_requisition(request, pk):
    obj = get_object_or_404(StoreRequisition, pk=pk)
    if request.method == 'POST':
        obj.is_received = True
        obj.received_by = request.user.username
        obj.received_at = timezone.now()
        obj.save()
        messages.success(request, f'Store requisition SR-{obj.id} marked as received!')
        return redirect('store_posted_list')
    return render(request, 'frontend/store_receive_modal.html', {'request': obj})


# ======================
# PURCHASE REQUISITIONS
# ======================
@login_required
def purchase_requisition(request):
    requisitions = PurchaseRequisition.objects.filter(requested_by=request.user.username).order_by('-created_at')
    if request.method == 'POST':
        edit_id = request.POST.get('edit_id')
        if edit_id:
            obj = get_object_or_404(PurchaseRequisition, id=edit_id)
            obj.description = request.POST.get('description', '')
            obj.department = request.POST.get('department')
            obj.save()
            messages.success(request, 'Purchase requisition updated successfully!')
        else:
            obj = PurchaseRequisition.objects.create(
                description=request.POST.get('description', ''),
                department=request.POST.get('department'),
                requested_by=request.user.username,
                status="PENDING",
                approval_level="HOD"
            )
            descriptions = request.POST.getlist('item_description[]')
            quantities = request.POST.getlist('item_quantity[]')
            for i in range(len(descriptions)):
                desc = descriptions[i]
                qty = quantities[i]
                if desc and qty:
                    try:
                        quantity = int(qty)
                        PurchaseRequisitionItem.objects.create(purchase_requisition=obj, description=desc, quantity=quantity)
                    except Exception as e:
                        print(f"Error saving item: {e}")
            messages.success(request, 'Purchase requisition created successfully! Waiting for HOD approval.')
        return redirect('purchase_requisition')
    return render(request, 'frontend/purchase_requisition.html', {'requisitions': requisitions})


@login_required
def purchase_approval(request):
    requisitions = PurchaseRequisition.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/purchase_approval.html', {'requisitions': requisitions})


@login_required
def approve_purchase_requisition(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, 'Purchase requisition approved!')
    return redirect('purchase_approval')


@login_required
def reject_purchase_requisition(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.status = 'REJECTED'
    obj.save()
    messages.success(request, 'Purchase requisition rejected!')
    return redirect('purchase_approval')


@login_required
def cancel_purchase_requisition(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.status = "CANCELLED"
    obj.save()
    messages.success(request, 'Purchase requisition cancelled!')
    return redirect('purchase_requisition')


# ======================
# PURCHASE REQUISITION APPROVAL - MULTI LEVEL
# ======================
@login_required
def purchase_approval_hod(request):
    user_department = None
    if hasattr(request.user, 'userprofile'):
        user_department = request.user.userprofile.department
    if user_department:
        requests = PurchaseRequisition.objects.filter(
            department=user_department, approval_level='HOD', hod_approved=False, status='PENDING'
        ).order_by('-created_at')
    else:
        requests = PurchaseRequisition.objects.none()
        messages.warning(request, 'Your profile does not have a department assigned.')
    return render(request, 'frontend/purchase_approval_hod.html', {'requests': requests})


@login_required
def approve_purchase_hod(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.hod_approved = True
    obj.hod_approved_by = request.user.username
    obj.hod_approved_at = timezone.now()
    obj.approval_level = 'PROCUREMENT_OFFICER'
    obj.save()
    messages.success(request, f'Purchase requisition PR-{obj.id} approved. Sent to Procurement Officer.')
    return redirect('purchase_approval_hod')


@login_required
def reject_purchase_hod(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Purchase requisition PR-{obj.id} rejected.')
        return redirect('purchase_approval_hod')
    return render(request, 'frontend/purchase_reject_modal.html', {'request': obj})


@login_required
def purchase_approval_procurement_officer(request):
    requests = PurchaseRequisition.objects.filter(
        approval_level='PROCUREMENT_OFFICER', hod_approved=True, procurement_officer_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/purchase_approval_procurement_officer.html', {'requests': requests})


@login_required
def approve_purchase_procurement_officer(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.procurement_officer_approved = True
    obj.procurement_officer_approved_by = request.user.username
    obj.procurement_officer_approved_at = timezone.now()
    obj.approval_level = 'PROCUREMENT_MANAGER'
    obj.save()
    messages.success(request, f'Purchase requisition PR-{obj.id} approved. Sent to Procurement Manager.')
    return redirect('purchase_approval_procurement_officer')


@login_required
def reject_purchase_procurement_officer(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Purchase requisition PR-{obj.id} rejected.')
        return redirect('purchase_approval_procurement_officer')
    return render(request, 'frontend/purchase_reject_modal.html', {'request': obj})


@login_required
def purchase_approval_procurement_manager(request):
    requests = PurchaseRequisition.objects.filter(
        approval_level='PROCUREMENT_MANAGER', hod_approved=True, procurement_officer_approved=True, procurement_manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/purchase_approval_procurement_manager.html', {'requests': requests})


@login_required
def approve_purchase_procurement_manager(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.procurement_manager_approved = True
    obj.procurement_manager_approved_by = request.user.username
    obj.procurement_manager_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Purchase requisition PR-{obj.id} approved. Sent to General Manager.')
    return redirect('purchase_approval_procurement_manager')


@login_required
def reject_purchase_procurement_manager(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Purchase requisition PR-{obj.id} rejected.')
        return redirect('purchase_approval_procurement_manager')
    return render(request, 'frontend/purchase_reject_modal.html', {'request': obj})


@login_required
def purchase_approval_manager(request):
    requests = PurchaseRequisition.objects.filter(
        approval_level='MANAGER', hod_approved=True, procurement_officer_approved=True, procurement_manager_approved=True, manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/purchase_approval_manager.html', {'requests': requests})


@login_required
def approve_purchase_manager(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Purchase requisition PR-{obj.id} fully approved!')
    return redirect('purchase_approval_manager')


@login_required
def reject_purchase_manager(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Purchase requisition PR-{obj.id} rejected.')
        return redirect('purchase_approval_manager')
    return render(request, 'frontend/purchase_reject_modal.html', {'request': obj})


# ======================
# PURCHASE POSTING & RECEIVING
# ======================
@login_required
def purchase_approved_list(request):
    requests = PurchaseRequisition.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/purchase_approved_list.html', {'requests': requests})


@login_required
def purchase_posted_list(request):
    requests = PurchaseRequisition.objects.filter(is_posted=True, is_received=False).order_by('-created_at')
    return render(request, 'frontend/purchase_posted_list.html', {'requests': requests})


@login_required
def purchase_received_list(request):
    requests = PurchaseRequisition.objects.filter(is_received=True).order_by('-created_at')
    return render(request, 'frontend/purchase_received_list.html', {'requests': requests})


@login_required
def post_purchase_requisition(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Purchase requisition PR-{obj.id} posted successfully!')
    return redirect('purchase_approved_list')


@login_required
def receive_purchase_requisition(request, pk):
    obj = get_object_or_404(PurchaseRequisition, pk=pk)
    if request.method == 'POST':
        obj.is_received = True
        obj.received_by = request.user.username
        obj.received_at = timezone.now()
        obj.save()
        messages.success(request, f'Purchase requisition PR-{obj.id} marked as received!')
        return redirect('purchase_posted_list')
    return render(request, 'frontend/purchase_receive_modal.html', {'request': obj})


# ======================
# PETTY CASH
# ======================
@login_required
def petty_cash_request(request):
    requests = PettyCash.objects.filter(employee_name=request.user.get_full_name() or request.user.username).order_by('-created_at')
    if request.method == 'POST':
        form = PettyCashForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee_name = request.user.get_full_name() or request.user.username
            obj.employee_number = f"EMP{request.user.id:03d}"
            obj.status = "PENDING"
            obj.approval_level = "HOD"
            obj.petty_cash_number = f"PC{PettyCash.objects.count() + 1:03d}"
            obj.save()
            descriptions = request.POST.getlist('item_description[]')
            amounts = request.POST.getlist('item_amount[]')
            total = 0
            for i in range(len(descriptions)):
                desc = descriptions[i]
                amt = amounts[i]
                if desc and amt:
                    try:
                        amount = Decimal(amt)
                        total += amount
                        PettyCashItem.objects.create(petty_cash=obj, description=desc, amount=amount)
                    except Exception as e:
                        print(f"Error saving item: {e}")
            obj.amount = total
            obj.save()
            messages.success(request, 'Petty cash request created successfully! Waiting for HOD approval.')
            return redirect('petty_cash')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PettyCashForm()
    return render(request, 'frontend/petty_cash.html', {'form': form, 'requests': requests})


@login_required
def petty_cash_approval(request):
    requests = PettyCash.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/petty_cash_approval.html', {'requests': requests})


@login_required
def approve_petty_cash(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    obj.status = "APPROVED"
    obj.save()
    messages.success(request, 'Petty cash request approved!')
    return redirect('petty_cash_approval')


@login_required
def reject_petty_cash(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    obj.status = "REJECTED"
    obj.save()
    messages.success(request, 'Petty cash request rejected!')
    return redirect('petty_cash_approval')


@login_required
def cancel_petty_cash(request, id):
    obj = get_object_or_404(PettyCash, id=id)
    obj.status = "CANCELLED"
    obj.save()
    messages.success(request, 'Petty cash request cancelled!')
    return redirect('petty_cash')


# ======================
# PETTY CASH APPROVAL - MULTI LEVEL
# ======================
@login_required
def petty_cash_approval_hod(request):
    user_department = None
    if hasattr(request.user, 'userprofile'):
        user_department = request.user.userprofile.department
    if user_department:
        requests = PettyCash.objects.filter(
            department=user_department, approval_level='HOD', hod_approved=False, status='PENDING'
        ).order_by('-created_at')
    else:
        requests = PettyCash.objects.none()
        messages.warning(request, 'Your profile does not have a department assigned.')
    return render(request, 'frontend/petty_cash_approval_hod.html', {'requests': requests})


@login_required
def approve_petty_cash_hod(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    user_dept = request.user.userprofile.department if hasattr(request.user, 'userprofile') else None
    if user_dept != obj.department:
        messages.error(request, 'You are not authorized to approve this request.')
        return redirect('petty_cash_approval_hod')
    obj.hod_approved = True
    obj.hod_approved_by = request.user.username
    obj.hod_approved_at = timezone.now()
    obj.approval_level = 'FINANCE_OFFICER'
    obj.save()
    messages.success(request, f'Request {obj.petty_cash_number} approved. Sent to Finance Officer.')
    return redirect('petty_cash_approval_hod')


@login_required
def reject_petty_cash_hod(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Request {obj.petty_cash_number} rejected.')
        return redirect('petty_cash_approval_hod')
    return render(request, 'frontend/petty_cash_reject_modal.html', {'request': obj})


@login_required
def petty_cash_approval_finance_officer(request):
    requests = PettyCash.objects.filter(
        approval_level='FINANCE_OFFICER', hod_approved=True, finance_officer_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/petty_cash_approval_finance_officer.html', {'requests': requests})


@login_required
def approve_petty_cash_finance_officer(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    obj.finance_officer_approved = True
    obj.finance_officer_approved_by = request.user.username
    obj.finance_officer_approved_at = timezone.now()
    obj.approval_level = 'FINANCE_MANAGER'
    obj.save()
    messages.success(request, f'Request {obj.petty_cash_number} approved. Sent to Finance Manager.')
    return redirect('petty_cash_approval_finance_officer')


@login_required
def reject_petty_cash_finance_officer(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Request {obj.petty_cash_number} rejected.')
        return redirect('petty_cash_approval_finance_officer')
    return render(request, 'frontend/petty_cash_reject_modal.html', {'request': obj})


@login_required
def petty_cash_approval_finance_manager(request):
    requests = PettyCash.objects.filter(
        approval_level='FINANCE_MANAGER', hod_approved=True, finance_officer_approved=True, finance_manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/petty_cash_approval_finance_manager.html', {'requests': requests})


@login_required
def approve_petty_cash_finance_manager(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    obj.finance_manager_approved = True
    obj.finance_manager_approved_by = request.user.username
    obj.finance_manager_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Request {obj.petty_cash_number} approved. Sent to General Manager.')
    return redirect('petty_cash_approval_finance_manager')


@login_required
def reject_petty_cash_finance_manager(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Request {obj.petty_cash_number} rejected.')
        return redirect('petty_cash_approval_finance_manager')
    return render(request, 'frontend/petty_cash_reject_modal.html', {'request': obj})


@login_required
def petty_cash_approval_manager(request):
    requests = PettyCash.objects.filter(
        approval_level='MANAGER', hod_approved=True, finance_officer_approved=True, finance_manager_approved=True, manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/petty_cash_approval_manager.html', {'requests': requests})


@login_required
def approve_petty_cash_manager(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Request {obj.petty_cash_number} fully approved!')
    return redirect('petty_cash_approval_manager')


@login_required
def reject_petty_cash_manager(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Request {obj.petty_cash_number} rejected.')
        return redirect('petty_cash_approval_manager')
    return render(request, 'frontend/petty_cash_reject_modal.html', {'request': obj})


# ======================
# PETTY CASH POSTING & SURRENDER
# ======================
@login_required
def petty_cash_approved_list(request):
    requests = PettyCash.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/petty_cash_approved_list.html', {'requests': requests})


@login_required
def petty_cash_posted_list(request):
    requests = PettyCash.objects.filter(is_posted=True, is_surrendered=False).order_by('-created_at')
    return render(request, 'frontend/petty_cash_posted_list.html', {'requests': requests})


@login_required
def petty_cash_surrendered_list(request):
    requests = PettyCash.objects.filter(is_surrendered=True).order_by('-created_at')
    return render(request, 'frontend/petty_cash_surrendered_list.html', {'requests': requests})


@login_required
def post_petty_cash(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Petty cash {obj.petty_cash_number} posted successfully!')
    return redirect('petty_cash_approved_list')


@login_required
def surrender_petty_cash(request, pk):
    obj = get_object_or_404(PettyCash, pk=pk)
    if request.method == 'POST':
        balance_returned = request.POST.get('balance_returned', 0)
        obj.is_surrendered = True
        obj.surrendered_by = request.user.username
        obj.surrendered_at = timezone.now()
        obj.balance_returned = Decimal(balance_returned)
        obj.save()
        messages.success(request, f'Petty cash {obj.petty_cash_number} surrendered successfully!')
        return redirect('petty_cash_posted_list')
    return render(request, 'frontend/petty_cash_surrender_modal.html', {'request': obj})


# ======================
# IMPREST
# ======================
@login_required
def imprest(request):
    if request.method == "POST":
        form = ImprestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee_name = request.user.get_full_name() or request.user.username
            obj.status = "PENDING"
            obj.approval_level = "HOD"
            obj.imprest_number = f"IMP{Imprest.objects.count() + 1:03d}"
            obj.save()
            descriptions = request.POST.getlist('item_description[]')
            amounts = request.POST.getlist('item_amount[]')
            total = 0
            for i in range(len(descriptions)):
                desc = descriptions[i]
                amt = amounts[i]
                if desc and amt:
                    try:
                        amount = Decimal(amt)
                        total += amount
                        ImprestItem.objects.create(imprest=obj, description=desc, amount=amount)
                    except Exception as e:
                        print(f"Error saving imprest item: {e}")
            obj.amount = total
            obj.save()
            messages.success(request, 'Imprest request created successfully! Waiting for HOD approval.')
            return redirect('imprest')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ImprestForm()
    requests = Imprest.objects.all().order_by("-created_at")
    return render(request, "frontend/imprest.html", {"form": form, "requests": requests})


@login_required
def imprest_approval(request):
    requests = Imprest.objects.filter(status="PENDING").order_by("-created_at")
    return render(request, "frontend/imprest_approval.html", {"requests": requests})


@login_required
def approve_imprest(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    obj.status = "APPROVED"
    obj.save()
    messages.success(request, 'Imprest request approved!')
    return redirect('imprest_approval')


@login_required
def reject_imprest(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    obj.status = "REJECTED"
    obj.save()
    messages.success(request, 'Imprest request rejected!')
    return redirect('imprest_approval')


@login_required
def cancel_imprest(request, id):
    obj = get_object_or_404(Imprest, id=id)
    obj.status = "CANCELLED"
    obj.save()
    messages.success(request, 'Imprest request cancelled!')
    return redirect("imprest")


# ======================
# IMPREST APPROVAL - MULTI LEVEL
# ======================
@login_required
def imprest_approval_hod(request):
    user_department = None
    if hasattr(request.user, 'userprofile'):
        user_department = request.user.userprofile.department
    if user_department:
        requests = Imprest.objects.filter(
            department=user_department, approval_level='HOD', hod_approved=False, status='PENDING'
        ).order_by('-created_at')
    else:
        requests = Imprest.objects.none()
        messages.warning(request, 'Your profile does not have a department assigned.')
    return render(request, 'frontend/imprest_approval_hod.html', {'requests': requests})


@login_required
def approve_imprest_hod(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    obj.hod_approved = True
    obj.hod_approved_by = request.user.username
    obj.hod_approved_at = timezone.now()
    obj.approval_level = 'FINANCE_OFFICER'
    obj.save()
    messages.success(request, f'Imprest request {obj.imprest_number} approved. Sent to Finance Officer.')
    return redirect('imprest_approval_hod')


@login_required
def reject_imprest_hod(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Imprest request {obj.imprest_number} rejected.')
        return redirect('imprest_approval_hod')
    return render(request, 'frontend/imprest_reject_modal.html', {'request': obj})


@login_required
def imprest_approval_finance_officer(request):
    requests = Imprest.objects.filter(
        approval_level='FINANCE_OFFICER', hod_approved=True, finance_officer_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/imprest_approval_finance_officer.html', {'requests': requests})


@login_required
def approve_imprest_finance_officer(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    obj.finance_officer_approved = True
    obj.finance_officer_approved_by = request.user.username
    obj.finance_officer_approved_at = timezone.now()
    obj.approval_level = 'FINANCE_MANAGER'
    obj.save()
    messages.success(request, f'Imprest request {obj.imprest_number} approved. Sent to Finance Manager.')
    return redirect('imprest_approval_finance_officer')


@login_required
def reject_imprest_finance_officer(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Imprest request {obj.imprest_number} rejected.')
        return redirect('imprest_approval_finance_officer')
    return render(request, 'frontend/imprest_reject_modal.html', {'request': obj})


@login_required
def imprest_approval_finance_manager(request):
    requests = Imprest.objects.filter(
        approval_level='FINANCE_MANAGER', hod_approved=True, finance_officer_approved=True, finance_manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/imprest_approval_finance_manager.html', {'requests': requests})


@login_required
def approve_imprest_finance_manager(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    obj.finance_manager_approved = True
    obj.finance_manager_approved_by = request.user.username
    obj.finance_manager_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Imprest request {obj.imprest_number} approved. Sent to General Manager.')
    return redirect('imprest_approval_finance_manager')


@login_required
def reject_imprest_finance_manager(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Imprest request {obj.imprest_number} rejected.')
        return redirect('imprest_approval_finance_manager')
    return render(request, 'frontend/imprest_reject_modal.html', {'request': obj})


@login_required
def imprest_approval_manager(request):
    requests = Imprest.objects.filter(
        approval_level='MANAGER', hod_approved=True, finance_officer_approved=True, finance_manager_approved=True, manager_approved=False, status='PENDING'
    ).order_by('-created_at')
    return render(request, 'frontend/imprest_approval_manager.html', {'requests': requests})


@login_required
def approve_imprest_manager(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Imprest request {obj.imprest_number} fully approved!')
    return redirect('imprest_approval_manager')


@login_required
def reject_imprest_manager(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Imprest request {obj.imprest_number} rejected.')
        return redirect('imprest_approval_manager')
    return render(request, 'frontend/imprest_reject_modal.html', {'request': obj})


# ======================
# IMPREST POSTING & SURRENDER
# ======================
@login_required
def imprest_approved_list(request):
    requests = Imprest.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/imprest_approved_list.html', {'requests': requests})


@login_required
def imprest_posted_list(request):
    requests = Imprest.objects.filter(is_posted=True, is_surrendered=False).order_by('-created_at')
    return render(request, 'frontend/imprest_posted_list.html', {'requests': requests})


@login_required
def imprest_surrendered_list(request):
    requests = Imprest.objects.filter(is_surrendered=True).order_by('-created_at')
    return render(request, 'frontend/imprest_surrendered_list.html', {'requests': requests})


@login_required
def post_imprest(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Imprest {obj.imprest_number} posted successfully!')
    return redirect('imprest_approved_list')


@login_required
def surrender_imprest(request, pk):
    obj = get_object_or_404(Imprest, pk=pk)
    if request.method == 'POST':
        balance_returned = request.POST.get('balance_returned', 0)
        obj.is_surrendered = True
        obj.surrendered_by = request.user.username
        obj.surrendered_at = timezone.now()
        obj.balance_returned = Decimal(balance_returned)
        obj.save()
        messages.success(request, f'Imprest {obj.imprest_number} surrendered successfully!')
        return redirect('imprest_posted_list')
    return render(request, 'frontend/imprest_surrender_modal.html', {'request': obj})


# ======================
# SALARY ADVANCE
# ======================
@login_required
def salary_advance_request(request):
    if request.method == "POST":
        form = SalaryAdvanceForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.employee_name = request.user.get_full_name() or request.user.username
            obj.status = "PENDING"
            obj.approval_level = "HR"
            obj.salary_advance_number = f"SA{SalaryAdvance.objects.count() + 1:03d}"
            obj.save()
            messages.success(request, 'Salary advance request created successfully! Waiting for HR approval.')
            return redirect('salary_advance')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SalaryAdvanceForm()
    requests = SalaryAdvance.objects.filter(employee_name=request.user.get_full_name() or request.user.username).order_by("-created_at")
    return render(request, 'frontend/salary_advance.html', {"form": form, "requests": requests})


@login_required
def salary_advance_approval(request):
    requests = SalaryAdvance.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/salary_advance_approval.html', {'requests': requests})


@login_required
def approve_salary_advance(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    obj.status = "APPROVED"
    obj.save()
    messages.success(request, 'Salary advance request approved!')
    return redirect('salary_advance_approval')


@login_required
def reject_salary_advance(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    obj.status = "REJECTED"
    obj.save()
    messages.success(request, 'Salary advance request rejected!')
    return redirect('salary_advance_approval')


@login_required
def cancel_salary_advance(request, id):
    obj = get_object_or_404(SalaryAdvance, id=id)
    obj.status = "CANCELLED"
    obj.save()
    messages.success(request, 'Salary advance request cancelled!')
    return redirect('salary_advance')


# ======================
# SALARY ADVANCE APPROVAL - MULTI LEVEL
# ======================
@login_required
def salary_advance_approval_hr(request):
    requests = SalaryAdvance.objects.filter(approval_level='HR', hr_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/salary_advance_approval_hr.html', {'requests': requests})


@login_required
def approve_salary_advance_hr(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    obj.hr_approved = True
    obj.hr_approved_by = request.user.username
    obj.hr_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Salary advance request approved. Sent to General Manager.')
    return redirect('salary_advance_approval_hr')


@login_required
def reject_salary_advance_hr(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Salary advance request rejected.')
        return redirect('salary_advance_approval_hr')
    return render(request, 'frontend/salary_advance_reject_modal.html', {'request': obj})


@login_required
def salary_advance_approval_manager(request):
    requests = SalaryAdvance.objects.filter(approval_level='MANAGER', hr_approved=True, manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/salary_advance_approval_manager.html', {'requests': requests})


@login_required
def approve_salary_advance_manager(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Salary advance request fully approved!')
    return redirect('salary_advance_approval_manager')


@login_required
def reject_salary_advance_manager(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Salary advance request rejected.')
        return redirect('salary_advance_approval_manager')
    return render(request, 'frontend/salary_advance_reject_modal.html', {'request': obj})


# ======================
# SALARY ADVANCE POSTING & SETTLEMENT
# ======================
@login_required
def salary_advance_approved_list(request):
    requests = SalaryAdvance.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/salary_advance_approved_list.html', {'requests': requests})


@login_required
def salary_advance_posted_list(request):
    requests = SalaryAdvance.objects.filter(is_posted=True, is_settled=False).order_by('-created_at')
    return render(request, 'frontend/salary_advance_posted_list.html', {'requests': requests})


@login_required
def salary_advance_settled_list(request):
    requests = SalaryAdvance.objects.filter(is_settled=True).order_by('-created_at')
    return render(request, 'frontend/salary_advance_settled_list.html', {'requests': requests})


@login_required
def post_salary_advance(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Salary advance for {obj.employee_name} posted successfully!')
    return redirect('salary_advance_approved_list')


@login_required
def settle_salary_advance(request, pk):
    obj = get_object_or_404(SalaryAdvance, pk=pk)
    if request.method == 'POST':
        obj.is_settled = True
        obj.settled_by = request.user.username
        obj.settled_at = timezone.now()
        obj.save()
        messages.success(request, f'Salary advance for {obj.employee_name} settled successfully!')
        return redirect('salary_advance_posted_list')
    return render(request, 'frontend/salary_advance_settle_modal.html', {'request': obj})


# ======================
# FINANCE DASHBOARD
# ======================
@login_required
def finance_dashboard(request):
    return render(request, 'frontend/finance_dashboard.html')


# ======================
# IMPREST SURRENDER
# ======================
@login_required
def imprest_surrender_request(request):
    if request.method == "POST":
        ImprestSurrender.objects.create(
            imprest_id=request.POST.get("imprest_id"),
            amount_spent=request.POST.get("amount_spent"),
            balance_returned=request.POST.get("balance_returned"),
            status="PENDING"
        )
        messages.success(request, 'Imprest surrender submitted successfully!')
        return redirect('imprest_surrender')
    surrenders = ImprestSurrender.objects.filter(imprest__employee_name=request.user.get_full_name() or request.user.username).order_by('-created_at')
    return render(request, 'frontend/imprest_surrender.html', {'surrenders': surrenders})


@login_required
def imprest_surrender_approval(request):
    surrenders = ImprestSurrender.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/imprest_surrender_approval.html', {'surrenders': surrenders})


@login_required
def approve_imprest_surrender(request, pk):
    obj = get_object_or_404(ImprestSurrender, pk=pk)
    obj.status = "APPROVED"
    obj.save()
    messages.success(request, 'Imprest surrender approved!')
    return redirect('imprest_surrender_approval')


@login_required
def reject_imprest_surrender(request, pk):
    obj = get_object_or_404(ImprestSurrender, pk=pk)
    obj.status = "REJECTED"
    obj.save()
    messages.success(request, 'Imprest surrender rejected!')
    return redirect('imprest_surrender_approval')


# ======================
# FLEET MANAGEMENT
# ======================
@login_required
def fleet_management(request):
    return render(request, 'frontend/fleet_management.html')


@login_required
def transport_requisition(request):
    if request.method == "POST":
        employee_name = request.user.get_full_name() or request.user.username
        TransportRequisition.objects.create(
            employee_name=employee_name,
            department=request.POST.get('department', 'General'),
            destination=request.POST.get('destination'),
            date_required=request.POST.get('date_required'),
            purpose=request.POST.get('purpose', ''),
            status="PENDING",
            approval_level="FLEET_MANAGER"
        )
        messages.success(request, 'Transport requisition submitted successfully! Waiting for Fleet Manager approval.')
        return redirect('transport_requisition')
    employee_name = request.user.get_full_name() or request.user.username
    transports = TransportRequisition.objects.filter(employee_name=employee_name).order_by('-created_at')
    return render(request, 'frontend/transport_requisition.html', {'transports': transports})


@login_required
def transport_approval(request):
    transports = TransportRequisition.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/transport_approval.html', {'transports': transports})


@login_required
def update_transport_status(request, pk, status):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    obj.status = status.upper()
    obj.save()
    messages.success(request, f'Transport requisition {status.lower()}')
    return redirect('transport_approval')


# ======================
# TRANSPORT REQUISITION APPROVALS - FLEET
# ======================
@login_required
def transport_approval_fleet_manager(request):
    requests = TransportRequisition.objects.filter(approval_level='FLEET_MANAGER', fleet_manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/transport_approval_fleet_manager.html', {'requests': requests})


@login_required
def approve_transport_fleet_manager(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    obj.fleet_manager_approved = True
    obj.fleet_manager_approved_by = request.user.username
    obj.fleet_manager_approved_at = timezone.now()
    obj.approval_level = 'OPERATIONS_MANAGER'
    obj.save()
    messages.success(request, f'Transport request approved. Sent to Operations Manager.')
    return redirect('transport_approval_fleet_manager')


@login_required
def reject_transport_fleet_manager(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Transport request rejected.')
        return redirect('transport_approval_fleet_manager')
    return render(request, 'frontend/transport_reject_modal.html', {'request': obj})


@login_required
def transport_approval_operations_manager(request):
    requests = TransportRequisition.objects.filter(approval_level='OPERATIONS_MANAGER', fleet_manager_approved=True, operations_manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/transport_approval_operations_manager.html', {'requests': requests})


@login_required
def approve_transport_operations_manager(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    obj.operations_manager_approved = True
    obj.operations_manager_approved_by = request.user.username
    obj.operations_manager_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Transport request approved. Sent to General Manager.')
    return redirect('transport_approval_operations_manager')


@login_required
def reject_transport_operations_manager(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Transport request rejected.')
        return redirect('transport_approval_operations_manager')
    return render(request, 'frontend/transport_reject_modal.html', {'request': obj})


@login_required
def transport_approval_manager(request):
    requests = TransportRequisition.objects.filter(approval_level='MANAGER', fleet_manager_approved=True, operations_manager_approved=True, manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/transport_approval_manager.html', {'requests': requests})


@login_required
def approve_transport_manager(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Transport request fully approved!')
    return redirect('transport_approval_manager')


@login_required
def reject_transport_manager(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Transport request rejected.')
        return redirect('transport_approval_manager')
    return render(request, 'frontend/transport_reject_modal.html', {'request': obj})


# ======================
# TRANSPORT POSTING & COMPLETION
# ======================
@login_required
def transport_approved_list(request):
    requests = TransportRequisition.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/transport_approved_list.html', {'requests': requests})


@login_required
def transport_posted_list(request):
    requests = TransportRequisition.objects.filter(is_posted=True, is_completed=False).order_by('-created_at')
    return render(request, 'frontend/transport_posted_list.html', {'requests': requests})


@login_required
def transport_completed_list(request):
    requests = TransportRequisition.objects.filter(is_completed=True).order_by('-created_at')
    return render(request, 'frontend/transport_completed_list.html', {'requests': requests})


@login_required
def post_transport_requisition(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Transport requisition {obj.id} posted successfully!')
    return redirect('transport_approved_list')


@login_required
def complete_transport_requisition(request, pk):
    obj = get_object_or_404(TransportRequisition, pk=pk)
    if request.method == 'POST':
        obj.is_completed = True
        obj.completed_by = request.user.username
        obj.completed_at = timezone.now()
        obj.save()
        messages.success(request, f'Transport requisition {obj.id} marked as completed!')
        return redirect('transport_posted_list')
    return render(request, 'frontend/transport_complete_modal.html', {'request': obj})


# ======================
# WORK TICKET
# ======================
@login_required
def work_ticket(request):
    employee_name = request.user.get_full_name() or request.user.username
    tickets = WorkTicket.objects.filter(employee_name=employee_name).order_by('-created_at')
    if request.method == "POST":
        edit_id = request.POST.get('edit_id')
        if edit_id:
            obj = get_object_or_404(WorkTicket, id=edit_id)
            obj.department = request.POST.get('department', obj.department)
            obj.destination = request.POST.get('destination', obj.destination)
            obj.date_required = request.POST.get('date_required', obj.date_required)
            obj.purpose = request.POST.get('purpose', obj.purpose)
            if request.FILES.get('document'):
                obj.document = request.FILES.get('document')
            obj.save()
            messages.success(request, 'Work ticket updated successfully!')
        else:
            WorkTicket.objects.create(
                employee_name=employee_name,
                employee_number=f"EMP{request.user.id:03d}",
                department=request.POST.get('department', 'General'),
                destination=request.POST.get('destination'),
                date_required=request.POST.get('date_required'),
                purpose=request.POST.get('purpose', ''),
                document=request.FILES.get('document'),
                status="PENDING",
                approval_level="FLEET_MANAGER"
            )
            messages.success(request, 'Work ticket created successfully! Waiting for Fleet Manager approval.')
        return redirect('work_ticket')
    return render(request, 'frontend/work_ticket.html', {'tickets': tickets})


@login_required
def work_ticket_approval(request):
    tickets = WorkTicket.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/work_ticket_approval.html', {'tickets': tickets})


@login_required
def update_work_ticket_status(request, pk, status):
    obj = get_object_or_404(WorkTicket, pk=pk)
    obj.status = status.upper()
    obj.save()
    messages.success(request, f'Work ticket {status.lower()}')
    return redirect('work_ticket_approval')


@login_required
def cancel_work_ticket(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    obj.status = "CANCELLED"
    obj.save()
    messages.success(request, 'Work ticket cancelled successfully!')
    return redirect('work_ticket')


# ======================
# WORK TICKET APPROVALS - FLEET
# ======================
@login_required
def work_ticket_approval_fleet_manager(request):
    requests = WorkTicket.objects.filter(approval_level='FLEET_MANAGER', fleet_manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/work_ticket_approval_fleet_manager.html', {'requests': requests})


@login_required
def approve_work_ticket_fleet_manager(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    obj.fleet_manager_approved = True
    obj.fleet_manager_approved_by = request.user.username
    obj.fleet_manager_approved_at = timezone.now()
    obj.approval_level = 'OPERATIONS_MANAGER'
    obj.save()
    messages.success(request, f'Work ticket approved. Sent to Operations Manager.')
    return redirect('work_ticket_approval_fleet_manager')


@login_required
def reject_work_ticket_fleet_manager(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Work ticket rejected.')
        return redirect('work_ticket_approval_fleet_manager')
    return render(request, 'frontend/work_ticket_reject_modal.html', {'request': obj})


@login_required
def work_ticket_approval_operations_manager(request):
    requests = WorkTicket.objects.filter(approval_level='OPERATIONS_MANAGER', fleet_manager_approved=True, operations_manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/work_ticket_approval_operations_manager.html', {'requests': requests})


@login_required
def approve_work_ticket_operations_manager(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    obj.operations_manager_approved = True
    obj.operations_manager_approved_by = request.user.username
    obj.operations_manager_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Work ticket approved. Sent to General Manager.')
    return redirect('work_ticket_approval_operations_manager')


@login_required
def reject_work_ticket_operations_manager(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Work ticket rejected.')
        return redirect('work_ticket_approval_operations_manager')
    return render(request, 'frontend/work_ticket_reject_modal.html', {'request': obj})


@login_required
def work_ticket_approval_manager(request):
    requests = WorkTicket.objects.filter(approval_level='MANAGER', fleet_manager_approved=True, operations_manager_approved=True, manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/work_ticket_approval_manager.html', {'requests': requests})


@login_required
def approve_work_ticket_manager(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Work ticket fully approved!')
    return redirect('work_ticket_approval_manager')


@login_required
def reject_work_ticket_manager(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Work ticket rejected.')
        return redirect('work_ticket_approval_manager')
    return render(request, 'frontend/work_ticket_reject_modal.html', {'request': obj})


# ======================
# WORK TICKET POSTING & COMPLETION
# ======================
@login_required
def work_ticket_approved_list(request):
    requests = WorkTicket.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/work_ticket_approved_list.html', {'requests': requests})


@login_required
def work_ticket_posted_list(request):
    requests = WorkTicket.objects.filter(is_posted=True, is_completed=False).order_by('-created_at')
    return render(request, 'frontend/work_ticket_posted_list.html', {'requests': requests})


@login_required
def work_ticket_completed_list(request):
    requests = WorkTicket.objects.filter(is_completed=True).order_by('-created_at')
    return render(request, 'frontend/work_ticket_completed_list.html', {'requests': requests})


@login_required
def post_work_ticket(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Work ticket {obj.id} posted successfully!')
    return redirect('work_ticket_approved_list')


@login_required
def complete_work_ticket(request, pk):
    obj = get_object_or_404(WorkTicket, pk=pk)
    if request.method == 'POST':
        obj.is_completed = True
        obj.completed_by = request.user.username
        obj.completed_at = timezone.now()
        obj.save()
        messages.success(request, f'Work ticket {obj.id} marked as completed!')
        return redirect('work_ticket_posted_list')
    return render(request, 'frontend/work_ticket_complete_modal.html', {'request': obj})


# ======================
# FUEL REQUISITION
# ======================
@login_required
def fuel_requisition(request):
    if request.method == "POST":
        edit_id = request.POST.get('edit_id')
        if edit_id:
            obj = get_object_or_404(FuelRequisition, id=edit_id)
            obj.employee_number = request.POST.get('employee_number', obj.employee_number)
            obj.employee_name = request.POST.get('employee_name', obj.employee_name)
            obj.department = request.POST.get('department', obj.department)
            obj.destination = request.POST.get('destination', obj.destination)
            obj.date_required = request.POST.get('date_required', obj.date_required)
            obj.purpose = request.POST.get('purpose', obj.purpose)
            obj.save()
            messages.success(request, 'Fuel requisition updated successfully!')
            return redirect('fuel_requisition')
        else:
            try:
                FuelRequisition.objects.create(
                    requested_by=request.user.username,
                    employee_number=request.POST.get('employee_number', f"EMP{request.user.id:03d}"),
                    employee_name=request.POST.get('employee_name', request.user.get_full_name() or request.user.username),
                    department=request.POST.get('department', 'General'),
                    destination=request.POST.get('destination', ''),
                    date_required=request.POST.get('date_required'),
                    purpose=request.POST.get('purpose', ''),
                    document=request.FILES.get('document'),
                    status="PENDING",
                    approval_level="FLEET_MANAGER"
                )
                messages.success(request, 'Fuel requisition submitted successfully! Waiting for Fleet Manager approval.')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
            return redirect('fuel_requisition')
    requests = FuelRequisition.objects.all().order_by('-created_at')
    return render(request, 'frontend/fuel_requisition.html', {'requests': requests})


@login_required
def fuel_requisition_approval(request):
    requests = FuelRequisition.objects.filter(status='PENDING').order_by('-created_at')
    return render(request, 'frontend/fuel_requisition_approval.html', {'requests': requests})


@login_required
def approve_fuel_requisition(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    obj.status = "APPROVED"
    obj.save()
    messages.success(request, 'Fuel requisition approved!')
    return redirect('fuel_requisition_approval')


@login_required
def reject_fuel_requisition(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    obj.status = "REJECTED"
    obj.save()
    messages.success(request, 'Fuel requisition rejected!')
    return redirect('fuel_requisition_approval')


# ======================
# FUEL REQUISITION APPROVALS - FLEET
# ======================
@login_required
def fuel_requisition_approval_fleet_manager(request):
    requests = FuelRequisition.objects.filter(approval_level='FLEET_MANAGER', fleet_manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/fuel_requisition_approval_fleet_manager.html', {'requests': requests})


@login_required
def approve_fuel_requisition_fleet_manager(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    obj.fleet_manager_approved = True
    obj.fleet_manager_approved_by = request.user.username
    obj.fleet_manager_approved_at = timezone.now()
    obj.approval_level = 'OPERATIONS_MANAGER'
    obj.save()
    messages.success(request, f'Fuel requisition approved. Sent to Operations Manager.')
    return redirect('fuel_requisition_approval_fleet_manager')


@login_required
def reject_fuel_requisition_fleet_manager(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Fuel requisition rejected.')
        return redirect('fuel_requisition_approval_fleet_manager')
    return render(request, 'frontend/fuel_requisition_reject_modal.html', {'request': obj})


@login_required
def fuel_requisition_approval_operations_manager(request):
    requests = FuelRequisition.objects.filter(approval_level='OPERATIONS_MANAGER', fleet_manager_approved=True, operations_manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/fuel_requisition_approval_operations_manager.html', {'requests': requests})


@login_required
def approve_fuel_requisition_operations_manager(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    obj.operations_manager_approved = True
    obj.operations_manager_approved_by = request.user.username
    obj.operations_manager_approved_at = timezone.now()
    obj.approval_level = 'MANAGER'
    obj.save()
    messages.success(request, f'Fuel requisition approved. Sent to General Manager.')
    return redirect('fuel_requisition_approval_operations_manager')


@login_required
def reject_fuel_requisition_operations_manager(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Fuel requisition rejected.')
        return redirect('fuel_requisition_approval_operations_manager')
    return render(request, 'frontend/fuel_requisition_reject_modal.html', {'request': obj})


@login_required
def fuel_requisition_approval_manager(request):
    requests = FuelRequisition.objects.filter(approval_level='MANAGER', fleet_manager_approved=True, operations_manager_approved=True, manager_approved=False, status='PENDING').order_by('-created_at')
    return render(request, 'frontend/fuel_requisition_approval_manager.html', {'requests': requests})


@login_required
def approve_fuel_requisition_manager(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    obj.manager_approved = True
    obj.manager_approved_by = request.user.username
    obj.manager_approved_at = timezone.now()
    obj.approval_level = 'APPROVED'
    obj.status = 'APPROVED'
    obj.save()
    messages.success(request, f'Fuel requisition fully approved!')
    return redirect('fuel_requisition_approval_manager')


@login_required
def reject_fuel_requisition_manager(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    if request.method == 'POST':
        reason = request.POST.get('rejection_reason', 'No reason provided')
        obj.status = 'REJECTED'
        obj.approval_level = 'REJECTED'
        obj.rejection_reason = reason
        obj.rejected_by = request.user.username
        obj.rejected_at = timezone.now()
        obj.save()
        messages.error(request, f'Fuel requisition rejected.')
        return redirect('fuel_requisition_approval_manager')
    return render(request, 'frontend/fuel_requisition_reject_modal.html', {'request': obj})


# ======================
# FUEL REQUISITION POSTING & COMPLETION
# ======================
@login_required
def fuel_requisition_approved_list(request):
    requests = FuelRequisition.objects.filter(status='APPROVED', is_posted=False).order_by('-created_at')
    return render(request, 'frontend/fuel_requisition_approved_list.html', {'requests': requests})


@login_required
def fuel_requisition_posted_list(request):
    requests = FuelRequisition.objects.filter(is_posted=True, is_completed=False).order_by('-created_at')
    return render(request, 'frontend/fuel_requisition_posted_list.html', {'requests': requests})


@login_required
def fuel_requisition_completed_list(request):
    requests = FuelRequisition.objects.filter(is_completed=True).order_by('-created_at')
    return render(request, 'frontend/fuel_requisition_completed_list.html', {'requests': requests})


@login_required
def post_fuel_requisition(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    obj.is_posted = True
    obj.posted_by = request.user.username
    obj.posted_at = timezone.now()
    obj.save()
    messages.success(request, f'Fuel requisition {obj.id} posted successfully!')
    return redirect('fuel_requisition_approved_list')


@login_required
def complete_fuel_requisition(request, pk):
    obj = get_object_or_404(FuelRequisition, pk=pk)
    if request.method == 'POST':
        obj.is_completed = True
        obj.completed_by = request.user.username
        obj.completed_at = timezone.now()
        obj.save()
        messages.success(request, f'Fuel requisition {obj.id} marked as completed!')
        return redirect('fuel_requisition_posted_list')
    return render(request, 'frontend/fuel_requisition_complete_modal.html', {'request': obj})