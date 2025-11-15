# ✅ B2B and B2C Support - Implementation Complete

## Summary

The GREWECO platform now fully supports **B2B (Business-to-Business)** and **B2C (Business-to-Consumer)** selling models with:

- ✅ Separate sectors for plantations and tree lots
- ✅ Different pricing for B2B and B2C
- ✅ Company logo support for B2B buyers
- ✅ Automatic validation (B2B buyers can only buy B2B lots)
- ✅ Sector-based filtering in API
- ✅ Logo display in PDF certificates

## Forest Division

### Plantation Sectors
- **B2B Sector**: Trees allocated for business/company sales
- **B2C Sector**: Trees allocated for individual consumer sales  
- **Mixed Sector**: Plantation can have both B2B and B2C lots

### Tree Lot Assignment
- Each `TreeLot` is assigned to either `b2b` or `b2c` sector
- Lots are physically divided in the forest
- Separate pricing for each sector

## B2B Features

### Company Information
- Company name (required)
- **Company logo** (uploaded to Google Cloud Storage)
- Country
- Tax ID/VAT number
- Website
- ISO standards tracking

### Logo Support
- Logo upload endpoint: `POST /api/buyers/{id}/upload_logo/`
- Logos stored in Google Cloud Storage
- Displayed in:
  - Admin panel (with preview)
  - PDF certificates
  - API responses
  - Frontend (when implemented)

### Pricing
- `b2b_price_per_tree` - B2B price per tree
- `b2b_price_per_hectare` - B2B price per hectare
- `b2b_price` on TreeLot - B2B price for specific lot

## B2C Features

### Individual Information
- Personal name
- Email
- Phone number
- Address

### Pricing
- `b2c_price_per_tree` - B2C price per tree
- `b2c_price_per_hectare` - B2C price per hectare
- `b2c_price` on TreeLot - B2C price for specific lot

## API Usage

### Filter Plantations by Sector
```bash
GET /api/plantations/?sector=b2b
GET /api/plantations/?sector=b2c
GET /api/plantations/?sector=mixed
```

### Filter Tree Lots by Sector
```bash
GET /api/tree-lots/?sector=b2b
GET /api/tree-lots/?sector=b2c
GET /api/plantations/{id}/available_lots/?sector=b2b
```

### Filter Buyers by Type
```bash
GET /api/buyers/?buyer_type=b2b
GET /api/buyers/?buyer_type=b2c
```

### Upload Company Logo (B2B only)
```bash
POST /api/buyers/{id}/upload_logo/
Content-Type: multipart/form-data
logo: <image file>
```

## Purchase Validation

The system automatically validates:
1. **Buyer type matches lot sector**
   - B2B buyers → can only buy B2B lots
   - B2C buyers → can only buy B2C lots
2. **Correct pricing applied**
   - Price automatically adjusted based on buyer type
3. **Company name required for B2B**
   - Validation error if B2B buyer missing company name

## Certificate Generation

### B2B Certificates Include:
- ✅ **Company logo** (if uploaded)
- ✅ Company name
- ✅ Company website
- ✅ Tax ID
- ✅ ISO compliance records
- ✅ CO₂ absorption data

### B2C Certificates Include:
- ✅ Personal name
- ✅ Contact information
- ✅ Address
- ✅ CO₂ absorption data

## Admin Panel

- **Buyer Admin**:
  - Filter by buyer type (B2B/B2C)
  - Logo preview for B2B buyers
  - "Has Logo" indicator

- **Plantation Admin**:
  - Filter by sector (B2B/B2C/Mixed)
  - Display sector in list view

- **TreeLot Admin**:
  - Filter by sector
  - Display both B2B and B2C prices

## Database Schema

### Buyer Model
```python
buyer_type: 'b2b' | 'b2c'
company_name: str (required for B2B)
company_logo: URL (B2B only)
country: str (B2B)
iso_standards: JSON (B2B)
tax_id: str (B2B)
website: URL (B2B)
phone: str (B2C)
address: str (B2C)
```

### Plantation Model
```python
sector: 'b2b' | 'b2c' | 'mixed'
b2b_price_per_tree: Decimal
b2b_price_per_hectare: Decimal
b2c_price_per_tree: Decimal
b2c_price_per_hectare: Decimal
```

### TreeLot Model
```python
sector: 'b2b' | 'b2c'
b2b_price: Decimal
b2c_price: Decimal
get_price_for_buyer_type(buyer_type): Decimal
```

## Status

🟢 **B2B and B2C support fully implemented!**

- ✅ Models updated with sectors
- ✅ Separate pricing for B2B/B2C
- ✅ Company logo upload and display
- ✅ Sector-based filtering
- ✅ Purchase validation
- ✅ PDF certificates with logos
- ✅ Admin panel updates
- ✅ API endpoints ready

## Next Steps for Frontend

1. Create separate registration forms for B2B vs B2C
2. Add logo upload component for B2B buyers
3. Filter plantations/lots by sector
4. Display company logos in buyer profiles
5. Show appropriate pricing based on buyer type
6. Validate buyer type before purchase

