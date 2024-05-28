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
**Success**

```json
{
    "username": "string"
}
```

**Failure**
[HTTP Response: 418](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418)

```json
{
    "error_message": "string"
}
```

### 1.3. View your profile - `/profile` (PATCH)

This endpoint allows a given user to edit their profile.

**Request**:

```json
{
    "public": "boolean" | "None"
    "about_me": "string"
}
```

**Response**:
**Success**

```json
{
    "message": "Account has been updated!"
}
```

**Failure**
HTTP Response 500 (Internal Server Error)

```json
{
    "error_message": "string" /* db issue with Profile or miscelleneous, however shouldn't happen as rollbacks / commits are in place during user creation process which creates their Profile */
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
    "new_post": "string"
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
    "post_id": "string",
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

### 2.6. View others profile - `/profile/{username}` (GET)

Retrieves profile of another user if they are following the user or their profile is public. Returns relevant information - username, user_id, date of account creation, top posts, etc.

**Request**:

Passed through url params.

```json
{}
```

**Response**:
**Success**

```json
{
    "Name": "string",
    "About Me": "string",
    "Account Created": "string",
    "Public": "boolean",
    "Username": "string",
    "ID": "number",
    "Followers": "number",
    "Following": "number",
    "Top Posts": "Post[]"
}
```

**Failure**
HTTP Response 500 (Internal Server Error)

```json
{
    "error_message": "string" /* because 'about me' couldn't be found for specified user */
}
```

HTTP Response 403 (Forbidden)

```json
{
    "error_message": "string" /* if the profile that they are trying to view is private and they aren't following the user, then they will recieve a 403 message */
}
```

### 2.7. React to a Post - '/posts/react/{post_id}' (POST)

Allows users to set how they feel about a post. Can change a like to a dislike or dislike to like. 

**Request**:

```json
{
    "post_id": "integer",
    "like": "boolean",
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
    "message": "string" /* Default value is "Invalid authentication credentials" */
}
```

HTTP Response 403

```json
{
    "message": "string" /* Default value is "Like/Dislike already exists." */
}
```

HTTP Response 404

```json
{
    "message": "string" /* Default value is "Post not found." */
}
```

### 2.8. View Following Page - '/posts/following' (GET)

Allows users to only see posts from users they follow.

**Request**:

```json
{
    "page": "integer"
}
```

**Response**:

Success

```json
{
    "prev": "integer",
    "next": "integer",
    "posts": []
}
```

Failure:

HTTP Response 401

```json
{
    "message": "string" /* Default value is "Invalid authentication credentials" */
}
```

## Regretful Actions

### 3.1. Delete a comment - `/post/[post_id]/comment/[comment_id]` (DELETE)

Allows a user to delete a comment they made on a post.

**Request**:

````json
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
````

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

````json
{
    "message": "string" /* Default value is "Incorrect password or username" */
}



HTTP Response 404
```json
{
    "message": "string" /* Default value is "Post id was not found" */
}
````

### 3.3. Delete a post - '/post/[post_id]' (DELETE)

**Request**:

```json
{
    "username": "string",
    "password": "string"
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
