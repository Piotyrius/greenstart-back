"""
GREWECO API Serializers - Marketplace for selling NFT-ized trees
"""
from rest_framework import serializers
from apps.core.models import (
    Buyer, Plantation, TreeLot, TreePurchase,
    NFTCertificate, ISOComplianceRecord, GrowthData
)


class BuyerSerializer(serializers.ModelSerializer):
    purchases_count = serializers.IntegerField(source='purchases.count', read_only=True)
    total_trees_purchased = serializers.SerializerMethodField()

    class Meta:
        model = Buyer
        fields = [
            'id', 'name', 'email', 'buyer_type', 'created_at',
            # B2B fields
            'company_name', 'company_logo', 'country', 'iso_standards',
            'tax_id', 'website',
            # B2C fields
            'phone', 'address',
            # Computed
            'purchases_count', 'total_trees_purchased'
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_trees_purchased(self, obj):
        """Calculate total trees purchased by this buyer."""
        return sum(
            purchase.quantity for purchase in obj.purchases.filter(status='completed')
        )
    
    def validate(self, data):
        """Validate B2B requires company_name."""
        if data.get('buyer_type') == 'b2b' and not data.get('company_name'):
            raise serializers.ValidationError({
                'company_name': 'Company name is required for B2B buyers.'
            })
        return data


class PlantationSerializer(serializers.ModelSerializer):
    yearly_co2_absorbed = serializers.SerializerMethodField()
    total_trees = serializers.SerializerMethodField()
    available_trees = serializers.SerializerMethodField()
    tree_lots_count = serializers.IntegerField(source='tree_lots.count', read_only=True)
    b2b_lots_count = serializers.SerializerMethodField()
    b2c_lots_count = serializers.SerializerMethodField()

    class Meta:
        model = Plantation
        fields = [
            'id', 'name', 'polygon_coordinates', 'planting_date',
            'expected_harvest_date', 'species', 'total_hectares',
            'sector', 'trees_per_hectare',
            # B2B pricing
            'b2b_price_per_tree', 'b2b_price_per_hectare',
            # B2C pricing
            'b2c_price_per_tree', 'b2c_price_per_hectare',
            # Legacy pricing (deprecated)
            'price_per_tree', 'price_per_hectare',
            'is_active', 'created_at', 'yearly_co2_absorbed',
            'total_trees', 'available_trees', 'tree_lots_count',
            'b2b_lots_count', 'b2c_lots_count'
        ]
        read_only_fields = ['id', 'created_at']

    def get_yearly_co2_absorbed(self, obj):
        """Calculate and return yearly CO₂ absorption."""
        co2 = obj.calculate_yearly_co2()
        return float(co2)

    def get_total_trees(self, obj):
        """Get total number of trees."""
        return obj.get_total_trees()

    def get_available_trees(self, obj):
        """Get available trees for sale."""
        return obj.get_available_trees()
    
    def get_b2b_lots_count(self, obj):
        """Get count of B2B lots."""
        return obj.tree_lots.filter(sector='b2b').count()
    
    def get_b2c_lots_count(self, obj):
        """Get count of B2C lots."""
        return obj.tree_lots.filter(sector='b2c').count()

    def validate_polygon_coordinates(self, value):
        """Validate polygon coordinates format."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Polygon coordinates must be a JSON object.")
        if 'type' not in value or value['type'] != 'Polygon':
            raise serializers.ValidationError("Polygon coordinates must be a GeoJSON Polygon.")
        if 'coordinates' not in value:
            raise serializers.ValidationError("Polygon coordinates must include 'coordinates' field.")
        return value


class TreeLotSerializer(serializers.ModelSerializer):
    plantation_name = serializers.CharField(source='plantation.name', read_only=True)
    plantation_sector = serializers.CharField(source='plantation.sector', read_only=True)
    available_trees = serializers.SerializerMethodField()

    class Meta:
        model = TreeLot
        fields = [
            'id', 'plantation', 'plantation_name', 'plantation_sector',
            'lot_number', 'sector',
            'area_polygon', 'area_hectares', 'number_of_trees',
            'b2b_price', 'b2c_price', 'price',  # price is legacy
            'is_available', 'created_at', 'available_trees'
        ]
        read_only_fields = ['id', 'created_at']

    def get_available_trees(self, obj):
        """Calculate remaining trees in this lot."""
        from django.db.models import Sum
        sold = TreePurchase.objects.filter(
            tree_lot=obj,
            status='completed'
        ).aggregate(total=Sum('quantity'))['total'] or 0
        return obj.number_of_trees - sold

    def validate_area_polygon(self, value):
        """Validate area polygon coordinates format."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Area polygon must be a JSON object.")
        if 'type' not in value or value['type'] != 'Polygon':
            raise serializers.ValidationError("Area polygon must be a GeoJSON Polygon.")
        if 'coordinates' not in value:
            raise serializers.ValidationError("Area polygon must include 'coordinates' field.")
        return value


class TreePurchaseSerializer(serializers.ModelSerializer):
    buyer_info = serializers.SerializerMethodField()
    tree_lot_info = serializers.SerializerMethodField()
    has_nft_certificate = serializers.SerializerMethodField()

    class Meta:
        model = TreePurchase
        fields = [
            'id', 'buyer', 'tree_lot', 'buyer_info', 'tree_lot_info',
            'quantity', 'price_per_tree', 'total_price', 'status',
            'purchase_date', 'payment_reference', 'notes',
            'has_nft_certificate'
        ]
        read_only_fields = ['id', 'purchase_date', 'total_price']

    def get_buyer_info(self, obj):
        """Return buyer details."""
        buyer = obj.buyer
        info = {
            'id': buyer.id,
            'buyer_type': buyer.buyer_type,
            'name': buyer.name,
        }
        if buyer.buyer_type == 'b2b':
            info.update({
                'company_name': buyer.company_name,
                'company_logo': buyer.company_logo,
                'country': buyer.country,
                'website': buyer.website,
            })
        else:
            info.update({
                'phone': buyer.phone,
                'address': buyer.address,
            })
        return info

    def get_tree_lot_info(self, obj):
        """Return tree lot details."""
        return {
            'id': obj.tree_lot.id,
            'lot_number': obj.tree_lot.lot_number,
            'plantation_name': obj.tree_lot.plantation.name,
            'number_of_trees': obj.tree_lot.number_of_trees,
        }

    def get_has_nft_certificate(self, obj):
        """Check if NFT certificate exists."""
        return hasattr(obj, 'nft_certificate')


class NFTCertificateSerializer(serializers.ModelSerializer):
    purchase_info = serializers.SerializerMethodField()
    buyer_info = serializers.SerializerMethodField()
    co2_absorbed_kg = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = NFTCertificate
        fields = [
            'id', 'purchase', 'purchase_info', 'buyer_info',
            'nft_token_id', 'blockchain_address', 'transaction_hash',
            'pdf_url', 'qr_code', 'issued_at', 'co2_absorbed_kg'
        ]
        read_only_fields = ['id', 'issued_at', 'co2_absorbed_kg']

    def get_purchase_info(self, obj):
        """Return purchase details."""
        return {
            'id': obj.purchase.id,
            'quantity': obj.purchase.quantity,
            'total_price': float(obj.purchase.total_price),
            'purchase_date': obj.purchase.purchase_date,
        }

    def get_buyer_info(self, obj):
        """Return buyer details."""
        buyer = obj.purchase.buyer
        return {
            'id': buyer.id,
            'company_name': buyer.company_name,
            'buyer_type': buyer.buyer_type,
            'country': buyer.country,
        }


class ISOComplianceRecordSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.company_name', read_only=True)
    certificate_token = serializers.CharField(source='nft_certificate.nft_token_id', read_only=True)

    class Meta:
        model = ISOComplianceRecord
        fields = [
            'id', 'buyer', 'buyer_name', 'nft_certificate', 'certificate_token',
            'iso_standard', 'compliance_status', 'verification_date',
            'expiry_date', 'verification_document_url', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class GrowthDataSerializer(serializers.ModelSerializer):
    plantation_name = serializers.CharField(source='plantation.name', read_only=True)
    co2_absorbed_kg = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = GrowthData
        fields = [
            'id', 'plantation', 'plantation_name', 'ndvi_value',
            'timestamp', 'co2_absorbed_kg', 'notes'
        ]
        read_only_fields = ['id', 'timestamp', 'co2_absorbed_kg']
