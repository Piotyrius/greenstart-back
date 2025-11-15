# ✅ GREWECO Backend Rebuild Summary

## Business Model Clarification

**GREWECO is a marketplace platform that sells NFT-ized paulownia trees to:**

1. **Developers** (construction companies)
   - Buy trees for ecological projects
   - Get CO₂ certificates for buildings
   - Improve environmental credentials

2. **Foreign Companies**
   - Buy trees for ISO compliance
   - ISO 14001 (Environmental Management)
   - ISO 14064 (Greenhouse Gas Accounting)
   - ISO 14067 (Carbon Footprint)
   - Investment/ESG compliance

## What Was Rebuilt

### ✅ Removed Old Models
- ❌ Developer (replaced with Buyer)
- ❌ Building
- ❌ Apartment
- ❌ HectareLot (replaced with TreeLot)
- ❌ Certificate (replaced with NFTCertificate)

### ✅ New Marketplace Models

1. **Buyer** - Developers or Companies who purchase trees
   - `buyer_type`: developer or company
   - `iso_standards`: List of ISO standards needed
   - `country`: For foreign companies

2. **Plantation** - Trees available for sale
   - `price_per_tree`: Price per individual tree
   - `price_per_hectare`: Price per hectare
   - `is_active`: Available for sale
   - `trees_per_hectare`: Tree density
   - Methods: `get_total_trees()`, `get_available_trees()`

3. **TreeLot** - Lots of trees for purchase
   - `number_of_trees`: Trees in this lot
   - `price`: Total price for lot
   - `is_available`: Can be purchased

4. **TreePurchase** - Purchase transaction
   - Links buyer to tree lot
   - `quantity`: Number of trees purchased
   - `status`: pending/completed/cancelled
   - `total_price`: Auto-calculated

5. **NFTCertificate** - NFT ownership certificate
   - `nft_token_id`: Blockchain token ID
   - `blockchain_address`: Contract address
   - `transaction_hash`: Blockchain transaction
   - `co2_absorbed_kg`: CO₂ absorption
   - Method: `calculate_co2()`

6. **ISOComplianceRecord** - ISO standards tracking
   - Links certificate to ISO standards
   - `compliance_status`: pending/verified/expired
   - Verification dates and documents

7. **GrowthData** - Monitoring data (unchanged)

## New API Endpoints

### Marketplace Endpoints
- `GET /api/buyers/` - List buyers (developers/companies)
- `GET /api/plantations/` - List plantations for sale
- `GET /api/plantations/{id}/co2_calculation/` - CO₂ details
- `GET /api/plantations/{id}/available_lots/` - Available lots
- `GET /api/tree-lots/` - List tree lots (filter by plantation, availability)
- `POST /api/purchases/` - Create purchase (status: pending)
- `POST /api/purchases/{id}/complete_purchase/` - Complete purchase & generate NFT
- `GET /api/nft-certificates/` - List NFT certificates
- `POST /api/nft-certificates/{id}/generate_pdf/` - Generate PDF
- `POST /api/nft-certificates/{id}/mint_nft/` - Mint NFT (placeholder for Web3)
- `GET /api/iso-compliance/` - ISO compliance records

## Purchase Flow

```
1. Buyer browses plantations → GET /api/plantations/
2. Buyer views available lots → GET /api/plantations/{id}/available_lots/
3. Buyer creates purchase → POST /api/purchases/ (status: pending)
4. Payment processed (external)
5. Complete purchase → POST /api/purchases/{id}/complete_purchase/
   - Creates NFTCertificate
   - Calculates CO₂
   - Marks lot unavailable if sold out
6. Mint NFT → POST /api/nft-certificates/{id}/mint_nft/ (Web3)
7. Generate PDF → POST /api/nft-certificates/{id}/generate_pdf/
8. Link ISO compliance → POST /api/iso-compliance/
```

## Files Updated

✅ `apps/core/models.py` - New marketplace models
✅ `apps/core/admin.py` - Updated for new models
✅ `apps/core/serializers.py` - New serializers
✅ `apps/core/views.py` - New API views
✅ `apps/core/urls.py` - New URL routes
✅ `apps/core/utils/pdf_generator.py` - Updated for NFTCertificate
✅ Migrations created - `0001_initial.py`

## Status

🟢 **Backend successfully rebuilt as marketplace platform!**

- ✅ All models reflect marketplace business model
- ✅ API endpoints for selling trees
- ✅ NFT certificate generation ready
- ✅ ISO compliance tracking
- ✅ CO₂ calculation system
- ✅ PDF certificate generation
- ✅ Google Cloud integration

## Next Steps

1. Run migrations: `python manage.py migrate`
2. Create superuser: `python manage.py createsuperuser`
3. Test API endpoints
4. Update frontend to match new API structure
5. Integrate Web3 NFT minting (Polygon blockchain)

## Questions Answered

✅ **What are we building?**
- Marketplace for selling NFT-ized trees to developers and companies

✅ **Who buys trees?**
- Developers (construction companies)
- Foreign companies (for ISO compliance)

✅ **What do buyers get?**
- NFT ownership certificate
- CO₂ absorption certificate
- ISO compliance documentation
- PDF certificate

✅ **How does it work?**
- Trees listed for sale → Buyer purchases → NFT certificate issued → ISO compliance tracked

