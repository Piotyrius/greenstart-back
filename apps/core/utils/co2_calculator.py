"""
CO₂ Absorption Calculator Utilities

This module contains centralized CO₂ calculation functions for plantations and certificates.
All species factors and rates are PLACEHOLDERS and should be replaced with real
biomass-based formulas and coefficients in future iterations.
"""
from decimal import Decimal
from datetime import date
from apps.core.models import Plantation, Certificate

# PLACEHOLDER Constants - Replace with real biomass data later
# These values are estimates and should be calibrated with actual paulownia growth data

# Species factor: kg CO₂ per tree per year
# PLACEHOLDER: This is an estimated value for paulownia trees
# Should be replaced with species-specific biomass growth data
PAULOWNIA_SPECIES_FACTOR = 22  # kg CO₂ per tree per year

# Trees per hectare
# PLACEHOLDER: Standard planting density for paulownia plantations
# Should be adjusted based on actual plantation configuration
TREES_PER_HECTARE = 1000

# Scale factor for annual rate calculation
# PLACEHOLDER: Used for future adjustments and calibration
# Should be set to 1.0 initially, adjusted based on real data
SCALE_FACTOR = 1.0


def calculate_plantation_co2(plantation, year=None):
    """
    Calculate CO₂ absorbed per year for a plantation.
    
    Formula: age_years × species_factor × hectares × annual_rate
    
    Where:
    - age_years = number of years since planting
    - species_factor = PAULOWNIA_SPECIES_FACTOR (kg CO₂ per tree per year) - PLACEHOLDER
    - hectares = total_hectares of plantation
    - annual_rate = TREES_PER_HECTARE × SCALE_FACTOR - PLACEHOLDER
    
    Args:
        plantation: Plantation instance
        year: Optional year to calculate for. If None, uses current year.
        
    Returns:
        Decimal: CO₂ absorbed in kg per year
        
    Note:
        This is a PLACEHOLDER formula. Replace with real biomass-based calculations
        that account for tree age, growth rates, and environmental factors.
    """
    if year is None:
        today = date.today()
    else:
        today = date(year, 12, 31)
    
    # Calculate age in years
    age_years = (today - plantation.planting_date).days / 365.25
    
    # Ensure age is not negative
    if age_years < 0:
        age_years = 0
    
    # Calculate CO₂ absorbed per year
    # PLACEHOLDER formula - replace with real biomass-based calculations later
    co2_per_year = (
        Decimal(str(age_years)) *
        Decimal(str(PAULOWNIA_SPECIES_FACTOR)) *
        plantation.total_hectares *
        Decimal(str(TREES_PER_HECTARE)) *
        Decimal(str(SCALE_FACTOR))
    )
    
    return co2_per_year


def calculate_apartment_co2_share(certificate):
    """
    Calculate apartment's share of CO₂ absorption from a certificate.
    
    Formula: CO2_absorbed_per_year × (apartment_area / total_building_area)
    
    Uses plantation's calculate_yearly_co2() for the hectare lot's plantation.
    Proportions based on apartment size vs building total area.
    
    Args:
        certificate: Certificate instance
        
    Returns:
        Decimal: CO₂ absorbed in kg for this apartment
        
    Note:
        This calculation assumes equal distribution of hectare lot CO₂ across
        all apartments in the building based on area. Adjust if different
        allocation methods are needed.
    """
    # Get the plantation from hectare lot
    plantation = certificate.hectare_lot.plantation
    
    # Calculate CO₂ absorbed per year for the hectare lot
    # Proportion the hectare lot's area to the plantation total
    hectare_proportion = certificate.hectare_lot.area_hectares / plantation.total_hectares
    plantation_co2_per_year = calculate_plantation_co2(plantation)
    hectare_co2_per_year = plantation_co2_per_year * hectare_proportion
    
    # Calculate apartment's share based on area proportion
    building = certificate.apartment.building
    if building.total_area_sqm > 0:
        apartment_proportion = certificate.apartment.size_sqm / building.total_area_sqm
        apartment_co2 = hectare_co2_per_year * Decimal(str(apartment_proportion))
    else:
        apartment_co2 = Decimal('0.00')
    
    return apartment_co2

