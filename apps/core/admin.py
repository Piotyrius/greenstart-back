from django.contrib import admin
from apps.core.models import (
    Buyer, Plantation, TreeLot, TreePurchase,
    NFTCertificate, ISOComplianceRecord, GrowthData
)


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'name', 'email', 'buyer_type', 'country', 'has_logo', 'created_at']
    list_filter = ['buyer_type', 'created_at']
    search_fields = ['name', 'email', 'company_name', 'country']
    readonly_fields = ['created_at', 'logo_preview']
    filter_horizontal = []
    
    def has_logo(self, obj):
        return bool(obj.company_logo)
    has_logo.boolean = True
    has_logo.short_description = "Has Logo"
    
    def logo_preview(self, obj):
        """Display logo preview in admin."""
        if obj.company_logo:
            return f'<img src="{obj.company_logo}" style="max-width: 200px; max-height: 200px;" />'
        return "No logo"
    logo_preview.allow_tags = True
    logo_preview.short_description = "Logo Preview"


@admin.register(Plantation)
class PlantationAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'sector', 'planting_date', 'total_hectares', 'is_active', 'created_at']
    list_filter = ['species', 'sector', 'is_active', 'planting_date', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'yearly_co2_display', 'total_trees_display', 'available_trees_display']
    
    def yearly_co2_display(self, obj):
        """Display yearly CO₂ absorption in admin."""
        co2 = obj.calculate_yearly_co2()
        return f"{co2:.2f} kg CO₂/year"
    yearly_co2_display.short_description = "Yearly CO₂ Absorption"
    
    def total_trees_display(self, obj):
        """Display total trees."""
        return f"{obj.get_total_trees()} trees"
    total_trees_display.short_description = "Total Trees"
    
    def available_trees_display(self, obj):
        """Display available trees."""
        return f"{obj.get_available_trees()} trees"
    available_trees_display.short_description = "Available Trees"


@admin.register(TreeLot)
class TreeLotAdmin(admin.ModelAdmin):
    list_display = ['lot_number', 'plantation', 'sector', 'number_of_trees', 'area_hectares', 'b2b_price', 'b2c_price', 'is_available', 'created_at']
    list_filter = ['plantation', 'sector', 'is_available', 'created_at']
    search_fields = ['lot_number']
    readonly_fields = ['created_at']
    raw_id_fields = ['plantation']


@admin.register(TreePurchase)
class TreePurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'buyer', 'tree_lot', 'quantity', 'total_price', 'status', 'purchase_date']
    list_filter = ['status', 'purchase_date', 'buyer__buyer_type']
    search_fields = ['buyer__company_name', 'buyer__email', 'payment_reference']
    readonly_fields = ['purchase_date', 'total_price']
    raw_id_fields = ['buyer', 'tree_lot']


@admin.register(NFTCertificate)
class NFTCertificateAdmin(admin.ModelAdmin):
    list_display = ['id', 'purchase', 'nft_token_id', 'co2_absorbed_kg', 'issued_at', 'has_pdf', 'is_minted']
    list_filter = ['issued_at']
    search_fields = ['nft_token_id', 'purchase__buyer__company_name', 'qr_code']
    readonly_fields = ['issued_at', 'co2_display']
    raw_id_fields = ['purchase']
    
    def has_pdf(self, obj):
        return bool(obj.pdf_url)
    has_pdf.boolean = True
    has_pdf.short_description = "Has PDF"
    
    def is_minted(self, obj):
        return bool(obj.nft_token_id)
    is_minted.boolean = True
    is_minted.short_description = "NFT Minted"
    
    def co2_display(self, obj):
        """Display CO₂ absorption in admin."""
        return f"{obj.co2_absorbed_kg:.2f} kg CO₂"
    co2_display.short_description = "CO₂ Absorption"


@admin.register(ISOComplianceRecord)
class ISOComplianceRecordAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'iso_standard', 'compliance_status', 'verification_date', 'expiry_date']
    list_filter = ['iso_standard', 'compliance_status', 'verification_date']
    search_fields = ['buyer__company_name', 'iso_standard']
    readonly_fields = ['created_at']
    raw_id_fields = ['buyer', 'nft_certificate']


@admin.register(GrowthData)
class GrowthDataAdmin(admin.ModelAdmin):
    list_display = ['plantation', 'ndvi_value', 'co2_absorbed_kg', 'timestamp']
    list_filter = ['plantation', 'timestamp']
    search_fields = ['plantation__name', 'notes']
    readonly_fields = ['timestamp']
    raw_id_fields = ['plantation']
