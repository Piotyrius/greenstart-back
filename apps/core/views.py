"""
GREWECO API Views - Marketplace for selling NFT-ized trees
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from django.core.management import call_command
from django.conf import settings
from django.db import models
from apps.core.models import (
    Buyer, Plantation, TreeLot, TreePurchase,
    NFTCertificate, ISOComplianceRecord, GrowthData
)
from apps.core.serializers import (
    BuyerSerializer, PlantationSerializer, TreeLotSerializer,
    TreePurchaseSerializer, NFTCertificateSerializer,
    ISOComplianceRecordSerializer, GrowthDataSerializer
)
from apps.core.utils.pdf_generator import generate_certificate_pdf


class BuyerViewSet(viewsets.ModelViewSet):
    """ViewSet for Buyer model (developers and companies)."""
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """Allow list/retrieve for authenticated users, require admin for create/update/delete."""
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]


class PlantationViewSet(viewsets.ModelViewSet):
    """ViewSet for Plantation model - trees available for sale."""
    queryset = Plantation.objects.all()
    serializer_class = PlantationSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def co2_calculation(self, request, pk=None):
        """Get detailed CO₂ calculation breakdown for a plantation."""
        plantation = self.get_object()
        co2_per_year = plantation.calculate_yearly_co2()
        
        from datetime import date
        age_years = (date.today() - plantation.planting_date).days / 365.25
        if age_years < 0:
            age_years = 0
        
        return Response({
            'plantation_id': plantation.id,
            'plantation_name': plantation.name,
            'age_years': round(age_years, 2),
            'total_hectares': float(plantation.total_hectares),
            'total_trees': plantation.get_total_trees(),
            'available_trees': plantation.get_available_trees(),
            'yearly_co2_absorbed_kg': float(co2_per_year),
            'price_per_tree': float(plantation.price_per_tree),
            'price_per_hectare': float(plantation.price_per_hectare),
        })

    @action(detail=True, methods=['get'])
    def available_lots(self, request, pk=None):
        """Get available tree lots for this plantation."""
        plantation = self.get_object()
        lots = TreeLot.objects.filter(plantation=plantation, is_available=True)
        serializer = TreeLotSerializer(lots, many=True)
        return Response(serializer.data)


class TreeLotViewSet(viewsets.ModelViewSet):
    """ViewSet for TreeLot model - lots available for purchase."""
    queryset = TreeLot.objects.all()
    serializer_class = TreeLotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter by plantation and availability."""
        queryset = TreeLot.objects.all()
        plantation_id = self.request.query_params.get('plantation', None)
        if plantation_id:
            queryset = queryset.filter(plantation_id=plantation_id)
        available_only = self.request.query_params.get('available', 'false').lower() == 'true'
        if available_only:
            queryset = queryset.filter(is_available=True)
        return queryset


class TreePurchaseViewSet(viewsets.ModelViewSet):
    """ViewSet for TreePurchase model - tree purchase transactions."""
    queryset = TreePurchase.objects.all()
    serializer_class = TreePurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter purchases by buyer."""
        queryset = TreePurchase.objects.all()
        buyer_id = self.request.query_params.get('buyer', None)
        if buyer_id:
            queryset = queryset.filter(buyer_id=buyer_id)
        return queryset

    @action(detail=True, methods=['post'])
    def complete_purchase(self, request, pk=None):
        """Complete a purchase and generate NFT certificate."""
        purchase = self.get_object()
        
        if purchase.status != 'pending':
            return Response(
                {'error': 'Purchase is not pending'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark purchase as completed
        purchase.status = 'completed'
        purchase.save()
        
        # Create NFT certificate
        nft_cert, created = NFTCertificate.objects.get_or_create(
            purchase=purchase,
            defaults={}
        )
        
        # Calculate CO₂
        nft_cert.calculate_co2()
        
        # Mark tree lot as unavailable if all trees sold
        tree_lot = purchase.tree_lot
        remaining = tree_lot.number_of_trees - TreePurchase.objects.filter(
            tree_lot=tree_lot,
            status='completed'
        ).aggregate(total=models.Sum('quantity'))['total'] or 0
        
        if remaining <= 0:
            tree_lot.is_available = False
            tree_lot.save()
        
        serializer = NFTCertificateSerializer(nft_cert)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class NFTCertificateViewSet(viewsets.ModelViewSet):
    """ViewSet for NFTCertificate model - NFT ownership certificates."""
    queryset = NFTCertificate.objects.all()
    serializer_class = NFTCertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter certificates by buyer."""
        queryset = NFTCertificate.objects.all()
        buyer_id = self.request.query_params.get('buyer', None)
        if buyer_id:
            queryset = queryset.filter(purchase__buyer_id=buyer_id)
        return queryset

    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        """Generate PDF certificate and upload to Google Cloud Storage."""
        certificate = self.get_object()
        
        # Calculate CO₂ if not already calculated
        if certificate.co2_absorbed_kg == 0:
            certificate.calculate_co2()
        
        # Generate PDF
        try:
            pdf_url = generate_certificate_pdf(certificate)
            certificate.pdf_url = pdf_url
            certificate.save(update_fields=['pdf_url'])
            
            return Response({
                'message': 'PDF generated successfully',
                'pdf_url': pdf_url
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'Failed to generate PDF: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def mint_nft(self, request, pk=None):
        """Mint NFT on blockchain (placeholder for future Web3 integration)."""
        certificate = self.get_object()
        
        # TODO: Integrate with Polygon blockchain
        # For now, generate a placeholder token ID
        if not certificate.nft_token_id:
            certificate.nft_token_id = f"GREWECO-{certificate.id}-{certificate.purchase.id}"
            certificate.blockchain_address = "0x0000000000000000000000000000000000000000"  # Placeholder
            certificate.save()
        
        return Response({
            'message': 'NFT minted (placeholder)',
            'nft_token_id': certificate.nft_token_id,
            'note': 'Real blockchain integration coming soon'
        })


class ISOComplianceRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for ISOComplianceRecord model."""
    queryset = ISOComplianceRecord.objects.all()
    serializer_class = ISOComplianceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter by buyer or certificate."""
        queryset = ISOComplianceRecord.objects.all()
        buyer_id = self.request.query_params.get('buyer', None)
        if buyer_id:
            queryset = queryset.filter(buyer_id=buyer_id)
        certificate_id = self.request.query_params.get('certificate', None)
        if certificate_id:
            queryset = queryset.filter(nft_certificate_id=certificate_id)
        return queryset


class GrowthDataViewSet(viewsets.ModelViewSet):
    """ViewSet for GrowthData model."""
    queryset = GrowthData.objects.all()
    serializer_class = GrowthDataSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter growth data by plantation."""
        queryset = GrowthData.objects.all()
        plantation_id = self.request.query_params.get('plantation', None)
        if plantation_id:
            queryset = queryset.filter(plantation_id=plantation_id)
        return queryset.order_by('-timestamp')


# Cloud Scheduler HTTP endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
def update_ndvi_data_endpoint(request):
    """HTTP endpoint for Cloud Scheduler to trigger NDVI data updates."""
    secret = request.headers.get('X-CloudScheduler-Secret', '')
    expected_secret = getattr(settings, 'CLOUD_SCHEDULER_SECRET', '')
    
    if expected_secret and secret != expected_secret:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        year = request.data.get('year', None)
        if year:
            call_command('update_ndvi_data', year=year)
        else:
            call_command('update_ndvi_data')
        return Response({'message': 'NDVI data updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def update_co2_absorption_endpoint(request):
    """HTTP endpoint for Cloud Scheduler to trigger CO₂ absorption recalculation."""
    secret = request.headers.get('X-CloudScheduler-Secret', '')
    expected_secret = getattr(settings, 'CLOUD_SCHEDULER_SECRET', '')
    
    if expected_secret and secret != expected_secret:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        call_command('update_co2_absorption')
        return Response({'message': 'CO₂ absorption updated successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
