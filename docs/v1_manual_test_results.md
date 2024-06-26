Timmy is a Computer Science student who is looking to make some friends and meet some new people. He recently heard of a new social media called poly chats. Timmy wants to make an account on PolyChats so he can make some new friends that also study Comptuer Sceince.

-   To begin he must call POST /users/ and make a username and password
-   Now that Timmy has an account on PolyChats, he can sign in with username and password.
-   After that he can make a post that other users can see by calling POST /post/ and passing in "Hello world" to the request body.

Now that Timmy made an account and posted a message to other users, he can expand his friend group and meet new people.

# Testing Results

1. Curl statment called for signing in. This endpoint is defined under /token - login

curl -X 'POST' \
 'http://127.0.0.1:8000/token' \
 -H 'accept: application/json' \
 -H 'Content-Type: application/x-www-form-urlencoded' \
 -d 'grant_type=&username=jesus&password=password&scope=&client_id=&client_secret='

2. The Reponse received from executing the curl above

{
"access_token": "jesus",
"token_type": "bearer"
}

---

# Ivan The Indecisive Flow

-   Ivan creates a new user account by calling POST /user/ with his name, username, and password. Unfortanately that username was taken and he spends an hour thinking of a new one.
-   He creates a new post by calling POST /post/ with his username, password, and a lengthy post about his favorite programming language.
-   Seconds later, Ivan changes his mind and decides to edit his post by calling PATCH /post/[post_id] with his username, password, and updated content. He does this 17 more times in the span of 5 minutes.
-   Ivan notices a funny comment on his post and decides to follow the user by calling POST /user/[user_id]/follow. However, he immediately regrets his decision and unfollows the user by calling DELETE /user/[user_id]/unfollow.
-   Finally, Ivan deletes his post after much time thinking, by calling DELETE /post/[post_id], only to create a new post moments later asking for opinions on his favorite programming language.

1. Creating an account. Endpoint defined as POST /user/create.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/auth/users/create?first_name=Jesus&last_name=Avalos&username=jesus&password=0password' \
  -H 'accept: application/json' \
  -d ''
```

1b. Response

```json
{
    "detail": "Username already taken. Choose another."
}
```

2. Creating a New Post
   Ivan creates a new post by calling `POST /posts/` with his username, password, and a lengthy post about his favorite programming language.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/posts/create?post=blah' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer jesus1' \
  -d ''
```

**Response:**

```json
{
    "post_id": 24
}
```

### 3. Editing the Post

Ivan changes his mind and decides to edit his post by calling `PATCH /post/update/[post_id]`.

**Curl Command:**

```bash

```

**Response:**

```json

```

### 4. Following a User

Ivan notices a funny comment on his post and decides to follow the user by calling `POST /follow/[username]`.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/user/67890/follow' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "ivan",
    "password": "securepassword123"
  }'
```

**Response:**

```json
{
    "message": "User followed successfully."
}
```

### 5. Unfollowing a User

Ivan immediately regrets his decision and unfollows the user by calling `DELETE /user/[user_id]/unfollow`.

**Curl Command:**

```bash
curl -X 'DELETE' \
  'http://13.52.181.106:3000/user/67890/unfollow' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "ivan",
    "password": "securepassword123"
  }'
```

**Response:**

```json
{
    "message": "User unfollowed successfully."
}
```

### 6. Deleting a Post

Finally, Ivan deletes his post after much time thinking, by calling `DELETE /post/[post_id]`.

**Curl Command:**

```bash
curl -X 'DELETE' \
  'http://13.52.181.106:3000/post/12345' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "ivan",
    "password": "securepassword123"
  }'
```

**Response:**

```json
{
    "message": "Post deleted successfully."
}
```

### 7. Creating a New Post Again

Moments later, Ivan creates a new post asking for opinions on his favorite programming language.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/post/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "ivan",
    "password": "securepassword123",
    "content": "What do you all think about Python vs. JavaScript?"
  }'
```

**Response:**

```json
{
    "post_id": "67890",
    "message": "Post created successfully."
}
```

These placeholders can be filled in with specific details as needed.
