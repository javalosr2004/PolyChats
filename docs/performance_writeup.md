# Performance Reuslts

## Posts
- `/posts/` View Posts: 1.0319581031799316 ms
- `/posts/following` View Following Page: 0.15085577964782715 ms
- `/posts/{id}` View Post Id: 0.23186302185058594 ms
- `/posts/create` Create Post: 0.011504173278808594 ms
- `/posts/delete/{post_id}` Delete Post: 0.23519492149353027 ms
- `/posts/update/{post_id}` Update Post: 0.013124227523803711 ms
- `/posts/react/{post_id}` React To Post: 0.056157827377319336 ms

## Auth
- `/auth/token` Login: 0.006117105484008789 ms
- `/auth/users` Create Account: 0.02041912078857422 ms
- `/auth/users/me` Read Users Me: 0.006742715835571289 ms

## Comments
- `/comments/` Create Comment: 0.008640050888061523 ms
- `/comments/comments/{comment_id}` Delete Comment: 0.01151585578918457 ms

## Followers
- `/followers/{username}/follow` Follow User: 0.0978400707244873 ms
- `/followers/{username}/unfollow` Unfollow User: 0.04481315612792969 ms

## Profile
- `/profile/` Get My Profile: 0.11908102035522461 ms
- `/profile/` Change Profile: 0.015496015548706055 ms
- `/profile/{username}` Get Person Profile: 0.09356212615966797 ms


# Performance Tuning
