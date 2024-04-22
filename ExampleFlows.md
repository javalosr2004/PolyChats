## Timmy making an account Example flow

Timmy is a Computer Science student who is looking to make some friends and meet some new people. He recently heard of a new social media called poly chats. Timmy wants to make an account on PolyChats so he can make some new friends that also study Comptuer Sceince.
- To begin he must call POST /users/ and make a username and password
- Now that Timmy has an account on PolyChats, he can make a post that other users can see by calling POST /post/ and passing in "Hello world" to the request body.

Now that Timmy made an account and posted a message to other users, he can expand his friend group and meet new people.

## Ivan is an indecisive student that 

    Ivan creates a new user account by calling POST /user/ with his name, username, and password. Unfortanatey that username was taken and he spends an hour thinking of a new one.
    He creates a new post by calling POST /post/ with his username, password, and a lengthy post about his favorite programming language.
    Seconds later, Ivan changes his mind and decides to edit his post by calling PATCH /post/[post_id] with his username, password, and updated content. He does this 17 more times in the span of 5 minutes.
    Ivan notices a witty comment on his post and decides to follow the user by calling POST /user/[user_id]/follow. However, he immediately regrets his decision and unfollows the user by calling DELETE /user/[user_id]/unfollow.
    Finally, Ivan deletes his post altogether by calling DELETE /post/[post_id], only to create a new post moments later asking for opinions on his favorite programming language.

User Flow 2: Perfectionist Polly

    Polly creates a new user account by calling POST /user/ with her name, desired username, and password.
    She spends hours crafting the perfect post about her latest coding project, only to realize she made a typo in her username. Polly calls PATCH /user/change-username to update her username.
    Polly finally posts her masterpiece by calling POST /post/ with her new username, password, and post content.
    She obsessively refreshes the post page by calling GET /post/[post_id] every 30 seconds to check for likes and comments.
    Upon receiving a comment suggesting a minor improvement to her code, Polly hastily deletes her post by calling DELETE /post/[post_id] and retreats to her coding cave to refactor her entire project.
