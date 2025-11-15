# B2B and B2C Support - Complete Implementation

## Overview

GREWECO platform now fully supports **B2B (Business-to-Business)** and **B2C (Business-to-Consumer)** selling models with separate sectors, pricing, and features.

## Key Features

### ✅ B2B Support
- **Company logos** - B2B buyers can upload company logos
- **Separate pricing** - B2B-specific pricing per tree/hectare
- **ISO compliance** - Track ISO standards (14001, 14064, 14067)
- **Company details** - Tax ID, website, country
- **Logo display** - Logos shown in certificates and admin

### ✅ B2C Support
- **Individual buyers** - Personal information (phone, address)
- **Separate pricing** - B2C-specific pricing (typically different from B2B)
- **Simplified flow** - Consumer-friendly purchase process

### ✅ Sector Division
- **Plantations** can be: B2B, B2C, or Mixed
- **Tree Lots** assigned to specific sector (B2B or B2C)
- **Automatic validation** - B2B buyers can only buy B2B lots, B2C buyers can only buy B2C lots

## Model Updates

### Buyer Model
```python
buyer_type: 'b2b' or 'b2c'

# B2B fields:
- company_name (required for B2B)
- company_logo (URL to logo in GCS)
- country
- iso_standards (JSON list)
- tax_id
- website

# B2C fields:
- phone
- address
```

### Plantation Model
```python
sector: 'b2b', 'b2c', or 'mixed'

# B2B pricing:
- b2b_price_per_tree
- b2b_price_per_hectare

# B2C pricing:
- b2c_price_per_tree
- b2c_price_per_hectare
```

### TreeLot Model
```python
sector: 'b2b' or 'b2c'

# Pricing:
- b2b_price (for B2B buyers)
- b2c_price (for B2C buyers)

# Method:
- get_price_for_buyer_type(buyer_type) - Returns correct price
```

## API Endpoints

### Filter by Sector

**Plantations:**
```bash
GET /api/plantations/?sector=b2b
GET /api/plantations/?sector=b2c
GET /api/plantations/?sector=mixed
```

**Tree Lots:**
```bash
GET /api/tree-lots/?sector=b2b
GET /api/tree-lots/?sector=b2c
GET /api/plantations/{id}/available_lots/?sector=b2b
```

### Buyer Registration

**B2B Buyer:**
```json
POST /api/buyers/
{
  "name": "John Doe",
  "email": "john@company.com",
  "buyer_type": "b2b",
  "company_name": "Eco Corp",
  "company_logo": "https://storage.googleapis.com/.../logo.png",
  "country": "USA",
  "iso_standards": ["ISO 14001", "ISO 14064"],
  "tax_id": "TAX123456",
  "website": "https://ecocorp.com"
}
```

**B2C Buyer:**
```json
POST /api/buyers/
{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "buyer_type": "b2c",
  "phone": "+1234567890",
  "address": "123 Main St, City, Country"
}
```

## Purchase Flow

1. **Buyer registers** (B2B or B2C)
2. **Browse plantations** filtered by sector
3. **View available lots** for their buyer type
4. **Create purchase** - System validates buyer type matches lot sector
5. **Complete purchase** - Price automatically adjusted based on buyer type
6. **NFT certificate** generated with:
   - Company logo (for B2B)
   - Appropriate buyer information
   - CO₂ data
   - ISO compliance (for B2B)

## Logo Upload

### For B2B Buyers

**Option 1: Via API (future)**
```bash
POST /api/buyers/{id}/upload-logo/
Content-Type: multipart/form-data
file: <logo image>
```

**Option 2: Via Admin Panel**
- Upload logo in Django admin
- Logo stored in Google Cloud Storage
- URL saved to `company_logo` field

**Option 3: Direct URL**
- Set `company_logo` field to external URL
- Logo will be displayed in certificates

## Certificate Display

### B2B Certificates Include:
- ✅ Company logo (if provided)
- ✅ Company name
- ✅ ISO compliance records
- ✅ Company website
- ✅ Tax ID

### B2C Certificates Include:
- ✅ Personal name
- ✅ Contact information
- ✅ Address

## Validation Rules

1. **B2B buyers** must have `company_name`
2. **B2B buyers** can only purchase from `sector='b2b'` lots
3. **B2C buyers** can only purchase from `sector='b2c'` lots
4. **Mixed plantations** can have both B2B and B2C lots
5. **Pricing** automatically uses correct price based on buyer type

## Admin Panel Features

- Filter buyers by type (B2B/B2C)
- Filter plantations by sector
- Filter tree lots by sector
- Logo preview for B2B buyers
- Separate pricing display for B2B/B2C

## Frontend Integration

Frontend should:
1. Show different registration forms for B2B vs B2C
2. Filter plantations/lots by sector
3. Display company logos for B2B buyers
4. Show appropriate pricing based on buyer type
5. Validate buyer type matches lot sector before purchase

## Status

🟢 **B2B and B2C support fully implemented!**

- ✅ Models updated with sectors and pricing
- ✅ Buyer types (B2B/B2C) with appropriate fields
- ✅ Company logo support for B2B
- ✅ Sector-based filtering
- ✅ Automatic price selection
- ✅ Purchase validation
- ✅ Certificate generation with logos
- ✅ Admin panel updates

