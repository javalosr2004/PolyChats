# Code Review Comments Addressed

## Spruha Nayak

#### When entering the OAuth Login, it prompts other variables that don't seem relative to the project, would there be anyway to have these values be pre-populated(these values are specifically client_id, client_secret, and scope)? (creation.py)
For now these here for development purposes but will fix this later down the line.

#### You do not need to create new MetaData variables each time, rather you can reuse the variable for each table (models.py)
We made this change, this was something I did not know before.

#### For clarity I would change auth/token to auth/login
Token is better according to rest best practices

#### I would change POST /users/create to just a POST create
We made this change as this this follows better Rest API practices.

#### I would state the prefix for the followers page to be followers/ rather than nothing
We made this change as it makes more sense.

#### I would also change the endpoint name to {username}/follow this makes it a bit more clear
We made this change is it follows best Rest API practices.

#### I would do the same with {username}/unfollow
We made this change is it follows best Rest API practices.

#### Wouldn't it be better to raise the exception rather than return it?
Yes it would and we made this change as this a better style.

#### Change /create to just a POST to /
We made this change is it follows best Rest API practices.

#### Change /delete/comment_id to just DELETE /{comment_id}
We made this change as that follows best Rest API practices.

#### This is not really a necessary change but you can use logging instead of print statements just by adding this line, 'logging.basicConfig(level=logging.INFO)'
This is something we will consider down the line but it is good information to know.

#### These comments are extremely nitpicky I think you guys did a great job implementing this, although the functionality DB wise is a bit simple
Thank you.

#### Design wise I think you guys can use an extra endpoint under followers that logs all of your followers and another one for all of the people following you
Cool idea and this is somethign that will consider adding a future release of this 

#### When looking at all of the posts rather than just looking at the user-id I think you should return the username instead
For now we are gonna keep it was user-id for development purposes but will change to username down the line.

#### I also did see the pagination logic for the posts endpoint but I do think it could be further improved with limits and other parameters
We agree and will extend this in further version of the app.


## Carlos V
#### Make Docs folder and add all team files such as "user_stories.md" to make repo cleaner.
We added this, it does make our repo cleaner.

#### Add more comments to "Auth.py" to make it easier to understand how it works.
Did not deem as necessary, the developers understand this file. The repo is public and we dont want everyone understadning out auth proccess.

#### Add comments to "Creation.py", unsure how it works completely as it is separate from the other api files
Wrote a short class header comment expalining the purpose of the class

#### Remove commented-out code to make actual code more readable.
We did this even though it was only a few lines.

#### In "Auth.py" change /token to /login for simplicity
Did not deem as necessary.

#### In "Auth.py" change /users/create to /create for simplicity
Did not deem as necessary.

#### Maybe change /users/me to /profile just to understand what that function does.
We took this advise but changed it to '/myprofile'

#### Maybe change the naming /posts/create or /comments/create to new or something to differentiate them.

#### Implement a way to view the users on the site and get their user id in order to follow them.
This will possibly come in a future version.

#### Maybe change the wording of /posts to "You must be logged in to view".
Did not deem as necessary.

#### Implement a way to see who follows you if you are logged in.
This will possibly come in a future version.

#### Maybe add an "About" section to a user profile to view their info
This will possibly come in a future version.
