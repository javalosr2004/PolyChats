## Timmy making an account Example flow

Timmy is a Computer Science student who is looking to make some friends and meet some new people. He recently heard of a new social media called poly chats. Timmy wants to make an account on PolyChats so he can make some new friends that also study Comptuer Sceince.
- To begin he must call POST /users/ and make a username and password
- Now that Timmy has an account on PolyChats, he can sign in with username and password.
- After that he can make a post that other users can see by calling POST /post/ and passing in "Hello world" to the request body.

Now that Timmy made an account and posted a message to other users, he can expand his friend group and meet new people.

# Testing Results

1. Curl statment called for signing in. This endpoint is defined under /token - login

curl -X 'POST' \
  'http://127.0.0.1:8000/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=&username=noah&password=test&scope=&client_id=&client_secret='

2. The Reponse received from executing the curl above 

{
  "access_token": "noah",
  "token_type": "bearer"
}