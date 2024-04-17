# API Specification for PolyChats

## 1. User Account Information

The API calls are made in this sequence when making a purchase:
1. `User Account Information`
2. `Normie Actions`
3. `Regretful Actions`

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

## 2. Normie Actions

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
Failure: HTTP Response 401
```json
{
    "error_message": "string" /* Default value is "Incorrect password use the one below" */
    "password": "string"
```

### 2.2. Edit a post - '/post/[post_id]' (PATCH)

Edits a post that already exists, given that the owner is editing it.

Success
```json
{
    "post_id": "string" /*,
    "username": "string",
    "password": "string",
    "new_post" "string"
}
```
Failure: 

HTTP Response 401
```json
{
    "error_message": "string" /* Default value is "Incorrect password or username" */
```

HTTP Response 404
```json
{
    "error_message": "string" /* Default value is "Post id was not found" */
```


## Regretful Actions

