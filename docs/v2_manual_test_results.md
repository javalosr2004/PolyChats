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
curl -X 'PATCH' \
  'http://13.52.181.106:3000/posts/update/24?new_post=not%20nice' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer jesus1'
```

**Response:**

```json

```

### 4. Following a User

Ivan notices a funny comment on his post and decides to follow the user by calling `POST /follow/[username]`.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/follow/jesus' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer jesus1' \
  -d ''
```

**Response:**

```json
{
    "message": "Followed Succesfully"
}
```

### 5. Unfollowing a User

Ivan immediately regrets his decision and unfollows the user by calling `DELETE /user/[user_id]/unfollow`.

**Curl Command:**

```bash
curl -X 'DELETE' \
  'http://13.52.181.106:3000/unfollow/jesus' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer jesus1'
```

**Response:**

```json
{
    "message": "Unfollowed Succesfully"
}
```

### 6. Deleting a Post

Finally, Ivan deletes his post after much time thinking, by calling `DELETE /post/[post_id]`.

**Curl Command:**

```bash
curl -X 'DELETE' \
  'http://13.52.181.106:3000/posts/delete/24' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer jesus1'
```

**Response:**

```json
{
    "message": "Post deleted successfully",
    "post_id": 24
}
```

### 7. Creating a New Post Again

Moments later, Ivan creates a new post asking for opinions on his favorite programming language.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/posts/create?post=I%20love%20testing%20apis.' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer jesus1' \
  -d ''
```

**Response:**

```json
{
    "post_id": 26
}
```

## Hopeless Romantic Holly

Holly made an account on Poly Chats after struggling to find the one. She knows there is someone out there for her and she believes they are on Poly Chats. She wants to make a post to help her find a boyfriend.

-   She starts by making a new post with some info about herself by calling POST /post/ with her username and password.
-   After some time, she views her post by calling GET /post/[post_id] with her post id and sees that she recieved a comment.
-   Then she continues having a conversation with this user by calling POST /post/[post_id]/comment to respond to them.
-   After talking, she follows this user by calling POST /user/[user_id]/follow.

1. Make a new post by calling POST /post/create with her post contents.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/posts/create?post=Hello%20everyone%21%20I%27m%20Holly%20and%20I%20am%20looking%20for%20the%20one.' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer hoe_lee' \
  -d ''
```

**Response:**

```json
{
    "post_id": 25
}
```

2. She views her post by calling GET /post/[post_id] with her post id.

**Curl Command:**

```bash
curl -X 'GET' \
  'http://13.52.181.106:3000/posts/25' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer hoe_lee'
```

**Response:**

```json
{
    "post_id": 25,
    "date": "2024-05-14T04:21:07.731504+00:00",
    "user_id": 8,
    "post": "Hello everyone! I'm Holly and I am looking for the one.",
    "likes": 0,
    "dislikes": 0
}
```

3. She continues having a conversation with this user by calling POST /comment/create to respond to them.

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/comments/create?post_id=25&content=Hello%21' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer hoe_lee' \
  -d ''
```

**Response:**

```json
{
    "message": "Comment added successfully",
    "comment_id": 10
}
```

4. She follows this user by calling POST /follow/[username]

**Curl Command:**

```bash
curl -X 'POST' \
  'http://13.52.181.106:3000/follow/aidan' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer hoe_lee' \
  -d ''
```

**Response:**

```json
{
    "message": "Followed Succesfully"
}
```

3. ## Perfectionist Polly

-   Polly creates a new user account by calling POST /user/ with her name, desired username, and password.
-   She spends hours crafting the perfect post about her latest coding project, only to realize she made a typo in her username. Polly calls PATCH /user/change-username to update her username.
-   Polly finally posts her masterpiece by calling POST /post/ with her new username, password, and post content.
-   She obsessively refreshes the post page by calling GET /post/[post_id] every 30 seconds to check for likes and comments.
-   Upon receiving a comment suggesting a minor improvement to her code, Polly hastily deletes her post by calling DELETE /post/[post_id] and retreats to her coding cave to refactor her entire project.

# Testing results

1. Creating an account

**Curl Command:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/auth/users/create?first_name=Polly&last_name=P&username=polly_cool_person&password=pass' \
  -H 'accept: application/json' \
  -d ''
```

**Response:**

```json
{ "Account created succesfully!" }
```

2. Patch Username

**Curl Command:**

```bash
curl -X 'PATCH' \
  'http://127.0.0.1:8000/auth/users/username?new_username=polly_cool' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer polly_cool_person'
```

**Response:**

```json
{ "message": "Username update succesfully" }
```

3. Create a new post

**Curl Command:**

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/posts/create?post=This%20my%20masterful%20post' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer polly_cool' \
  -d ''
```

**Response:**

```json
{ "post_id": 22 }
```

4. View her post

**Curl Command:**

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/posts/22' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer polly_cool'
```

**Response:**

```json
{
    "post_id": 22,
    "date": "2024-05-14T03:17:21.790557+00:00",
    "user_id": 7,
    "post": "This my masterful post",
    "likes": 0,
    "dislikes": 0
}
```

4. Delete her post

**Curl Command:**

```bash
curl -X 'DELETE' \
  'http://127.0.0.1:8000/posts/delete/22' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer polly_cool'
```

**Response:**

```json
{
    "message": "Post deleted successfully",
    "post_id": 22
}
```
