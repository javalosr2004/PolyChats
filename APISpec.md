# API Specification for PolyChats

## 1. User Account Information

The API calls are made in this sequence when making a purchase:
1. `User Account Information`
2. `Influencer Actions`
3. `Regretful Actions`
4. `Normie Actions` (For normal people)

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
    "error_message": "string"
}
```

## 2. Influencer Actions

### 2.1. Create a post - `/post/` (POST)

Creates a new post given username and password.

**Request**:

```json
{
  "username": "string",
  "password": "string",
  "post": "string"
}
```

**Response**:
Success
```json
{
    "post_id": "string" /* This id will be used to modify any regretfully made posts, or if one wants to always appear right */
}
```
Failure
HTTP Reesponse 401
## Regretful Actions
