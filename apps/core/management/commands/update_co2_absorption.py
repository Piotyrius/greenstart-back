"""
Django management command to recalculate CO₂ absorption for all certificates.

This command recalculates CO₂ absorption for all certificates based on current
plantation growth data. Can be triggered by Google Cloud Scheduler.

Usage:
    python manage.py update_co2_absorption
"""
from django.core.management.base import BaseCommand
from apps.core.models import Certificate


class Command(BaseCommand):
    help = 'Recalculate CO₂ absorption for all certificates'

    def add_arguments(self, parser):
        parser.add_argument(
            '--certificate-id',
            type=int,
            help='Update specific certificate by ID',
        )

    def handle(self, *args, **options):
        certificate_id = options.get('certificate_id')
        
        if certificate_id:
            certificates = Certificate.objects.filter(id=certificate_id)
            self.stdout.write(f'Recalculating CO₂ for certificate {certificate_id}...')
        else:
            certificates = Certificate.objects.all()
            self.stdout.write('Recalculating CO₂ for all certificates...')
        
        updated_count = 0
        
        for certificate in certificates:
            try:
                old_co2 = certificate.co2_absorbed_kg
                new_co2 = certificate.calculate_apartment_co2()
                
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Certificate {certificate.id}: {old_co2:.2f} kg -> {new_co2:.2f} kg'
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'Error updating certificate {certificate.id}: {str(e)}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} certificate(s)'
            )
        )

