from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    PettyCashViewSet, ImprestViewSet, LeaveViewSet,
    StoreRequisitionViewSet, PurchaseRequisitionViewSet,
    SalaryAdvanceViewSet, TransportRequisitionViewSet,
    WorkTicketViewSet, FuelRequisitionViewSet, OvertimeViewSet,
    DashboardStatsViewSet
)

router = DefaultRouter()
router.register(r'petty-cash', PettyCashViewSet, basename='petty-cash')
router.register(r'imprest', ImprestViewSet, basename='imprest')
router.register(r'leaves', LeaveViewSet, basename='leave')
router.register(r'store-requisitions', StoreRequisitionViewSet, basename='store-requisition')
router.register(r'purchase-requisitions', PurchaseRequisitionViewSet, basename='purchase-requisition')
router.register(r'salary-advance', SalaryAdvanceViewSet, basename='salary-advance')
router.register(r'transport', TransportRequisitionViewSet, basename='transport')
router.register(r'work-tickets', WorkTicketViewSet, basename='work-ticket')
router.register(r'fuel', FuelRequisitionViewSet, basename='fuel')
router.register(r'overtime', OvertimeViewSet, basename='overtime')
router.register(r'dashboard', DashboardStatsViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]