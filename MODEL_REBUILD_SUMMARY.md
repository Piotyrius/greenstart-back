# Model Rebuild Summary - Marketplace Platform

## Business Model Understanding

✅ **GREWECO is a marketplace that sells NFT-ized trees to:**
- Developers (construction companies) - for ecological projects
- Foreign Companies - for ISO compliance (ISO 14001, 14064, 14067, etc.)

## New Model Structure

### Core Models (Marketplace)

1. **Buyer** (replaces Developer)
   - Can be: Developer OR Company
   - Tracks ISO standards needed
   - Country field for foreign companies

2. **Plantation**
   - Trees available for sale
   - Pricing: per tree and per hectare
   - Active/inactive status
   - Methods: calculate CO₂, get available trees

3. **TreeLot**
   - Lots of trees/hectares for purchase
   - Pricing per lot
   - Available/unavailable status

4. **TreePurchase**
   - Transaction when trees are sold
   - Links buyer to tree lot
   - Payment tracking
   - Status: pending/completed/cancelled

5. **NFTCertificate**
   - NFT ownership certificate
   - Blockchain token ID
   - CO₂ absorption data
   - PDF certificate

6. **ISOComplianceRecord**
   - Links purchases to ISO standards
   - Tracks compliance status
   - Verification dates

7. **GrowthData**
   - Monitoring data
   - NDVI values
   - CO₂ tracking

## Next Steps

1. ✅ Models rebuilt
2. ✅ Admin updated
3. ⏳ Update serializers.py
4. ⏳ Update views.py
5. ⏳ Update urls.py
6. ⏳ Create new migrations
7. ⏳ Update tests

## Key Changes

- **Marketplace focus**: Trees are SOLD, not just allocated
- **Buyer types**: Developer vs Company
- **Purchase flow**: TreeLot → TreePurchase → NFTCertificate
- **ISO compliance**: Dedicated tracking model
- **NFT integration**: Ready for blockchain minting

