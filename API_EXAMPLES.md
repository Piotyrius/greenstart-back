# API Examples

Example API requests for the GREWECO backend.

## Authentication

### Register
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer1",
    "email": "dev@example.com",
    "password": "securepassword123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "developer1",
    "password": "securepassword123"
  }'
```

Response:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "developer1",
    "email": "dev@example.com"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

## Using the Access Token

Set the token as an environment variable:
```bash
export ACCESS_TOKEN="your-access-token-here"
```

Or use it directly in requests:
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/buildings/
```

## Developers

### List Developers
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/developers/
```

### Get Developer
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/developers/1/
```

## Buildings

### List Buildings
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/buildings/
```

### Filter by Developer
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  "http://localhost:8000/api/buildings/?developer=1"
```

### Create Building (Admin only)
```bash
curl -X POST http://localhost:8000/api/buildings/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "developer": 1,
    "name": "Eco Tower",
    "address": "123 Green Street, Batumi",
    "floors": 10,
    "total_apartments": 50,
    "total_area_sqm": 5000.00
  }'
```

## Apartments

### List Apartments
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/apartments/
```

### Filter by Building
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  "http://localhost:8000/api/apartments/?building=1"
```

### Create Apartment
```bash
curl -X POST http://localhost:8000/api/apartments/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "building": 1,
    "apartment_number": "101",
    "size_sqm": 100.00,
    "owner_name": "Jane Smith",
    "owner_email": "jane@example.com"
  }'
```

## Plantations

### List Plantations
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/plantations/
```

Response includes `yearly_co2_absorbed`:
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "name": "Paulownia Forest 1",
      "species": "Paulownia",
      "total_hectares": "10.0000",
      "yearly_co2_absorbed": 440000.0,
      ...
    }
  ]
}
```

### Get CO₂ Calculation Details
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/plantations/1/co2_calculation/
```

Response:
```json
{
  "plantation_id": 1,
  "plantation_name": "Paulownia Forest 1",
  "age_years": 2.0,
  "total_hectares": 10.0,
  "yearly_co2_absorbed_kg": 440000.0,
  "formula_breakdown": {
    "age_years": 2.0,
    "species_factor": 22,
    "trees_per_hectare": 1000,
    "scale_factor": 1.0,
    "calculation": "2.00 × 22 × 10.00 × 1000 × 1.0"
  },
  "note": "Species factor and rates are PLACEHOLDERS - replace with real biomass data"
}
```

### Assign Hectare to Building
```bash
curl -X POST http://localhost:8000/api/plantations/1/assign_hectare/1/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

## Certificates

### List Certificates
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/certificates/
```

### Create Certificate
```bash
curl -X POST http://localhost:8000/api/certificates/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "apartment": 1,
    "hectare_lot": 1
  }'
```

Response includes `co2_absorbed_kg`:
```json
{
  "id": 1,
  "apartment": 1,
  "hectare_lot": 1,
  "co2_absorbed_kg": "4400.00",
  "apartment_info": {
    "id": 1,
    "apartment_number": "101",
    "building_name": "Eco Tower",
    "size_sqm": 100.0,
    "owner_name": "Jane Smith"
  },
  ...
}
```

### Generate PDF Certificate
```bash
curl -X POST http://localhost:8000/api/certificates/1/generate_pdf/ \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

Response:
```json
{
  "message": "PDF generated successfully",
  "pdf_url": "https://storage.googleapis.com/greweco-certificates/certificates/cert_1_20240101_120000.pdf"
}
```

## Growth Data

### List Growth Data
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  http://localhost:8000/api/growth-data/
```

### Filter by Plantation
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" \
  "http://localhost:8000/api/growth-data/?plantation=1"
```

### Create Growth Data
```bash
curl -X POST http://localhost:8000/api/growth-data/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "plantation": 1,
    "ndvi_value": 0.65,
    "co2_absorbed_kg": 440000.00,
    "notes": "Monthly growth update"
  }'
```

## Using Python requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(
    f"{BASE_URL}/auth/login/",
    json={
        "username": "developer1",
        "password": "securepassword123"
    }
)
tokens = response.json()["tokens"]
access_token = tokens["access"]

# Get buildings
headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(f"{BASE_URL}/buildings/", headers=headers)
buildings = response.json()["results"]
print(buildings)

# Create apartment
response = requests.post(
    f"{BASE_URL}/apartments/",
    headers=headers,
    json={
        "building": 1,
        "apartment_number": "102",
        "size_sqm": 120.00,
        "owner_name": "John Doe"
    }
)
apartment = response.json()
print(apartment)
```

## Using JavaScript fetch

```javascript
const BASE_URL = "http://localhost:8000/api";

// Login
const loginResponse = await fetch(`${BASE_URL}/auth/login/`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "developer1",
    password: "securepassword123"
  })
});

const { tokens } = await loginResponse.json();
const accessToken = tokens.access;

// Get plantations
const plantationsResponse = await fetch(`${BASE_URL}/plantations/`, {
  headers: { Authorization: `Bearer ${accessToken}` }
});

const { results } = await plantationsResponse.json();
console.log(results);
```

