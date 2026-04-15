from django.urls import path
from . import views

urlpatterns = [

    # ======================
    # DASHBOARD
    # ======================
    path('', views.dashboard, name='dashboard'),

    # ======================
    # PROCUREMENT MODULE
    # ======================
    # Store Requisition - Regular
    path('procurement/store-requisition/', views.store_requisition, name='store_requisition'),
    path('procurement/store-requisition/<int:pk>/cancel/', views.cancel_store_requisition, name='cancel_store_requisition'),
    
    # Store Requisition - Old Approval (backward compatibility)
    path('procurement/store-approval/', views.store_approval, name='store_approval'),
    path('procurement/store-approval/<int:pk>/approve/', views.approve_store_requisition, name='approve_store'),
    path('procurement/store-approval/<int:pk>/reject/', views.reject_store_requisition, name='reject_store'),
    
    # Store Requisition - Multi-Level Approval
    path('procurement/store/approval/hod/', views.store_approval_hod, name='store_approval_hod'),
    path('procurement/store/approval/hod/<int:pk>/approve/', views.approve_store_hod, name='approve_store_hod'),
    path('procurement/store/approval/hod/<int:pk>/reject/', views.reject_store_hod, name='reject_store_hod'),
    
    path('procurement/store/approval/procurement-officer/', views.store_approval_procurement_officer, name='store_approval_procurement_officer'),
    path('procurement/store/approval/procurement-officer/<int:pk>/approve/', views.approve_store_procurement_officer, name='approve_store_procurement_officer'),
    path('procurement/store/approval/procurement-officer/<int:pk>/reject/', views.reject_store_procurement_officer, name='reject_store_procurement_officer'),
    
    path('procurement/store/approval/procurement-manager/', views.store_approval_procurement_manager, name='store_approval_procurement_manager'),
    path('procurement/store/approval/procurement-manager/<int:pk>/approve/', views.approve_store_procurement_manager, name='approve_store_procurement_manager'),
    path('procurement/store/approval/procurement-manager/<int:pk>/reject/', views.reject_store_procurement_manager, name='reject_store_procurement_manager'),
    
    path('procurement/store/approval/manager/', views.store_approval_manager, name='store_approval_manager'),
    path('procurement/store/approval/manager/<int:pk>/approve/', views.approve_store_manager, name='approve_store_manager'),
    path('procurement/store/approval/manager/<int:pk>/reject/', views.reject_store_manager, name='reject_store_manager'),
    path('procurement/store/approved-list/', views.store_approved_list, name='store_approved_list'),
    path('procurement/store/posted-list/', views.store_posted_list, name='store_posted_list'),
    path('procurement/store/received-list/', views.store_received_list, name='store_received_list'),
    path('procurement/store/<int:pk>/post/', views.post_store_requisition, name='post_store_requisition'),
    path('procurement/store/<int:pk>/receive/', views.receive_store_requisition, name='receive_store_requisition'),
    # Purchase Requisition - Regular
    path('procurement/purchase-requisition/', views.purchase_requisition, name='purchase_requisition'),
    path('procurement/purchase-requisition/<int:pk>/cancel/', views.cancel_purchase_requisition, name='cancel_purchase_requisition'),
    
    # Purchase Requisition - Old Approval (backward compatibility)
    path('procurement/purchase-approval/', views.purchase_approval, name='purchase_approval'),
    path('procurement/purchase-approval/<int:pk>/approve/', views.approve_purchase_requisition, name='approve_purchase'),
    path('procurement/purchase-approval/<int:pk>/reject/', views.reject_purchase_requisition, name='reject_purchase'),
    
    # Purchase Requisition - Multi-Level Approval
    path('procurement/purchase/approval/hod/', views.purchase_approval_hod, name='purchase_approval_hod'),
    path('procurement/purchase/approval/hod/<int:pk>/approve/', views.approve_purchase_hod, name='approve_purchase_hod'),
    path('procurement/purchase/approval/hod/<int:pk>/reject/', views.reject_purchase_hod, name='reject_purchase_hod'),
    
    path('procurement/purchase/approval/procurement-officer/', views.purchase_approval_procurement_officer, name='purchase_approval_procurement_officer'),
    path('procurement/purchase/approval/procurement-officer/<int:pk>/approve/', views.approve_purchase_procurement_officer, name='approve_purchase_procurement_officer'),
    path('procurement/purchase/approval/procurement-officer/<int:pk>/reject/', views.reject_purchase_procurement_officer, name='reject_purchase_procurement_officer'),
    
    path('procurement/purchase/approval/procurement-manager/', views.purchase_approval_procurement_manager, name='purchase_approval_procurement_manager'),
    path('procurement/purchase/approval/procurement-manager/<int:pk>/approve/', views.approve_purchase_procurement_manager, name='approve_purchase_procurement_manager'),
    path('procurement/purchase/approval/procurement-manager/<int:pk>/reject/', views.reject_purchase_procurement_manager, name='reject_purchase_procurement_manager'),
    
    path('procurement/purchase/approval/manager/', views.purchase_approval_manager, name='purchase_approval_manager'),
    path('procurement/purchase/approval/manager/<int:pk>/approve/', views.approve_purchase_manager, name='approve_purchase_manager'),
    path('procurement/purchase/approval/manager/<int:pk>/reject/', views.reject_purchase_manager, name='reject_purchase_manager'),
    
    path('procurement/purchase/approved-list/', views.purchase_approved_list, name='purchase_approved_list'),
    path('procurement/purchase/posted-list/', views.purchase_posted_list, name='purchase_posted_list'),
    path('procurement/purchase/received-list/', views.purchase_received_list, name='purchase_received_list'),
    path('procurement/purchase/<int:pk>/post/', views.post_purchase_requisition, name='post_purchase_requisition'),
    path('procurement/purchase/<int:pk>/receive/', views.receive_purchase_requisition, name='receive_purchase_requisition'),
    # ======================
    # HR MODULE
    # ======================
    path('hr/', views.hr, name='hr'),
    path('hr/leave/apply/', views.apply_leave, name='leave_apply'),
    path('hr/leave/approval/', views.leave_approval, name='leave_approval'),
    path('hr/leave/approval/<int:pk>/approve/', views.approve_leave, name='approve_leave'),
    path('hr/leave/approval/<int:pk>/reject/', views.reject_leave, name='reject_leave'),

    path('hr/payslips/', views.payslips, name='payslips'),
    path('hr/overtime/', views.overtime, name='overtime'),
    path('hr/overtime/approval/', views.overtime_approval, name='overtime_approval'),
    path('hr/overtime/<int:pk>/approve/', views.approve_overtime, name='approve_overtime'),
    path('hr/overtime/<int:pk>/reject/', views.reject_overtime, name='reject_overtime'),
    path('hr/overtime/<int:pk>/cancel/', views.cancel_overtime, name='cancel_overtime'),
    path('hr/profile/', views.profile, name='profile'),
    path('hr/attendance/', views.attendance, name='attendance'),
    
    # Leave Multi-Level Approval
    path('hr/leave/approval/hod/', views.leave_approval_hod, name='leave_approval_hod'),
    path('hr/leave/approval/hod/<int:pk>/approve/', views.approve_leave_hod, name='approve_leave_hod'),
    path('hr/leave/approval/hod/<int:pk>/reject/', views.reject_leave_hod, name='reject_leave_hod'),

    path('hr/leave/approval/hr/', views.leave_approval_hr, name='leave_approval_hr'),
    path('hr/leave/approval/hr/<int:pk>/approve/', views.approve_leave_hr, name='approve_leave_hr'),
    path('hr/leave/approval/hr/<int:pk>/reject/', views.reject_leave_hr, name='reject_leave_hr'),

    path('hr/leave/approval/manager/', views.leave_approval_manager, name='leave_approval_manager'),
    path('hr/leave/approval/manager/<int:pk>/approve/', views.approve_leave_manager, name='approve_leave_manager'),
    path('hr/leave/approval/manager/<int:pk>/reject/', views.reject_leave_manager, name='reject_leave_manager'),

    # Overtime Multi-Level Approval
    path('hr/overtime/approval/hod/', views.overtime_approval_hod, name='overtime_approval_hod'),
    path('hr/overtime/approval/hod/<int:pk>/approve/', views.approve_overtime_hod, name='approve_overtime_hod'),
    path('hr/overtime/approval/hod/<int:pk>/reject/', views.reject_overtime_hod, name='reject_overtime_hod'),

    path('hr/overtime/approval/hr/', views.overtime_approval_hr, name='overtime_approval_hr'),
    path('hr/overtime/approval/hr/<int:pk>/approve/', views.approve_overtime_hr, name='approve_overtime_hr'),
    path('hr/overtime/approval/hr/<int:pk>/reject/', views.reject_overtime_hr, name='reject_overtime_hr'),

    path('hr/overtime/approval/manager/', views.overtime_approval_manager, name='overtime_approval_manager'),
    path('hr/overtime/approval/manager/<int:pk>/approve/', views.approve_overtime_manager, name='approve_overtime_manager'),
    path('hr/overtime/approval/manager/<int:pk>/reject/', views.reject_overtime_manager, name='reject_overtime_manager'),
    
     # Leave Posting & Settlement
path('hr/leave/approved-list/', views.leave_approved_list, name='leave_approved_list'),
path('hr/leave/posted-list/', views.leave_posted_list, name='leave_posted_list'),
path('hr/leave/settled-list/', views.leave_settled_list, name='leave_settled_list'),
path('hr/leave/<int:pk>/post/', views.post_leave, name='post_leave'),
path('hr/leave/<int:pk>/settle/', views.settle_leave, name='settle_leave'),

# Overtime Posting & Settlement
path('hr/overtime/approved-list/', views.overtime_approved_list, name='overtime_approved_list'),
path('hr/overtime/posted-list/', views.overtime_posted_list, name='overtime_posted_list'),
path('hr/overtime/settled-list/', views.overtime_settled_list, name='overtime_settled_list'),
path('hr/overtime/<int:pk>/post/', views.post_overtime, name='post_overtime'),
path('hr/overtime/<int:pk>/settle/', views.settle_overtime, name='settle_overtime'),
    # ======================
    # FINANCE MODULE
    # ======================
    path('finance/', views.finance_dashboard, name='finance'),

    # Requests
    path('finance/petty-cash/', views.petty_cash_request, name='petty_cash'),
    path('finance/imprest/', views.imprest, name='imprest'),
    path('finance/salary-advance/', views.salary_advance_request, name='salary_advance'),

    # Approvals - Old (backward compatibility)
    path('finance/petty-cash-approval/', views.petty_cash_approval, name='petty_cash_approval'),
    path('finance/imprest-approval/', views.imprest_approval, name='imprest_approval'),
    path('finance/salary-advance-approval/', views.salary_advance_approval, name='salary_advance_approval'),

    # Approve - Old
    path('finance/petty-cash/<int:pk>/approve/', views.approve_petty_cash, name='approve_petty_cash'),
    path('finance/imprest/<int:pk>/approve/', views.approve_imprest, name='approve_imprest'),
    path('finance/salary-advance/<int:pk>/approve/', views.approve_salary_advance, name='approve_salary_advance'),

    # Reject - Old
    path('finance/petty-cash/<int:pk>/reject/', views.reject_petty_cash, name='reject_petty_cash'),
    path('finance/imprest/<int:pk>/reject/', views.reject_imprest, name='reject_imprest'),
    path('finance/salary-advance/<int:pk>/reject/', views.reject_salary_advance, name='reject_salary_advance'),

    # Cancel
    path('finance/petty-cash/cancel/<int:id>/', views.cancel_petty_cash, name='cancel_petty_cash'),
    path('finance/imprest/cancel/<int:id>/', views.cancel_imprest, name='cancel_imprest'),
    path('finance/salary-advance/cancel/<int:id>/', views.cancel_salary_advance, name='cancel_salary_advance'),

    # Imprest Surrender
    path('finance/imprest-surrender/', views.imprest_surrender_request, name='imprest_surrender'),
    path('finance/imprest-surrender-approval/', views.imprest_surrender_approval, name='imprest_surrender_approval'),
    path('finance/imprest-surrender/<int:pk>/approve/', views.approve_imprest_surrender, name='approve_imprest_surrender'),
    path('finance/imprest-surrender/<int:pk>/reject/', views.reject_imprest_surrender, name='reject_imprest_surrender'),

    # Petty Cash Multi-Level Approval
    path('finance/petty-cash/approval/hod/', views.petty_cash_approval_hod, name='petty_cash_approval_hod'),
    path('finance/petty-cash/approval/hod/<int:pk>/approve/', views.approve_petty_cash_hod, name='approve_petty_cash_hod'),
    path('finance/petty-cash/approval/hod/<int:pk>/reject/', views.reject_petty_cash_hod, name='reject_petty_cash_hod'),

    path('finance/petty-cash/approval/finance-officer/', views.petty_cash_approval_finance_officer, name='petty_cash_approval_finance_officer'),
    path('finance/petty-cash/approval/finance-officer/<int:pk>/approve/', views.approve_petty_cash_finance_officer, name='approve_petty_cash_finance_officer'),
    path('finance/petty-cash/approval/finance-officer/<int:pk>/reject/', views.reject_petty_cash_finance_officer, name='reject_petty_cash_finance_officer'),

    path('finance/petty-cash/approval/finance-manager/', views.petty_cash_approval_finance_manager, name='petty_cash_approval_finance_manager'),
    path('finance/petty-cash/approval/finance-manager/<int:pk>/approve/', views.approve_petty_cash_finance_manager, name='approve_petty_cash_finance_manager'),
    path('finance/petty-cash/approval/finance-manager/<int:pk>/reject/', views.reject_petty_cash_finance_manager, name='reject_petty_cash_finance_manager'),

    path('finance/petty-cash/approval/manager/', views.petty_cash_approval_manager, name='petty_cash_approval_manager'),
    path('finance/petty-cash/approval/manager/<int:pk>/approve/', views.approve_petty_cash_manager, name='approve_petty_cash_manager'),
    path('finance/petty-cash/approval/manager/<int:pk>/reject/', views.reject_petty_cash_manager, name='reject_petty_cash_manager'),
# Petty Cash Posting & Surrender
    path('finance/petty-cash/approved/', views.petty_cash_approved_list, name='petty_cash_approved_list'),
    path('finance/petty-cash/posted/', views.petty_cash_posted_list, name='petty_cash_posted_list'),
    path('finance/petty-cash/surrendered/', views.petty_cash_surrendered_list, name='petty_cash_surrendered_list'),
    path('finance/petty-cash/<int:pk>/post/', views.post_petty_cash, name='post_petty_cash'),
    path('finance/petty-cash/<int:pk>/surrender/', views.surrender_petty_cash, name='surrender_petty_cash'),
    # Imprest Multi-Level Approval
    path('finance/imprest/approval/hod/', views.imprest_approval_hod, name='imprest_approval_hod'),
    path('finance/imprest/approval/hod/<int:pk>/approve/', views.approve_imprest_hod, name='approve_imprest_hod'),
    path('finance/imprest/approval/hod/<int:pk>/reject/', views.reject_imprest_hod, name='reject_imprest_hod'),

    path('finance/imprest/approval/finance-officer/', views.imprest_approval_finance_officer, name='imprest_approval_finance_officer'),
    path('finance/imprest/approval/finance-officer/<int:pk>/approve/', views.approve_imprest_finance_officer, name='approve_imprest_finance_officer'),
    path('finance/imprest/approval/finance-officer/<int:pk>/reject/', views.reject_imprest_finance_officer, name='reject_imprest_finance_officer'),

    path('finance/imprest/approval/finance-manager/', views.imprest_approval_finance_manager, name='imprest_approval_finance_manager'),
    path('finance/imprest/approval/finance-manager/<int:pk>/approve/', views.approve_imprest_finance_manager, name='approve_imprest_finance_manager'),
    path('finance/imprest/approval/finance-manager/<int:pk>/reject/', views.reject_imprest_finance_manager, name='reject_imprest_finance_manager'),

    path('finance/imprest/approval/manager/', views.imprest_approval_manager, name='imprest_approval_manager'),
    path('finance/imprest/approval/manager/<int:pk>/approve/', views.approve_imprest_manager, name='approve_imprest_manager'),
    path('finance/imprest/approval/manager/<int:pk>/reject/', views.reject_imprest_manager, name='reject_imprest_manager'),

    # Salary Advance Multi-Level Approval
    path('finance/salary-advance/approval/hr/', views.salary_advance_approval_hr, name='salary_advance_approval_hr'),
    path('finance/salary-advance/approval/hr/<int:pk>/approve/', views.approve_salary_advance_hr, name='approve_salary_advance_hr'),
    path('finance/salary-advance/approval/hr/<int:pk>/reject/', views.reject_salary_advance_hr, name='reject_salary_advance_hr'),

    path('finance/salary-advance/approval/manager/', views.salary_advance_approval_manager, name='salary_advance_approval_manager'),
    path('finance/salary-advance/approval/manager/<int:pk>/approve/', views.approve_salary_advance_manager, name='approve_salary_advance_manager'),
    path('finance/salary-advance/approval/manager/<int:pk>/reject/', views.reject_salary_advance_manager, name='reject_salary_advance_manager'),
    
    # Petty Cash Posting & Surrender
path('finance/petty-cash/approved-list/', views.petty_cash_approved_list, name='petty_cash_approved_list'),
path('finance/petty-cash/posted-list/', views.petty_cash_posted_list, name='petty_cash_posted_list'),
path('finance/petty-cash/surrendered-list/', views.petty_cash_surrendered_list, name='petty_cash_surrendered_list'),
path('finance/petty-cash/<int:pk>/post/', views.post_petty_cash, name='post_petty_cash'),
path('finance/petty-cash/<int:pk>/surrender/', views.surrender_petty_cash, name='surrender_petty_cash'),

# Imprest Posting & Surrender
path('finance/imprest/approved-list/', views.imprest_approved_list, name='imprest_approved_list'),
path('finance/imprest/posted-list/', views.imprest_posted_list, name='imprest_posted_list'),
path('finance/imprest/surrendered-list/', views.imprest_surrendered_list, name='imprest_surrendered_list'),
path('finance/imprest/<int:pk>/post/', views.post_imprest, name='post_imprest'),
path('finance/imprest/<int:pk>/surrender/', views.surrender_imprest, name='surrender_imprest'),
    # Imprest Posting & Surrender
path('finance/imprest/approved-list/', views.imprest_approved_list, name='imprest_approved_list'),
path('finance/imprest/posted-list/', views.imprest_posted_list, name='imprest_posted_list'),
path('finance/imprest/surrendered-list/', views.imprest_surrendered_list, name='imprest_surrendered_list'),
path('finance/imprest/<int:pk>/post/', views.post_imprest, name='post_imprest'),
path('finance/imprest/<int:pk>/surrender/', views.surrender_imprest, name='surrender_imprest'),
# Salary Advance Posting & Settlement
path('finance/salary-advance/approved-list/', views.salary_advance_approved_list, name='salary_advance_approved_list'),
path('finance/salary-advance/posted-list/', views.salary_advance_posted_list, name='salary_advance_posted_list'),
path('finance/salary-advance/settled-list/', views.salary_advance_settled_list, name='salary_advance_settled_list'),
path('finance/salary-advance/<int:pk>/post/', views.post_salary_advance, name='post_salary_advance'),
path('finance/salary-advance/<int:pk>/settle/', views.settle_salary_advance, name='settle_salary_advance'),

    # ======================
    # FLEET MANAGEMENT
    # ======================
    path('fleet-management/', views.fleet_management, name='fleet_management'),

    # Transport Requisition - Regular
    path('fleet/transport-requisition/', views.transport_requisition, name='transport_requisition'),
    path('fleet/transport-approval/', views.transport_approval, name='transport_approval'),
    path('fleet/transport/update/<int:pk>/<str:status>/', views.update_transport_status, name='update_transport_status'),

    # Transport Requisition - Multi-Level Approval
    path('fleet/transport/approval/fleet-manager/', views.transport_approval_fleet_manager, name='transport_approval_fleet_manager'),
    path('fleet/transport/approval/fleet-manager/<int:pk>/approve/', views.approve_transport_fleet_manager, name='approve_transport_fleet_manager'),
    path('fleet/transport/approval/fleet-manager/<int:pk>/reject/', views.reject_transport_fleet_manager, name='reject_transport_fleet_manager'),

    path('fleet/transport/approval/operations-manager/', views.transport_approval_operations_manager, name='transport_approval_operations_manager'),
    path('fleet/transport/approval/operations-manager/<int:pk>/approve/', views.approve_transport_operations_manager, name='approve_transport_operations_manager'),
    path('fleet/transport/approval/operations-manager/<int:pk>/reject/', views.reject_transport_operations_manager, name='reject_transport_operations_manager'),

    path('fleet/transport/approval/manager/', views.transport_approval_manager, name='transport_approval_manager'),
    path('fleet/transport/approval/manager/<int:pk>/approve/', views.approve_transport_manager, name='approve_transport_manager'),
    path('fleet/transport/approval/manager/<int:pk>/reject/', views.reject_transport_manager, name='reject_transport_manager'),

path('fleet/transport/approved-list/', views.transport_approved_list, name='transport_approved_list'),
path('fleet/transport/posted-list/', views.transport_posted_list, name='transport_posted_list'),
path('fleet/transport/completed-list/', views.transport_completed_list, name='transport_completed_list'),
path('fleet/transport/<int:pk>/post/', views.post_transport_requisition, name='post_transport_requisition'),
path('fleet/transport/<int:pk>/complete/', views.complete_transport_requisition, name='complete_transport_requisition'),
    # Work Ticket - Regular
    path('fleet/work-ticket/', views.work_ticket, name='work_ticket'),
    path('fleet/work-ticket-approval/', views.work_ticket_approval, name='work_ticket_approval'),
    path('fleet/work-ticket/<int:pk>/cancel/', views.cancel_work_ticket, name='cancel_work_ticket'),
    path('fleet/work-ticket/update/<int:pk>/<str:status>/', views.update_work_ticket_status, name='update_work_ticket_status'),

    # Work Ticket - Multi-Level Approval
    path('fleet/work-ticket/approval/fleet-manager/', views.work_ticket_approval_fleet_manager, name='work_ticket_approval_fleet_manager'),
    path('fleet/work-ticket/approval/fleet-manager/<int:pk>/approve/', views.approve_work_ticket_fleet_manager, name='approve_work_ticket_fleet_manager'),
    path('fleet/work-ticket/approval/fleet-manager/<int:pk>/reject/', views.reject_work_ticket_fleet_manager, name='reject_work_ticket_fleet_manager'),

    path('fleet/work-ticket/approval/operations-manager/', views.work_ticket_approval_operations_manager, name='work_ticket_approval_operations_manager'),
    path('fleet/work-ticket/approval/operations-manager/<int:pk>/approve/', views.approve_work_ticket_operations_manager, name='approve_work_ticket_operations_manager'),
    path('fleet/work-ticket/approval/operations-manager/<int:pk>/reject/', views.reject_work_ticket_operations_manager, name='reject_work_ticket_operations_manager'),

    path('fleet/work-ticket/approval/manager/', views.work_ticket_approval_manager, name='work_ticket_approval_manager'),
    path('fleet/work-ticket/approval/manager/<int:pk>/approve/', views.approve_work_ticket_manager, name='approve_work_ticket_manager'),
    path('fleet/work-ticket/approval/manager/<int:pk>/reject/', views.reject_work_ticket_manager, name='reject_work_ticket_manager'),

   path('fleet/work-ticket/approved-list/', views.work_ticket_approved_list, name='work_ticket_approved_list'),
   path('fleet/work-ticket/posted-list/', views.work_ticket_posted_list, name='work_ticket_posted_list'),
   path('fleet/work-ticket/completed-list/', views.work_ticket_completed_list, name='work_ticket_completed_list'),
   path('fleet/work-ticket/<int:pk>/post/', views.post_work_ticket, name='post_work_ticket'),
   path('fleet/work-ticket/<int:pk>/complete/', views.complete_work_ticket, name='complete_work_ticket'),
    # Fuel Requisition - Regular
    path('fleet/fuel-requisition/', views.fuel_requisition, name='fuel_requisition'),
    path('fleet/fuel-requisition-approval/', views.fuel_requisition_approval, name='fuel_requisition_approval'),
    path('fleet/fuel-requisition/<int:pk>/approve/', views.approve_fuel_requisition, name='approve_fuel_requisition'),
    path('fleet/fuel-requisition/<int:pk>/reject/', views.reject_fuel_requisition, name='reject_fuel_requisition'),

    # Fuel Requisition - Multi-Level Approval
    path('fleet/fuel-requisition/approval/fleet-manager/', views.fuel_requisition_approval_fleet_manager, name='fuel_requisition_approval_fleet_manager'),
    path('fleet/fuel-requisition/approval/fleet-manager/<int:pk>/approve/', views.approve_fuel_requisition_fleet_manager, name='approve_fuel_requisition_fleet_manager'),
    path('fleet/fuel-requisition/approval/fleet-manager/<int:pk>/reject/', views.reject_fuel_requisition_fleet_manager, name='reject_fuel_requisition_fleet_manager'),

    path('fleet/fuel-requisition/approval/operations-manager/', views.fuel_requisition_approval_operations_manager, name='fuel_requisition_approval_operations_manager'),
    path('fleet/fuel-requisition/approval/operations-manager/<int:pk>/approve/', views.approve_fuel_requisition_operations_manager, name='approve_fuel_requisition_operations_manager'),
    path('fleet/fuel-requisition/approval/operations-manager/<int:pk>/reject/', views.reject_fuel_requisition_operations_manager, name='reject_fuel_requisition_operations_manager'),

    path('fleet/fuel-requisition/approval/manager/', views.fuel_requisition_approval_manager, name='fuel_requisition_approval_manager'),
    path('fleet/fuel-requisition/approval/manager/<int:pk>/approve/', views.approve_fuel_requisition_manager, name='approve_fuel_requisition_manager'),
    path('fleet/fuel-requisition/approval/manager/<int:pk>/reject/', views.reject_fuel_requisition_manager, name='reject_fuel_requisition_manager'),
    
    path('fleet/fuel-requisition/approved-list/', views.fuel_requisition_approved_list, name='fuel_requisition_approved_list'),
    path('fleet/fuel-requisition/posted-list/', views.fuel_requisition_posted_list, name='fuel_requisition_posted_list'),
    path('fleet/fuel-requisition/completed-list/', views.fuel_requisition_completed_list, name='fuel_requisition_completed_list'),
    path('fleet/fuel-requisition/<int:pk>/post/', views.post_fuel_requisition, name='post_fuel_requisition'),
    path('fleet/fuel-requisition/<int:pk>/complete/', views.complete_fuel_requisition, name='complete_fuel_requisition'),
   

]