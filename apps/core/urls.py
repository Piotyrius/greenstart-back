from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views import (
    BuyerViewSet, PlantationViewSet, TreeLotViewSet,
    TreePurchaseViewSet, NFTCertificateViewSet,
    ISOComplianceRecordViewSet, GrowthDataViewSet,
    update_ndvi_data_endpoint,
    update_co2_absorption_endpoint
)

router = DefaultRouter()
router.register(r'buyers', BuyerViewSet)
router.register(r'plantations', PlantationViewSet)
router.register(r'tree-lots', TreeLotViewSet)
router.register(r'purchases', TreePurchaseViewSet)
router.register(r'nft-certificates', NFTCertificateViewSet)
router.register(r'iso-compliance', ISOComplianceRecordViewSet)
router.register(r'growth-data', GrowthDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Cloud Scheduler endpoints
    path('update-ndvi/', update_ndvi_data_endpoint, name='update-ndvi'),
    path('update-co2/', update_co2_absorption_endpoint, name='update-co2'),
]
