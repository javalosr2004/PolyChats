# Basic Setup

In order to run the fake data, you must create a venv environment within the `faker` folder.
After this is done you must install using pip install -r requirements.txt.

# Reasoning For ~1.6 Million Records

This data is a valid representation of how a social media site would look like distribution wise.
There are 20k followers, 20k profiles, ~300k followers, ~300k posts, ~400k comments, ~600k reactions (likes / dislikes).
In social media not everyone will be creating posts, and this is taken into account, as there where will be "whales" (creators) that will post more often / make up the majority of post count.
Likewise there are people that will simply only view posts (comment / react) rather than creating their own posts, this will compose the majority of the visitors on the social media, as it requires much less work than creating something.
In a similar fashion, reacting to a post is often easier than commenting which is why it accounts for the most records in the fake data.
