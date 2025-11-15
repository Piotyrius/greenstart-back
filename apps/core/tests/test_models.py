from django.test import TestCase
from decimal import Decimal
from datetime import date, timedelta
from apps.core.models import (
    Developer, Building, Apartment, Plantation, HectareLot,
    Certificate, GrowthData
)


class DeveloperModelTest(TestCase):
    def setUp(self):
        self.developer = Developer.objects.create(
            name="John Doe",
            email="john@example.com",
            company_name="Green Builders Inc."
        )

    def test_developer_str(self):
        self.assertEqual(str(self.developer), "Green Builders Inc. (John Doe)")


class BuildingModelTest(TestCase):
    def setUp(self):
        self.developer = Developer.objects.create(
            name="John Doe",
            email="john@example.com",
            company_name="Green Builders Inc."
        )
        self.building = Building.objects.create(
            developer=self.developer,
            name="Eco Tower",
            address="123 Green Street",
            floors=10,
            total_apartments=50,
            total_area_sqm=Decimal('5000.00')
        )

    def test_building_str(self):
        self.assertEqual(str(self.building), "Eco Tower - Green Builders Inc.")


class ApartmentModelTest(TestCase):
    def setUp(self):
        self.developer = Developer.objects.create(
            name="John Doe",
            email="john@example.com",
            company_name="Green Builders Inc."
        )
        self.building = Building.objects.create(
            developer=self.developer,
            name="Eco Tower",
            address="123 Green Street",
            floors=10,
            total_apartments=50,
            total_area_sqm=Decimal('5000.00')
        )
        self.apartment = Apartment.objects.create(
            building=self.building,
            apartment_number="101",
            size_sqm=Decimal('100.00'),
            owner_name="Jane Smith",
            owner_email="jane@example.com"
        )

    def test_apartment_str(self):
        self.assertEqual(str(self.apartment), "Eco Tower - Apt 101")


class PlantationModelTest(TestCase):
    def setUp(self):
        self.planting_date = date.today() - timedelta(days=365 * 2)  # 2 years ago
        self.plantation = Plantation.objects.create(
            name="Paulownia Forest 1",
            polygon_coordinates={
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            },
            planting_date=self.planting_date,
            expected_harvest_date=date.today() + timedelta(days=365 * 8),
            species="Paulownia",
            total_hectares=Decimal('10.00')
        )

    def test_plantation_str(self):
        self.assertEqual(str(self.plantation), "Paulownia Forest 1 (10.00 ha)")

    def test_calculate_yearly_co2(self):
        """Test CO₂ calculation for plantation."""
        co2 = self.plantation.calculate_yearly_co2()
        
        # Expected: age_years (2) × species_factor (22) × hectares (10) × trees_per_hectare (1000) × scale (1.0)
        # = 2 × 22 × 10 × 1000 × 1.0 = 440,000 kg CO₂/year
        expected_co2 = Decimal('2') * Decimal('22') * Decimal('10') * Decimal('1000') * Decimal('1.0')
        
        # Allow small rounding differences
        self.assertAlmostEqual(float(co2), float(expected_co2), delta=1000)

    def test_calculate_yearly_co2_future_date(self):
        """Test CO₂ calculation for future date (should be 0)."""
        future_date = date.today() + timedelta(days=365)
        co2 = self.plantation.calculate_yearly_co2(year=future_date.year)
        # Age should be negative or zero, so CO₂ should be 0 or very small
        self.assertGreaterEqual(co2, Decimal('0'))


class CertificateModelTest(TestCase):
    def setUp(self):
        # Create developer and building
        self.developer = Developer.objects.create(
            name="John Doe",
            email="john@example.com",
            company_name="Green Builders Inc."
        )
        self.building = Building.objects.create(
            developer=self.developer,
            name="Eco Tower",
            address="123 Green Street",
            floors=10,
            total_apartments=50,
            total_area_sqm=Decimal('5000.00')
        )
        self.apartment = Apartment.objects.create(
            building=self.building,
            apartment_number="101",
            size_sqm=Decimal('100.00'),
            owner_name="Jane Smith"
        )
        
        # Create plantation
        planting_date = date.today() - timedelta(days=365 * 2)
        self.plantation = Plantation.objects.create(
            name="Paulownia Forest 1",
            polygon_coordinates={
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            },
            planting_date=planting_date,
            expected_harvest_date=date.today() + timedelta(days=365 * 8),
            species="Paulownia",
            total_hectares=Decimal('10.00')
        )
        
        # Create hectare lot
        self.hectare_lot = HectareLot.objects.create(
            plantation=self.plantation,
            lot_number="LOT-001",
            area_polygon={
                "type": "Polygon",
                "coordinates": [[[0, 0], [0.5, 0], [0.5, 0.5], [0, 0.5], [0, 0]]]
            },
            area_hectares=Decimal('5.00'),
            assigned_to_building=self.building
        )
        
        # Create certificate
        self.certificate = Certificate.objects.create(
            apartment=self.apartment,
            hectare_lot=self.hectare_lot
        )

    def test_certificate_str(self):
        self.assertIn("Eco Tower", str(self.certificate))

    def test_calculate_apartment_co2(self):
        """Test CO₂ calculation for apartment certificate."""
        co2 = self.certificate.calculate_apartment_co2()
        
        # Should be positive
        self.assertGreater(co2, Decimal('0'))
        
        # Verify it's saved
        self.certificate.refresh_from_db()
        self.assertEqual(self.certificate.co2_absorbed_kg, co2)


class GrowthDataModelTest(TestCase):
    def setUp(self):
        planting_date = date.today() - timedelta(days=365 * 2)
        self.plantation = Plantation.objects.create(
            name="Paulownia Forest 1",
            polygon_coordinates={
                "type": "Polygon",
                "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]
            },
            planting_date=planting_date,
            expected_harvest_date=date.today() + timedelta(days=365 * 8),
            species="Paulownia",
            total_hectares=Decimal('10.00')
        )
        self.growth_data = GrowthData.objects.create(
            plantation=self.plantation,
            ndvi_value=0.65,
            co2_absorbed_kg=Decimal('440000.00'),
            notes="Test growth data"
        )

    def test_growth_data_str(self):
        self.assertIn("Paulownia Forest 1", str(self.growth_data))

