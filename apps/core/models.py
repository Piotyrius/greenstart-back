"""
GREWECO Core Models
Marketplace for selling NFT-ized trees to developers and companies for ISO compliance
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import date


class Buyer(models.Model):
    """
    Buyer model - represents B2B companies or B2C individuals purchasing trees.
    B2B: Companies, developers, foreign companies (for ISO compliance)
    B2C: Individual consumers
    """
    BUYER_TYPE_CHOICES = [
        ('b2b', 'B2B - Business/Company'),
        ('b2c', 'B2C - Individual Consumer'),
    ]
    
    # Common fields
    name = models.CharField(max_length=255, help_text="Contact person name (B2B) or full name (B2C)")
    email = models.EmailField(unique=True)
    buyer_type = models.CharField(max_length=10, choices=BUYER_TYPE_CHOICES, default='b2b')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # B2B specific fields
    company_name = models.CharField(max_length=255, blank=True, help_text="Required for B2B")
    company_logo = models.URLField(
        blank=True,
        null=True,
        help_text="URL to company logo image (stored in Google Cloud Storage)"
    )
    country = models.CharField(max_length=100, blank=True, help_text="For foreign companies")
    iso_standards = models.JSONField(
        default=list,
        blank=True,
        help_text="ISO standards they need compliance for (e.g., ['ISO 14001', 'ISO 14064'])"
    )
    tax_id = models.CharField(max_length=100, blank=True, help_text="Company tax ID/VAT number")
    website = models.URLField(blank=True, help_text="Company website")
    
    # B2C specific fields
    phone = models.CharField(max_length=50, blank=True, help_text="Phone number (B2C)")
    address = models.TextField(blank=True, help_text="Home address (B2C)")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Buyer"
        verbose_name_plural = "Buyers"

    def __str__(self):
        if self.buyer_type == 'b2b':
            return f"{self.company_name or 'N/A'} ({self.get_buyer_type_display()})"
        else:
            return f"{self.name} ({self.get_buyer_type_display()})"
    
    def clean(self):
        """Validate B2B requires company_name."""
        from django.core.exceptions import ValidationError
        if self.buyer_type == 'b2b' and not self.company_name:
            raise ValidationError({'company_name': 'Company name is required for B2B buyers.'})


class Plantation(models.Model):
    """
    Plantation model - represents paulownia tree plantations available for sale.
    Trees are sold as NFTs to buyers. Can be divided into B2B and B2C sectors.
    """
    SECTOR_CHOICES = [
        ('b2b', 'B2B - Business to Business'),
        ('b2c', 'B2C - Business to Consumer'),
        ('mixed', 'Mixed - Both B2B and B2C'),
    ]
    
    name = models.CharField(max_length=255)
    polygon_coordinates = models.JSONField(
        help_text="GeoJSON polygon coordinates for the plantation boundary"
    )
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    species = models.CharField(max_length=100, default="Paulownia")
    total_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))]
    )
    sector = models.CharField(
        max_length=10,
        choices=SECTOR_CHOICES,
        default='mixed',
        help_text="Sector type: B2B, B2C, or Mixed"
    )
    trees_per_hectare = models.PositiveIntegerField(
        default=1000,
        help_text="Number of trees per hectare (for sale calculation)"
    )
    # B2B pricing
    b2b_price_per_tree = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="B2B price per tree in USD"
    )
    b2b_price_per_hectare = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="B2B price per hectare in USD"
    )
    # B2C pricing
    b2c_price_per_tree = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="B2C price per tree in USD"
    )
    b2c_price_per_hectare = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="B2C price per hectare in USD"
    )
    # Legacy fields for backward compatibility
    price_per_tree = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Default price per tree (deprecated - use b2b/b2c prices)"
    )
    price_per_hectare = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Default price per hectare (deprecated - use b2b/b2c prices)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this plantation is available for sale"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.total_hectares} ha)"

    def calculate_yearly_co2(self, year=None):
        """
        Calculate CO₂ absorbed per year for this plantation.
        
        Formula: age_years × species_factor × hectares × annual_rate
        
        Where:
        - age_years = number of years since planting
        - species_factor = 22 kg CO₂ per tree per year (PLACEHOLDER - adjust later)
        - hectares = total_hectares of plantation
        - annual_rate = trees_per_hectare × scale_factor (PLACEHOLDER - adjust later)
        
        Args:
            year: Optional year to calculate for. If None, uses current year.
            
        Returns:
            Decimal: CO₂ absorbed in kg per year
        """
        from apps.core.utils.co2_calculator import (
            PAULOWNIA_SPECIES_FACTOR,
            SCALE_FACTOR
        )
        
        if year is None:
            today = date.today()
        else:
            today = date(year, 12, 31)
        
        # Calculate age in years
        age_years = (today - self.planting_date).days / 365.25
        
        # Ensure age is not negative
        if age_years < 0:
            age_years = 0
        
        # Calculate CO₂ absorbed per year
        # PLACEHOLDER formula - replace with real biomass-based calculations later
        co2_per_year = (
            Decimal(str(age_years)) *
            Decimal(str(PAULOWNIA_SPECIES_FACTOR)) *
            self.total_hectares *
            Decimal(str(self.trees_per_hectare)) *
            Decimal(str(SCALE_FACTOR))
        )
        
        return co2_per_year

    def get_total_trees(self):
        """Get total number of trees in plantation."""
        return int(self.total_hectares * self.trees_per_hectare)

    def get_available_trees(self):
        """Get number of trees still available for sale."""
        sold = TreePurchase.objects.filter(
            tree_lot__plantation=self,
            status='completed'
        ).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
        return self.get_total_trees() - sold


class TreeLot(models.Model):
    """
    TreeLot model - represents a lot of trees/hectares available for purchase.
    Each lot can be sold to a buyer. Can be assigned to B2B or B2C sector.
    """
    SECTOR_CHOICES = [
        ('b2b', 'B2B - Business to Business'),
        ('b2c', 'B2C - Business to Consumer'),
    ]
    
    plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name='tree_lots')
    lot_number = models.CharField(max_length=50)
    sector = models.CharField(
        max_length=10,
        choices=SECTOR_CHOICES,
        default='b2b',
        help_text="Sector this lot is assigned to (B2B or B2C)"
    )
    area_polygon = models.JSONField(
        help_text="GeoJSON polygon coordinates for this lot"
    )
    area_hectares = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0.0001'))]
    )
    number_of_trees = models.PositiveIntegerField(
        help_text="Number of trees in this lot"
    )
    # Pricing based on sector
    b2b_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="B2B price for this lot"
    )
    b2c_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="B2C price for this lot"
    )
    # Legacy field
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Default price (deprecated - use b2b/b2c prices)"
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_price_for_buyer_type(self, buyer_type):
        """Get price based on buyer type."""
        if buyer_type == 'b2b':
            return self.b2b_price if self.b2b_price > 0 else self.price
        else:
            return self.b2c_price if self.b2c_price > 0 else self.price

    class Meta:
        ordering = ['lot_number']
        unique_together = ['plantation', 'lot_number']

    def __str__(self):
        return f"{self.plantation.name} - Lot {self.lot_number} ({self.number_of_trees} trees)"


class TreePurchase(models.Model):
    """
    TreePurchase model - represents a purchase of trees by a buyer.
    This is the transaction record when trees are sold.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='purchases')
    tree_lot = models.ForeignKey(TreeLot, on_delete=models.CASCADE, related_name='purchases')
    quantity = models.PositiveIntegerField(
        help_text="Number of trees purchased"
    )
    price_per_tree = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    purchase_date = models.DateTimeField(auto_now_add=True)
    payment_reference = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-purchase_date']

    def __str__(self):
        return f"Purchase #{self.id} - {self.buyer.company_name} - {self.quantity} trees"

    def save(self, *args, **kwargs):
        """Auto-calculate total price."""
        if not self.total_price:
            self.total_price = self.price_per_tree * self.quantity
        super().save(*args, **kwargs)


class NFTCertificate(models.Model):
    """
    NFTCertificate model - represents NFT ownership certificate for purchased trees.
    Each purchase generates an NFT certificate with blockchain token ID.
    """
    purchase = models.OneToOneField(
        TreePurchase,
        on_delete=models.CASCADE,
        related_name='nft_certificate'
    )
    nft_token_id = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Blockchain NFT token ID (will be minted on Polygon)"
    )
    blockchain_address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Blockchain contract address"
    )
    transaction_hash = models.CharField(
        max_length=255,
        blank=True,
        help_text="Blockchain transaction hash"
    )
    pdf_url = models.URLField(blank=True, null=True)
    qr_code = models.CharField(max_length=255, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    co2_absorbed_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="Total CO₂ absorption for this certificate (kg)"
    )

    class Meta:
        ordering = ['-issued_at']

    def __str__(self):
        return f"NFT Certificate #{self.id} - Token: {self.nft_token_id or 'Not Minted'}"

    def calculate_co2(self):
        """
        Calculate CO₂ absorption for this certificate based on purchased trees.
        
        Returns:
            Decimal: CO₂ absorbed in kg
        """
        plantation = self.purchase.tree_lot.plantation
        co2_per_year = plantation.calculate_yearly_co2()
        
        # Proportion based on trees purchased vs total trees
        total_trees = plantation.get_total_trees()
        if total_trees > 0:
            proportion = Decimal(str(self.purchase.quantity)) / Decimal(str(total_trees))
            certificate_co2 = co2_per_year * proportion
        else:
            certificate_co2 = Decimal('0.00')
        
        self.co2_absorbed_kg = certificate_co2
        self.save(update_fields=['co2_absorbed_kg'])
        return certificate_co2


class ISOComplianceRecord(models.Model):
    """
    ISOComplianceRecord model - tracks ISO standards compliance for buyers.
    Links purchased trees to ISO standards requirements.
    """
    ISO_STANDARD_CHOICES = [
        ('ISO 14001', 'ISO 14001 - Environmental Management'),
        ('ISO 14064', 'ISO 14064 - Greenhouse Gas Accounting'),
        ('ISO 14067', 'ISO 14067 - Carbon Footprint'),
        ('ISO 50001', 'ISO 50001 - Energy Management'),
    ]
    
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='iso_records')
    nft_certificate = models.ForeignKey(
        NFTCertificate,
        on_delete=models.CASCADE,
        related_name='iso_records'
    )
    iso_standard = models.CharField(max_length=50, choices=ISO_STANDARD_CHOICES)
    compliance_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Verification'),
            ('verified', 'Verified'),
            ('expired', 'Expired'),
        ],
        default='pending'
    )
    verification_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    verification_document_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['buyer', 'nft_certificate', 'iso_standard']

    def __str__(self):
        return f"{self.buyer.company_name} - {self.iso_standard} - {self.get_compliance_status_display()}"


class GrowthData(models.Model):
    """
    GrowthData model - tracks plantation growth and CO₂ absorption over time.
    Used for monitoring and reporting.
    """
    plantation = models.ForeignKey(Plantation, on_delete=models.CASCADE, related_name='growth_data')
    ndvi_value = models.FloatField(
        null=True,
        blank=True,
        help_text="NDVI value (placeholder - replace with real satellite data)"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    co2_absorbed_kg = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text="CO₂ absorbed at this timestamp (kg)"
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['plantation', '-timestamp']),
        ]

    def __str__(self):
        return f"Growth data for {self.plantation.name} - {self.timestamp}"
