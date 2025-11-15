# ✅ Marketplace Platform Rebuild Complete

## Business Model Clarified

**GREWECO is a marketplace that sells NFT-ized paulownia trees to:**
- **Developers** (construction companies) - for ecological projects
- **Foreign Companies** - for ISO compliance (ISO 14001, 14064, 14067, etc.)

## New Model Structure ✅

### 1. **Buyer** (replaces Developer)
- Can be: `developer` OR `company`
- Tracks ISO standards needed
- Country field for foreign companies
- Links to purchases

### 2. **Plantation**
- Trees available for sale
- Pricing: `price_per_tree` and `price_per_hectare`
- `is_active` status for availability
- Methods: `calculate_yearly_co2()`, `get_total_trees()`, `get_available_trees()`

### 3. **TreeLot**
- Lots of trees/hectares for purchase
- `number_of_trees` in lot
- `price` per lot
- `is_available` status

### 4. **TreePurchase**
- Transaction when trees are sold
- Links `buyer` to `tree_lot`
- `quantity` of trees purchased
- `status`: pending/completed/cancelled
- Payment tracking

### 5. **NFTCertificate**
- NFT ownership certificate (blockchain)
- `nft_token_id` for blockchain token
- `blockchain_address` and `transaction_hash`
- CO₂ absorption data
- PDF certificate URL
- Method: `calculate_co2()`

### 6. **ISOComplianceRecord**
- Links purchases to ISO standards
- Tracks: ISO 14001, 14064, 14067, 50001
- `compliance_status`: pending/verified/expired
- Verification dates and documents

### 7. **GrowthData**
- Monitoring data for plantations
- NDVI values
- CO₂ tracking over time

## API Endpoints ✅

- `/api/buyers/` - List/create buyers (developers/companies)
- `/api/plantations/` - List plantations for sale
- `/api/plantations/{id}/co2_calculation/` - CO₂ calculation details
- `/api/plantations/{id}/available_lots/` - Available tree lots
- `/api/tree-lots/` - List tree lots (filter by plantation, availability)
- `/api/purchases/` - Tree purchase transactions
- `/api/purchases/{id}/complete_purchase/` - Complete purchase & generate NFT
- `/api/nft-certificates/` - NFT ownership certificates
- `/api/nft-certificates/{id}/generate_pdf/` - Generate PDF certificate
- `/api/nft-certificates/{id}/mint_nft/` - Mint NFT on blockchain (placeholder)
- `/api/iso-compliance/` - ISO compliance records
- `/api/growth-data/` - Growth monitoring data

## Purchase Flow

1. **List Plantations** → Buyer sees available trees
2. **Select TreeLot** → Buyer chooses lot to purchase
3. **Create Purchase** → `POST /api/purchases/` (status: pending)
4. **Complete Purchase** → `POST /api/purchases/{id}/complete_purchase/`
   - Creates NFTCertificate
   - Calculates CO₂
   - Marks lot as unavailable if sold out
5. **Mint NFT** → `POST /api/nft-certificates/{id}/mint_nft/` (Web3 integration)
6. **Generate PDF** → `POST /api/nft-certificates/{id}/generate_pdf/`
7. **ISO Compliance** → Link certificate to ISO standards

## Next Steps

1. ✅ Models rebuilt for marketplace
2. ✅ Admin panel updated
3. ✅ Serializers created
4. ✅ Views/API endpoints created
5. ✅ Migrations created
6. ⏳ Update PDF generator for NFTCertificate
7. ⏳ Update tests
8. ⏳ Update frontend to match new API

## Key Features

- **Marketplace**: Trees are sold, not just allocated
- **Buyer Types**: Developer vs Company
- **NFT Ready**: Blockchain token ID field
- **ISO Compliance**: Dedicated tracking
- **CO₂ Tracking**: Automatic calculation
- **Pricing**: Per tree and per hectare

## Status

🟢 **Backend rebuilt as marketplace platform!**

Ready for:
- Selling trees to developers/companies
- NFT certificate generation
- ISO compliance tracking
- CO₂ credit management

