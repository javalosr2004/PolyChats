# API Specification for PolyChats

## 1. User Account Information

The API calls are made in this sequence when making a purchase:
1. `User Account Information`
2. `Normie Actions`
3. `Regretful Actions`

### 1.1. Create user - `/user/` (POST)

Creates a user, given a unique username and password. On success returns the username.

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

### 1.2. Change username - `/user/change-username` (PATCH)

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

**Request**:
```json
{
    "username": "string",
    "password": "string",
    "new_post" "string"
}
```
**Response**:
Success
```json
{
    "message": "string"
}
```
Failure: 

HTTP Response 401
```json
{
    "message": "string" /* Default value is "Incorrect password or username" */
```

HTTP Response 404
```json
{
    "message": "string" /* Default value is "Post id was not found" */
```
### 2.3. View a post - '/post/[post_id]' (GET)

Views a post that already exists along with the comments, likes, and dislikes.
**Request**:

Success
```json
{
    "post_id": "string" ,
    "username": "string",
    "post": "string",
    "comments": "list",
    "likes": "integer",
    "dislikes": "integer"
}
```

**Response**:
Success
```json
{
    "message": "string" /* Default value is "OK" */
```

Failure: 

HTTP Response 404
```json
{
    "error_message": "string" /* Default value is "Post id was not found" */
```

### 2.4. Create a comment - '/post/[post_id]/comment' (POST)

Creates a comment for the current user "signed in".

**Request**:
```json
{
    "username": "string",
    "password": "string",
    "comment": "string"
}
```

**Response**:

Success
```json
{
    "message": "string"
}
```

Failure: 

HTTP Response 401
```json
{
    "message": "string" /* Default value is "Incorrect password or username" */
}

```

HTTP Response 404
```json
{
    "message": "string" /* Default value is "Post id was not found" */
}
```

### 2.5. Follow a user - '/user/[user_id]/follow' (POST)

**Request**:
```json
{
    "username": "string",
    "password": "string",
    "follow_username": "string"
}
```
**Response**:

Success
```json
{
    "message": "string"
}
```

Failure: 

HTTP Response 401
```json
{
    "message": "string" /* Default value is "Incorrect password or username" */
}

```

HTTP Response 404
```json
{
    "message": "string" /* Default value is "Post id was not found" */
}
```

## Regretful Actions

### 3.1. Delete a comment - `/post/[post_id]/comment/[comment_id]` (DELETE)

Allows a user to delete a comment they made on a post.

**Request**:
```json
{
    "username": "string",
    "password": "string"
}

**Response**:

Success
```json
{
    "message": "string"
}
```

Failure: 

HTTP Response 401
```json
{
    "message": "string" /* Default value is "Incorrect password or username" */
```

HTTP Response 404
```json
{
    "message": "string" /* Default value is "Post id was not found" */
```

### 3.2. Unfollow a user - '/user/[user_id]/unfollow' (DELETE)

**Request**:
```json
{
    "username": "string",
    "password": "string",
    "unfollow_username": "string"
}
```
**Response**:

Success
```json
{
    "message": "string"
}
```

Failure: 

HTTP Response 401
```json
{
    "message": "string" /* Default value is "Incorrect password or username" */
}



HTTP Response 404
```json
{
    "message": "string" /* Default value is "Post id was not found" */
}
```

### 3.3. Delete a post - '/post/[post_id]' (DELETE)

**Request**:
```json
{
    "username": "string",
    "password": "string",
}
```
**Response**:

Success
```json
{
    "message": "string"
}
```

Failure: 

HTTP Response 401
```json
{
    "message": "string" /* Default value is "Incorrect password or username" */
}

```

HTTP Response 404
```json
{
    "message": "string" /* Default value is "Post id was not found" */
}


