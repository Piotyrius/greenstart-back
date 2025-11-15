from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date, timedelta
from apps.core.models import (
    Developer, Building, Apartment, Plantation, HectareLot, Certificate
)

User = get_user_model()


class DeveloperAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.developer = Developer.objects.create(
            name="John Doe",
            email="john@example.com",
            company_name="Green Builders Inc."
        )

    def test_list_developers(self):
        response = self.client.get('/api/developers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_developer_requires_admin(self):
        response = self.client.post('/api/developers/', {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'company_name': 'Eco Builders'
        })
        # Should fail because user is not admin
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class BuildingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.developer = Developer.objects.create(
            name="John Doe",
            email="john@example.com",
            company_name="Green Builders Inc."
        )

    def test_list_buildings(self):
        Building.objects.create(
            developer=self.developer,
            name="Eco Tower",
            address="123 Green Street",
            floors=10,
            total_apartments=50,
            total_area_sqm=Decimal('5000.00')
        )
        response = self.client.get('/api/buildings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_buildings_by_developer(self):
        building = Building.objects.create(
            developer=self.developer,
            name="Eco Tower",
            address="123 Green Street",
            floors=10,
            total_apartments=50,
            total_area_sqm=Decimal('5000.00')
        )
        response = self.client.get(f'/api/buildings/?developer={self.developer.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class PlantationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
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

    def test_list_plantations(self):
        response = self.client.get('/api/plantations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_plantation_includes_co2_data(self):
        response = self.client.get(f'/api/plantations/{self.plantation.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('yearly_co2_absorbed', response.data)
        self.assertIsInstance(response.data['yearly_co2_absorbed'], float)

    def test_co2_calculation_endpoint(self):
        response = self.client.get(f'/api/plantations/{self.plantation.id}/co2_calculation/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('yearly_co2_absorbed_kg', response.data)
        self.assertIn('formula_breakdown', response.data)


class CertificateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test data
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

    def test_create_certificate(self):
        response = self.client.post('/api/certificates/', {
            'apartment': self.apartment.id,
            'hectare_lot': self.hectare_lot.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('co2_absorbed_kg', response.data)

    def test_certificate_includes_co2_data(self):
        certificate = Certificate.objects.create(
            apartment=self.apartment,
            hectare_lot=self.hectare_lot
        )
        certificate.calculate_apartment_co2()
        
        response = self.client.get(f'/api/certificates/{certificate.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('co2_absorbed_kg', response.data)

