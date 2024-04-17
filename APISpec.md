# API Specification for PolyChats

## 1. User Account Information

The API calls are made in this sequence when making a purchase:
1. `Get Catalog`
2. `Customer Visits`
3. `New Cart`
4. `Add Item to Cart` (Can be called multiple times)
5. `Checkout Cart`
6. `Search Orders`

### 1.1. Create user - `/user/` (POST)

Creates a user, given a unique username and password. On success returns the username.
Retrieves the catalog of items. Each unique item combination should have only a single price. You can have at most 6 potion SKUs offered in your catalog at one time.

**Request**:
```json
{
    "name": "string",
    "username": "string",
    "password": "string"
}
```

**Response**:

```json
{
    "username": "string"
}
```

### 1.2. Change username - `/user/change-password` (PATCH)

Changes the username of a given user, and returns new username or returns error if username has already been taken.

**Request**:

```json
{
    "old_username": "string",
    "new_username": "string",
    "password": "string"
}
```
**Response**:
__Success__
```json
{
    "username": "string"
}
```
__Failure__
[HTTP Response: 418](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418)
```json
{
    "error_message": "sting"
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
