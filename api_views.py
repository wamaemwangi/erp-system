from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import (
    PettyCash, Imprest, LeaveApplication, StoreRequisition,
    PurchaseRequisition, SalaryAdvance, TransportRequisition,
    WorkTicket, FuelRequisition, Overtime
)
from .serializers import (
    PettyCashSerializer, ImprestSerializer, LeaveApplicationSerializer,
    StoreRequisitionSerializer, PurchaseRequisitionSerializer,
    SalaryAdvanceSerializer, TransportRequisitionSerializer,
    WorkTicketSerializer, FuelRequisitionSerializer, OvertimeSerializer
)


class PettyCashViewSet(viewsets.ModelViewSet):
    serializer_class = PettyCashSerializer
    permission_classes = [IsAuthenticated]
    queryset = PettyCash.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = PettyCash.objects.filter(status='PENDING')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


class ImprestViewSet(viewsets.ModelViewSet):
    serializer_class = ImprestSerializer
    permission_classes = [IsAuthenticated]
    queryset = Imprest.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = Imprest.objects.filter(status='PENDING')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveApplicationSerializer
    permission_classes = [IsAuthenticated]
    queryset = LeaveApplication.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = LeaveApplication.objects.filter(status='PENDING')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)


class StoreRequisitionViewSet(viewsets.ModelViewSet):
    serializer_class = StoreRequisitionSerializer
    permission_classes = [IsAuthenticated]
    queryset = StoreRequisition.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(requested_by=self.request.user.username)


class PurchaseRequisitionViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseRequisitionSerializer
    permission_classes = [IsAuthenticated]
    queryset = PurchaseRequisition.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(requested_by=self.request.user.username)


class SalaryAdvanceViewSet(viewsets.ModelViewSet):
    serializer_class = SalaryAdvanceSerializer
    permission_classes = [IsAuthenticated]
    queryset = SalaryAdvance.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)


class TransportRequisitionViewSet(viewsets.ModelViewSet):
    serializer_class = TransportRequisitionSerializer
    permission_classes = [IsAuthenticated]
    queryset = TransportRequisition.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)


class WorkTicketViewSet(viewsets.ModelViewSet):
    serializer_class = WorkTicketSerializer
    permission_classes = [IsAuthenticated]
    queryset = WorkTicket.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)


class FuelRequisitionViewSet(viewsets.ModelViewSet):
    serializer_class = FuelRequisitionSerializer
    permission_classes = [IsAuthenticated]
    queryset = FuelRequisition.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)


class OvertimeViewSet(viewsets.ModelViewSet):
    serializer_class = OvertimeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Overtime.objects.all()  # Fixed: added queryset

    def get_queryset(self):
        return self.queryset.filter(employee_name=self.request.user.get_full_name() or self.request.user.username)


class DashboardStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def stats(self, request):
        user_name = request.user.get_full_name() or request.user.username
        data = {
            'my_pending_leaves': LeaveApplication.objects.filter(employee_name=user_name, status='PENDING').count(),
            'my_pending_petty_cash': PettyCash.objects.filter(employee_name=user_name, status='PENDING').count(),
            'my_pending_imprest': Imprest.objects.filter(employee_name=user_name, status='PENDING').count(),
            'my_pending_store': StoreRequisition.objects.filter(requested_by=request.user.username, status='PENDING').count(),
            'my_pending_purchase': PurchaseRequisition.objects.filter(requested_by=request.user.username, status='PENDING').count(),
            'my_pending_overtime': Overtime.objects.filter(employee_name=user_name, status='PENDING').count(),
            'pending_approvals': {
                'leaves': LeaveApplication.objects.filter(status='PENDING').count(),
                'petty_cash': PettyCash.objects.filter(status='PENDING').count(),
                'imprest': Imprest.objects.filter(status='PENDING').count(),
                'store': StoreRequisition.objects.filter(status='PENDING').count(),
                'purchase': PurchaseRequisition.objects.filter(status='PENDING').count(),
                'salary_advance': SalaryAdvance.objects.filter(status='PENDING').count(),
            }
        }
        return Response(data)