# API Specification for Potion Exchange Compatible Shops

## 1. Customer Purchasing

The API calls are made in this sequence when making a purchase:
1. `Get Catalog`
2. `Customer Visits`
3. `New Cart`
4. `Add Item to Cart` (Can be called multiple times)
5. `Checkout Cart`
6. `Search Orders`

### 1.1. Get Catalog - `/catalog/` (GET)

Retrieves the catalog of items. Each unique item combination should have only a single price. You can have at most 6 potion SKUs offered in your catalog at one time.

**Response**:

```json
[
    {
        "sku": "string", /* Matching regex ^[a-zA-Z0-9_]{1,20}$ */
        "name": "string",
        "quantity": "integer", /* Between 1 and 10000 */
        "price": "integer", /* Between 1 and 500 */
        "potion_type": [r, g, b, d] /* r, g, b, d are integers that add up to exactly 100 */
    }
]
```

### 1.2. Visits - `/carts/visits/{visit_id}` (POST)

Shares the customers that visited the store on that tick. Not all
customers end up purchasing because they may not like what they see
in the current catalog.

**Request**:

```json
[
  {
    "customer_name": "string",
    "character_class": "string",
    "level": "number"
  },
  {
    ...
  }
]
```
**Response**:

```json
{
    "success": "boolean"
}
```

### 1.3. New Cart - `/carts/` (POST)

Creates a new cart for a specific customer.

**Request**:

```json
{
  "customer_name": "string",
  "character_class": "string",
  "level": "number"
}
```

**Response**:

```json
{
    "cart_id": "string" /* This id will be used for future calls to add items and checkout */
}
``` 
