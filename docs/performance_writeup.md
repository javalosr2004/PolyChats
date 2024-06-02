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

## Slowest Endpoints
These were are three slowest endpoints prior to performance tuning
- `/posts/` View Posts: 1031.96 ms
- `/posts/delete/{post_id}` Delete Post: 235.19 ms
- `/posts/{id}` View Post Id: 231.86 ms

### `/posts/{id}` View Post Id

Running Explain on this query resulted in

| QUERY PLAN                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GroupAggregate  (cost=3016.77..54296.80 rows=1 width=197) (actual time=83.630..83.693 rows=1 loops=1)                                                                 |
|   Group Key: p.post_id                                                                                                                                                |
|   ->  Nested Loop Left Join  (cost=3016.77..54296.75 rows=4 width=190) (actual time=16.964..83.627 rows=63 loops=1)                                                   |
|         Join Filter: (r.post_id = p.post_id)                                                                                                                          |
|         ->  Nested Loop Left Join  (cost=2016.77..45320.92 rows=1 width=181) (actual time=16.867..24.181 rows=7 loops=1)                                              |
|               Join Filter: (c.post_id = p.post_id)                                                                                                                    |
|               ->  Nested Loop Left Join  (cost=1016.77..6113.36 rows=1 width=173) (actual time=16.596..18.572 rows=1 loops=1)                                         |
|                     Join Filter: (f1.user_id = p.user_id)                                                                                                             |
|                     Rows Removed by Join Filter: 4                                                                                                                    |
|                     Filter: (pr.public OR ((NOT pr.public) AND (u.username = 'your_test_user'::text)))                                                                |
|                     ->  Hash Join  (cost=8.45..814.07 rows=1 width=174) (actual time=0.088..2.027 rows=1 loops=1)                                                     |
|                           Hash Cond: (pr.owner_id = p.user_id)                                                                                                        |
|                           ->  Seq Scan on "Profile" pr  (cost=0.00..764.01 rows=15848 width=9) (actual time=0.016..1.326 rows=20005 loops=1)                          |
|                                 Filter: (public OR (NOT public))                                                                                                      |
|                           ->  Hash  (cost=8.44..8.44 rows=1 width=173) (actual time=0.043..0.043 rows=1 loops=1)                                                      |
|                                 Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                          |
|                                 ->  Index Scan using post_pkey on "Posts" p  (cost=0.42..8.44 rows=1 width=173) (actual time=0.037..0.038 rows=1 loops=1)             |
|                                       Index Cond: (post_id = 1)                                                                                                       |
|                     ->  Gather  (cost=1008.32..5299.07 rows=15 width=19) (actual time=16.408..16.541 rows=4 loops=1)                                                  |
|                           Workers Planned: 1                                                                                                                          |
|                           Workers Launched: 1                                                                                                                         |
|                           ->  Hash Join  (cost=8.32..4297.57 rows=9 width=19) (actual time=13.703..13.705 rows=2 loops=2)                                             |
|                                 Hash Cond: (f1.follower_id = u.id)                                                                                                    |
|                                 ->  Parallel Seq Scan on "Followers" f1  (cost=0.00..3841.05 rows=170705 width=12) (actual time=0.005..6.163 rows=145101 loops=2)     |
|                                 ->  Hash  (cost=8.30..8.30 rows=1 width=19) (actual time=0.023..0.023 rows=1 loops=2)                                                 |
|                                       Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                    |
|                                       ->  Index Scan using user_username_key on "User" u  (cost=0.29..8.30 rows=1 width=19) (actual time=0.019..0.020 rows=1 loops=2) |
|                                             Index Cond: (username = 'noahgiboney'::text)                                                                              |
|               ->  Gather  (cost=1000.00..39207.51 rows=3 width=16) (actual time=0.269..5.602 rows=7 loops=1)                                                          |
|                     Workers Planned: 2                                                                                                                                |
|                     Workers Launched: 2                                                                                                                               |
|                     ->  Parallel Seq Scan on "Comments" c  (cost=0.00..38207.21 rows=1 width=16) (actual time=0.244..14.541 rows=2 loops=3)                           |
|                           Filter: (post_id = 1)                                                                                                                       |
|                           Rows Removed by Filter: 133139                                                                                                              |
|         ->  Gather  (cost=1000.00..8975.78 rows=5 width=17) (actual time=0.527..8.489 rows=9 loops=7)                                                                 |
|               Workers Planned: 2                                                                                                                                      |
|               Workers Launched: 2                                                                                                                                     |
|               ->  Parallel Seq Scan on "Reactions" r  (cost=0.00..7975.28 rows=2 width=17) (actual time=1.734..6.723 rows=3 loops=20)                                 |
|                     Filter: (post_id = 1)                                                                                                                             |
|                     Rows Removed by Filter: 206118                                                                                                                    |
| Planning Time: 1.447 ms                                                                                                                                               |
| Execution Time: 83.836 ms                                                                                                                                             |

Looking into this explian, somethings that I got from it were the group aggregation, that groups counts of comments, likes, and dislikes. There is also a nested loop left join is slowing this query down. There is a sequential scan that scans all the rows in the table, which also is slowing down the query. There is an index scan from the exsisting primary key. From this its clear we need to add more indexes to speed up the query.

Now creating these indexes
- CREATE INDEX idx_comments_post_id ON "Comments" (post_id);
- CREATE INDEX idx_reactions_post_id ON "Reactions" (post_id);
- CREATE INDEX idx_profile_owner_id_public ON "Profile" (owner_id, public);
- CREATE INDEX idx_followers_user_id_follower_id ON "Followers" (user_id, follower_id);
- CREATE INDEX idx_user_username ON "User" (username);

Resulted in this expalin query
| QUERY PLAN                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GroupAggregate  (cost=2.27..64.02 rows=1 width=197) (actual time=0.708..0.710 rows=1 loops=1)                                                                     |
|   Group Key: p.post_id                                                                                                                                            |
|   ->  Nested Loop Left Join  (cost=2.27..63.97 rows=4 width=190) (actual time=0.256..0.630 rows=63 loops=1)                                                       |
|         Join Filter: (r.post_id = p.post_id)                                                                                                                      |
|         ->  Nested Loop  (cost=1.84..46.50 rows=1 width=181) (actual time=0.215..0.401 rows=7 loops=1)                                                            |
|               Join Filter: (pr.public OR ((NOT pr.public) AND (u.username = 'your_test_user'::text)))                                                             |
|               ->  Nested Loop Left Join  (cost=1.55..38.18 rows=1 width=192) (actual time=0.199..0.366 rows=7 loops=1)                                            |
|                     Join Filter: (c.post_id = p.post_id)                                                                                                          |
|                     ->  Nested Loop Left Join  (cost=1.13..25.21 rows=1 width=184) (actual time=0.085..0.086 rows=1 loops=1)                                      |
|                           ->  Index Scan using post_pkey on "Posts" p  (cost=0.42..8.44 rows=1 width=173) (actual time=0.069..0.070 rows=1 loops=1)               |
|                                 Index Cond: (post_id = 1)                                                                                                         |
|                           ->  Nested Loop  (cost=0.71..16.76 rows=1 width=19) (actual time=0.012..0.012 rows=0 loops=1)                                           |
|                                 ->  Index Scan using idx_user_username on "User" u  (cost=0.29..8.30 rows=1 width=19) (actual time=0.011..0.012 rows=0 loops=1)   |
|                                       Index Cond: (username = 'noahgibony'::text)                                                                                 |
|                                 ->  Index Only Scan using idx_followers_user_id_follower_id on "Followers" f1  (cost=0.42..8.44 rows=1 width=12) (never executed) |
|                                       Index Cond: ((user_id = p.user_id) AND (follower_id = u.id))                                                                |
|                                       Heap Fetches: 0                                                                                                             |
|                     ->  Index Scan using idx_comments_post_id on "Comments" c  (cost=0.42..12.94 rows=3 width=16) (actual time=0.112..0.275 rows=7 loops=1)       |
|                           Index Cond: (post_id = 1)                                                                                                               |
|               ->  Index Only Scan using idx_profile_owner_id_public on "Profile" pr  (cost=0.29..8.30 rows=1 width=9) (actual time=0.004..0.004 rows=1 loops=7)   |
|                     Index Cond: (owner_id = p.user_id)                                                                                                            |
|                     Filter: (public OR (NOT public))                                                                                                              |
|                     Heap Fetches: 7                                                                                                                               |
|         ->  Index Scan using idx_reactions_post_id on "Reactions" r  (cost=0.42..17.41 rows=5 width=17) (actual time=0.007..0.030 rows=9 loops=7)                 |
|               Index Cond: (post_id = 1)                                                                                                                           |
| Planning Time: 2.206 ms                                                                                                                                           |
| Execution Time: 0.905 ms                                                                                                                                          |

This resulted in a faster time to view posts, which keeps users happpy. These results align with out expections, because adding these indexes greatly will increase lookup time as the query does not have to scan the full tables to search for values. The endpoint execution went from 231.86 ms to 5.62 ms