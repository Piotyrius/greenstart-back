"""
Django management command to update NDVI data and CO₂ absorption.

This command simulates NDVI updates and calculates CO₂ absorption for all plantations.
Can be triggered by Google Cloud Scheduler via HTTP endpoint.

Usage:
    python manage.py update_ndvi_data
    python manage.py update_ndvi_data --year 2024
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from apps.core.models import Plantation, GrowthData
from apps.core.utils.co2_calculator import calculate_plantation_co2
import random


class Command(BaseCommand):
    help = 'Update NDVI data and CO₂ absorption for all plantations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=int,
            help='Year to calculate for (default: current year)',
        )
        parser.add_argument(
            '--simulate',
            action='store_true',
            help='Simulate NDVI values (placeholder)',
        )

    def handle(self, *args, **options):
        year = options.get('year')
        simulate = options.get('simulate', True)
        
        if year is None:
            today = date.today()
            year = today.year
        
        self.stdout.write(f'Updating NDVI and CO₂ data for year {year}...')
        
        plantations = Plantation.objects.all()
        updated_count = 0
        
        for plantation in plantations:
            # Calculate CO₂ absorption
            co2_absorbed = calculate_plantation_co2(plantation, year)
            
            # Simulate NDVI value (placeholder - replace with real satellite data)
            if simulate:
                # NDVI typically ranges from -1 to 1, healthy vegetation is 0.3-0.8
                # Simulate based on plantation age
                age_years = (date(year, 12, 31) - plantation.planting_date).days / 365.25
                if age_years < 0:
                    age_years = 0
                
                # Simulate NDVI: newer plantations have lower NDVI, mature ones higher
                base_ndvi = 0.3 + min(age_years / 10, 0.5)  # Cap at 0.8
                ndvi_value = base_ndvi + random.uniform(-0.1, 0.1)
                ndvi_value = max(0.0, min(1.0, ndvi_value))  # Clamp to valid range
            else:
                ndvi_value = None
            
            # Create or update GrowthData record
            growth_data, created = GrowthData.objects.get_or_create(
                plantation=plantation,
                timestamp__year=year,
                defaults={
                    'ndvi_value': ndvi_value,
                    'co2_absorbed_kg': co2_absorbed,
                    'notes': f'Auto-generated data for year {year}',
                }
            )
            
            if not created:
                # Update existing record
                growth_data.ndvi_value = ndvi_value
                growth_data.co2_absorbed_kg = co2_absorbed
                growth_data.notes = f'Updated data for year {year}'
                growth_data.save()
            
            updated_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Updated {plantation.name}: CO₂ = {co2_absorbed:.2f} kg, NDVI = {ndvi_value:.2f if ndvi_value else "N/A"}'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} plantation(s)'
            )
        )

