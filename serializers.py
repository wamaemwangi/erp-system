from rest_framework import serializers
from .models import (
    PettyCash, PettyCashItem,
    Imprest, ImprestItem,
    LeaveApplication,
    StoreRequisition, StoreRequisitionItem,
    PurchaseRequisition, PurchaseRequisitionItem,
    SalaryAdvance,
    TransportRequisition,
    WorkTicket,
    FuelRequisition,
    Overtime,
)


class PettyCashItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PettyCashItem
        fields = ['id', 'description', 'amount']


class PettyCashSerializer(serializers.ModelSerializer):
    items = PettyCashItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = PettyCash
        fields = ['id', 'petty_cash_number', 'employee_name', 'amount', 'description',
                  'from_date', 'to_date', 'department', 'status', 'document', 
                  'created_at', 'items', 'approval_level', 'is_posted', 'is_surrendered']


class ImprestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImprestItem
        fields = ['id', 'description', 'amount']


class ImprestSerializer(serializers.ModelSerializer):
    items = ImprestItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Imprest
        fields = ['id', 'imprest_number', 'employee_name', 'amount', 'description',
                  'from_date', 'to_date', 'department', 'status', 'document',
                  'created_at', 'items', 'approval_level', 'is_posted', 'is_surrendered']


class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['id', 'employee_name', 'leave_type', 'days', 'start_date', 'end_date',
                  'reason', 'status', 'created_at', 'approval_level']


class StoreRequisitionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRequisitionItem
        fields = ['id', 'description', 'quantity']


class StoreRequisitionSerializer(serializers.ModelSerializer):
    items = StoreRequisitionItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = StoreRequisition
        fields = ['id', 'description', 'department', 'requested_by', 'status',
                  'created_at', 'items', 'approval_level']


class PurchaseRequisitionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseRequisitionItem
        fields = ['id', 'description', 'quantity']


class PurchaseRequisitionSerializer(serializers.ModelSerializer):
    items = PurchaseRequisitionItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = PurchaseRequisition
        fields = ['id', 'description', 'department', 'requested_by', 'status',
                  'created_at', 'items', 'approval_level']


class SalaryAdvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryAdvance
        fields = ['id', 'employee_name', 'amount', 'purpose', 'date_required',
                  'status', 'created_at', 'approval_level']


class TransportRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportRequisition
        fields = ['id', 'employee_name', 'department', 'destination', 'date_required',
                  'purpose', 'status', 'created_at']


class WorkTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTicket
        fields = ['id', 'employee_name', 'department', 'destination', 'date_required',
                  'purpose', 'status', 'created_at', 'document']


class FuelRequisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelRequisition
        fields = ['id', 'employee_name', 'vehicle', 'liters', 'destination',
                  'purpose', 'status', 'created_at']


class OvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = ['id', 'employee_name', 'hours', 'reason', 'department', 
                  'status', 'created_at']