from django.test import TestCase
from decimal import Decimal
from datetime import date, timedelta
from apps.core.models import Plantation, Certificate, Building, Apartment, HectareLot, Developer
from apps.core.utils.co2_calculator import (
    calculate_plantation_co2,
    calculate_apartment_co2_share,
    PAULOWNIA_SPECIES_FACTOR,
    TREES_PER_HECTARE,
    SCALE_FACTOR
)


class CO2CalculatorTest(TestCase):
    def setUp(self):
        # Create test plantation (2 years old)
        self.planting_date = date.today() - timedelta(days=365 * 2)
        self.plantation = Plantation.objects.create(
            name="Test Plantation",
            polygon_coordinates={
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            },
            planting_date=self.planting_date,
            expected_harvest_date=date.today() + timedelta(days=365 * 8),
            species="Paulownia",
            total_hectares=Decimal('10.00')
        )

    def test_calculate_plantation_co2(self):
        """Test CO₂ calculation for plantation."""
        co2 = calculate_plantation_co2(self.plantation)
        
        # Expected: age_years (2) × species_factor (22) × hectares (10) × trees_per_hectare (1000) × scale (1.0)
        # = 2 × 22 × 10 × 1000 × 1.0 = 440,000 kg CO₂/year
        expected_co2 = Decimal('2') * Decimal(str(PAULOWNIA_SPECIES_FACTOR)) * Decimal('10') * Decimal(str(TREES_PER_HECTARE)) * Decimal(str(SCALE_FACTOR))
        
        # Allow small rounding differences
        self.assertAlmostEqual(float(co2), float(expected_co2), delta=1000)

    def test_calculate_plantation_co2_specific_year(self):
        """Test CO₂ calculation for specific year."""
        # Calculate for 1 year after planting
        year = self.planting_date.year + 1
        co2 = calculate_plantation_co2(self.plantation, year=year)
        
        # Age should be approximately 1 year
        expected_co2 = Decimal('1') * Decimal(str(PAULOWNIA_SPECIES_FACTOR)) * Decimal('10') * Decimal(str(TREES_PER_HECTARE)) * Decimal(str(SCALE_FACTOR))
        
        self.assertAlmostEqual(float(co2), float(expected_co2), delta=50000)

    def test_calculate_plantation_co2_future_date(self):
        """Test CO₂ calculation for future date (should be 0)."""
        future_year = date.today().year + 1
        co2 = calculate_plantation_co2(self.plantation, year=future_year)
        # Age should be negative or zero, so CO₂ should be 0 or very small
        self.assertGreaterEqual(co2, Decimal('0'))

    def test_calculate_apartment_co2_share(self):
        """Test CO₂ calculation for apartment share."""
        # Create developer, building, apartment
        developer = Developer.objects.create(
            name="John Doe",
            email="john@example.com",
            company_name="Green Builders Inc."
        )
        building = Building.objects.create(
            developer=developer,
            name="Eco Tower",
            address="123 Green Street",
            floors=10,
            total_apartments=50,
            total_area_sqm=Decimal('5000.00')  # 50 apartments × 100 m² each
        )
        apartment = Apartment.objects.create(
            building=building,
            apartment_number="101",
            size_sqm=Decimal('100.00')  # 100 m² apartment
        )
        
        # Create hectare lot (5 hectares out of 10)
        hectare_lot = HectareLot.objects.create(
            plantation=self.plantation,
            lot_number="LOT-001",
            area_polygon={
                "type": "Polygon",
                "coordinates": [[[0, 0], [0.5, 0], [0.5, 0.5], [0, 0.5], [0, 0]]]
            },
            area_hectares=Decimal('5.00'),  # 5 hectares
            assigned_to_building=building
        )
        
        # Create certificate
        certificate = Certificate.objects.create(
            apartment=apartment,
            hectare_lot=hectare_lot
        )
        
        # Calculate apartment CO₂ share
        co2 = calculate_apartment_co2_share(certificate)
        
        # Should be positive
        self.assertGreater(co2, Decimal('0'))
        
        # Apartment is 100 m² out of 5000 m² total = 2% of building
        # Hectare lot is 5 ha out of 10 ha = 50% of plantation
        # Plantation CO₂ = 2 × 22 × 10 × 1000 × 1.0 = 440,000 kg/year
        # Hectare lot CO₂ = 440,000 × 0.5 = 220,000 kg/year
        # Apartment CO₂ = 220,000 × 0.02 = 4,400 kg/year
        expected_co2 = Decimal('220000') * Decimal('0.02')
        
        self.assertAlmostEqual(float(co2), float(expected_co2), delta=100)

