# Performance Reuslts

## Posts
- `/posts/` View Posts: 1031.96 ms
- `/posts/` following View Following Page: 150.86 ms
- `/posts/{id}` View Post Id: 231.86 ms
- `/posts/create` Create Post: 11.50 ms
- `/posts/delete/{post_id}` Delete Post: 235.19 ms
- `/posts/update/{post_id}` Update Post: 13.12 ms
- /`posts/react/{post_id}` React To Post: 56.16 ms

## Auth
- `/auth/token` Login: 6.12 ms
- `/auth/users` Create Account: 20.42 ms
- `/auth/users/me` Read Users Me: 6.74 ms

## Comments
- `/comments/` Create Comment: 8.64 ms
- `/comments/comments/{comment_id}` Delete Comment: 11.52 ms

## Followers
- `/followers/{username}/follow` Follow User: 97.84 ms
- `/followers/{username}/unfollow` Unfollow User: 44.81 ms

## Profile
- `/profile/` Get My Profile: 119.081 ms
- `/profile/` Change Profile: 15.50 ms
- `/profile/{username}` Get Person Profile: 93.56 ms


# Performance Tuning
