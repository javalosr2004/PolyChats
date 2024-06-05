# Fake Data Modeling
[faker/populate_posts.py](https://github.com/javalosr2004/PolyChats/blob/6777061cf8ab47e37b334a584a4a9b9ad29bc414/faker/populate_posts.py)
## Basic Setup

In order to run the fake data, you must create a venv environment within the `faker` folder.
After this is done you must install using pip install -r requirements.txt.

## Reasoning For ~1.6 Million Records

This data is a valid representation of how a social media site would look like distribution wise.
There are 20k followers, 20k profiles, ~300k followers, ~300k posts, ~400k comments, ~600k reactions (likes / dislikes).
In social media not everyone will be creating posts, and this is taken into account, as there where will be "whales" (creators) that will post more often / make up the majority of post count.
Likewise there are people that will simply only view posts (comment / react) rather than creating their own posts, this will compose the majority of the visitors on the social media, as it requires much less work than creating something.
In a similar fashion, reacting to a post is often easier than commenting which is why it accounts for the most records in the fake data.

# Performance Results

## Posts
- `/posts/` View Posts: 2205.89 ms
- `/posts/` following View Following Page: 150.86 ms
- `/posts/{id}` View Post Id: 231.86 ms
- `/posts/create` Create Post: 11.50 ms
- `/posts/delete/{post_id}` Delete Post: 499.69 ms
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
These were the three slowest endpoints prior to performance tuning
- `/posts/` View Posts: 2205.89
- `/posts/delete/{post_id}` Delete Post: 499.69 ms
- `/posts/{id}` View Post Id: 231.86 ms

### `/posts/{id}` View Post Id

Running explain on this query resulted in

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

Looking into this explain, somethings that I got from it were the group aggregation, that groups counts of comments, likes, and dislikes. There is also a nested loop left join is slowing this query down. There is a sequential scan that scans all the rows in the table, which also is slowing down the query. There is an index scan from the exsisting primary key. From this it is clear we need to add more indexes to speed up the query.

Now creating these indexes
- CREATE INDEX idx_comments_post_id ON "Comments" (post_id);
- CREATE INDEX idx_reactions_post_id ON "Reactions" (post_id);
- CREATE INDEX idx_profile_owner_id_public ON "Profile" (owner_id, public);
- CREATE INDEX idx_followers_user_id_follower_id ON "Followers" (user_id, follower_id);
- CREATE INDEX idx_user_username ON "User" (username);

Resulted in this explain query
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

This resulted in a faster time to view a post, which keeps users happy. These results align with our expections, because adding these indexes greatly will increase lookup time as the query does not have to scan the full tables to search for values. The endpoint execution went from 231.86 ms to 5.62 ms.

### `/posts/` View Posts: 2205.89 ms

Running explain on this query resulted in

| QUERY PLAN                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=203164.78..203164.81 rows=10 width=207) (actual time=2309.854..2335.368 rows=10 loops=1)                                                                                           |
|   ->  Sort  (cost=203164.76..204480.39 rows=526252 width=207) (actual time=2285.112..2310.626 rows=20 loops=1)                                                                                  |
|         Sort Key: p.date DESC                                                                                                                                                                   |
|         Sort Method: top-N heapsort  Memory: 37kB                                                                                                                                               |
|         ->  GroupAggregate  (cost=116029.99..189161.38 rows=526252 width=207) (actual time=1187.142..2266.874 rows=202693 loops=1)                                                              |
|               Group Key: p.post_id, u.username                                                                                                                                                  |
|               ->  Gather Merge  (cost=116029.99..177320.71 rows=526252 width=200) (actual time=1187.020..1623.993 rows=1339251 loops=1)                                                         |
|                     Workers Planned: 2                                                                                                                                                          |
|                     Workers Launched: 2                                                                                                                                                         |
|                     ->  Sort  (cost=115029.97..115578.15 rows=219272 width=200) (actual time=1158.117..1226.716 rows=446417 loops=3)                                                            |
|                           Sort Key: p.post_id, u.username                                                                                                                                       |
|                           Sort Method: external merge  Disk: 95960kB                                                                                                                            |
|                           Worker 0:  Sort Method: external merge  Disk: 98944kB                                                                                                                 |
|                           Worker 1:  Sort Method: external merge  Disk: 98632kB                                                                                                                 |
|                           ->  Parallel Hash Left Join  (cost=55667.41..74591.96 rows=219272 width=200) (actual time=335.814..559.052 rows=446417 loops=3)                                       |
|                                 Hash Cond: (p.post_id = c.post_id)                                                                                                                              |
|                                 ->  Parallel Hash Left Join  (cost=17551.41..34938.77 rows=166280 width=192) (actual time=217.434..312.906 rows=153698 loops=3)                                 |
|                                       Hash Cond: (p.post_id = r.post_id)                                                                                                                        |
|                                       ->  Parallel Hash Left Join  (cost=6034.19..16631.36 rows=84272 width=183) (actual time=37.440..110.174 rows=67564 loops=3)                               |
|                                             Hash Cond: (p.user_id = f1.user_id)                                                                                                                 |
|                                             Filter: (pr.public OR ((NOT pr.public) AND (u_1.username = 'jeffrey30'::text)))                                                                     |
|                                             Rows Removed by Filter: 28990                                                                                                                       |
|                                             ->  Hash Join  (cost=1654.82..11893.99 rows=95264 width=184) (actual time=18.084..76.493 rows=96554 loops=3)                                        |
|                                                   Hash Cond: (p.user_id = u.id)                                                                                                                 |
|                                                   ->  Parallel Seq Scan on "Posts" p  (cost=0.00..8833.93 rows=120693 width=173) (actual time=0.042..26.310 rows=96554 loops=3)                 |
|                                                   ->  Hash  (cost=1457.48..1457.48 rows=15787 width=27) (actual time=18.000..18.003 rows=20001 loops=3)                                         |
|                                                         Buckets: 32768 (originally 16384)  Batches: 1 (originally 1)  Memory Usage: 1493kB                                                      |
|                                                         ->  Hash Join  (cost=651.02..1457.48 rows=15787 width=27) (actual time=5.594..13.735 rows=20001 loops=3)                                |
|                                                               Hash Cond: (pr.owner_id = u.id)                                                                                                   |
|                                                               ->  Seq Scan on "Profile" pr  (cost=0.00..765.01 rows=15787 width=9) (actual time=0.038..3.713 rows=20001 loops=3)                |
|                                                                     Filter: (public OR (NOT public))                                                                                            |
|                                                               ->  Hash  (cost=401.01..401.01 rows=20001 width=18) (actual time=5.397..5.398 rows=20001 loops=3)                                 |
|                                                                     Buckets: 32768  Batches: 1  Memory Usage: 1317kB                                                                            |
|                                                                     ->  Seq Scan on "User" u  (cost=0.00..401.01 rows=20001 width=18) (actual time=0.007..2.388 rows=20001 loops=3)             |
|                                             ->  Parallel Hash  (cost=4379.26..4379.26 rows=9 width=18) (actual time=18.610..18.614 rows=0 loops=3)                                              |
|                                                   Buckets: 1024  Batches: 1  Memory Usage: 8kB                                                                                                  |
|                                                   ->  Hash Join  (cost=8.32..4379.26 rows=9 width=18) (actual time=18.525..18.526 rows=0 loops=3)                                               |
|                                                         Hash Cond: (f1.follower_id = u_1.id)                                                                                                    |
|                                                         ->  Parallel Seq Scan on "Followers" f1  (cost=0.00..3914.28 rows=173928 width=12) (actual time=0.008..7.821 rows=98559 loops=3)        |
|                                                         ->  Hash  (cost=8.30..8.30 rows=1 width=18) (actual time=0.041..0.042 rows=1 loops=3)                                                   |
|                                                               Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                      |
|                                                               ->  Index Scan using user_username_key on "User" u_1  (cost=0.29..8.30 rows=1 width=18) (actual time=0.038..0.039 rows=1 loops=3) |
|                                                                     Index Cond: (username = 'jeffrey30'::text)                                                                                  |
|                                       ->  Parallel Hash  (cost=7144.43..7144.43 rows=238143 width=17) (actual time=69.369..69.370 rows=190515 loops=3)                                          |
|                                             Buckets: 131072  Batches: 8  Memory Usage: 4992kB                                                                                                   |
|                                             ->  Parallel Seq Scan on "Reactions" r  (cost=0.00..7144.43 rows=238143 width=17) (actual time=0.041..29.565 rows=190515 loops=3)                   |
|                                 ->  Parallel Hash  (cost=36126.56..36126.56 rows=159156 width=16) (actual time=117.596..117.596 rows=127297 loops=3)                                            |
|                                       Buckets: 524288  Batches: 1  Memory Usage: 22080kB                                                                                                        |
|                                       ->  Parallel Seq Scan on "Comments" c  (cost=0.00..36126.56 rows=159156 width=16) (actual time=16.661..83.168 rows=127297 loops=3)                        |
| Planning Time: 3.118 ms                                                                                                                                                                         |
| JIT:                                                                                                                                                                                            |
|   Functions: 179                                                                                                                                                                                |
|   Options: Inlining false, Optimization false, Expressions true, Deforming true                                                                                                                 |
|   Timing: Generation 11.336 ms, Inlining 0.000 ms, Optimization 3.972 ms, Emission 69.236 ms, Total 84.544 ms                                                                                   |
| Execution Time: 2361.973 ms                                                                                                                                                                     |

I noticed that the query is not written in the most efficient way. It is currently joining all rows of posts with a bunch of tables and doing aggreation opperations on all the rows of post then filtering. I rewrote the query to first filter the rows that the user wants to view and then join and aggregate further. 

```sql
WITH filtered_posts AS (
  SELECT p.post_id, p.date, p.user_id, p.post
  FROM "Posts" p
  LEFT JOIN "Profile" pr ON p.user_id = pr.owner_id
  LEFT JOIN (
      SELECT *
      FROM "Followers" f1
      JOIN "User" u ON u.id = f1.follower_id
      WHERE username = :user
  ) f ON p.user_id = f.user_id 
  WHERE pr.public = TRUE OR ( pr.public = FALSE AND f.username = :user)
  ORDER BY date DESC
  OFFSET :offset
  LIMIT :limit
)
SELECT p.post_id, p.date, p.user_id, u.username, p.post,
    COUNT(DISTINCT c.id) AS comments,
    COUNT(DISTINCT CASE WHEN r.like = true THEN r.id ELSE NULL END) AS likes,
    COUNT(DISTINCT CASE WHEN r.like = false THEN r.id ELSE NULL END) AS dislikes
FROM filtered_posts p
LEFT JOIN "User" u ON p.user_id = u.id 
LEFT JOIN "Comments" c ON p.post_id = c.post_id 
LEFT JOIN "Reactions" r ON p.post_id = r.post_id 
GROUP BY p.post_id, p.date, p.user_id, u.username, p.post
ORDER BY date DESC;
```

Now running explain on this query resulted in

| QUERY PLAN                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GroupAggregate  (cost=73590.60..73595.67 rows=156 width=208) (actual time=531.031..531.268 rows=10 loops=1)                                                                                                       |
|   Group Key: p.date, p.post_id, p.user_id, u.username, p.post                                                                                                                                                     |
|   ->  Sort  (cost=73590.60..73590.99 rows=156 width=201) (actual time=530.968..531.181 rows=34 loops=1)                                                                                                           |
|         Sort Key: p.date DESC, p.post_id, p.user_id, u.username, p.post                                                                                                                                           |
|         Sort Method: quicksort  Memory: 34kB                                                                                                                                                                      |
|         ->  Hash Right Join  (cost=31889.61..73584.92 rows=156 width=201) (actual time=369.274..531.043 rows=34 loops=1)                                                                                          |
|               Hash Cond: (c.post_id = p.post_id)                                                                                                                                                                  |
|               ->  Seq Scan on "Comments" c  (cost=0.00..38352.99 rows=381799 width=16) (actual time=0.161..202.200 rows=381844 loops=1)                                                                           |
|               ->  Hash  (cost=31889.04..31889.04 rows=46 width=193) (actual time=283.240..283.449 rows=19 loops=1)                                                                                                |
|                     Buckets: 1024  Batches: 1  Memory Usage: 13kB                                                                                                                                                 |
|                     ->  Hash Right Join  (cost=19266.85..31889.04 rows=46 width=193) (actual time=209.969..283.366 rows=19 loops=1)                                                                               |
|                           Hash Cond: (r.post_id = p.post_id)                                                                                                                                                      |
|                           ->  Seq Scan on "Reactions" r  (cost=0.00..10478.44 rows=571544 width=17) (actual time=0.106..58.002 rows=571544 loops=1)                                                               |
|                           ->  Hash  (cost=19266.72..19266.72 rows=10 width=184) (actual time=158.064..158.272 rows=10 loops=1)                                                                                    |
|                                 Buckets: 1024  Batches: 1  Memory Usage: 11kB                                                                                                                                     |
|                                 ->  Nested Loop Left Join  (cost=19182.69..19266.72 rows=10 width=184) (actual time=157.971..158.262 rows=10 loops=1)                                                             |
|                                       ->  Limit  (cost=19182.40..19183.57 rows=10 width=174) (actual time=157.922..158.132 rows=10 loops=1)                                                                       |
|                                             ->  Gather Merge  (cost=19181.24..38845.61 rows=168540 width=174) (actual time=157.916..158.128 rows=20 loops=1)                                                      |
|                                                   Workers Planned: 2                                                                                                                                              |
|                                                   Workers Launched: 2                                                                                                                                             |
|                                                   ->  Sort  (cost=18181.21..18391.89 rows=84270 width=174) (actual time=151.295..151.303 rows=16 loops=3)                                                         |
|                                                         Sort Key: p.date DESC                                                                                                                                     |
|                                                         Sort Method: top-N heapsort  Memory: 33kB                                                                                                                 |
|                                                         Worker 0:  Sort Method: top-N heapsort  Memory: 35kB                                                                                                      |
|                                                         Worker 1:  Sort Method: top-N heapsort  Memory: 33kB                                                                                                      |
|                                                         ->  Parallel Hash Left Join  (cost=5341.72..15938.82 rows=84270 width=174) (actual time=33.577..134.703 rows=67562 loops=3)                               |
|                                                               Hash Cond: (p.user_id = f1.user_id)                                                                                                                 |
|                                                               Filter: (pr.public OR ((NOT pr.public) AND (u_1.username = 'jeffrey30'::text)))                                                                     |
|                                                               Rows Removed by Filter: 28990                                                                                                                       |
|                                                               ->  Hash Join  (cost=962.35..11201.45 rows=95262 width=175) (actual time=10.512..89.852 rows=96552 loops=3)                                         |
|                                                                     Hash Cond: (p.user_id = pr.owner_id)                                                                                                          |
|                                                                     ->  Parallel Seq Scan on "Posts" p  (cost=0.00..8833.90 rows=120690 width=174) (actual time=0.086..36.106 rows=96552 loops=3)                 |
|                                                                     ->  Hash  (cost=765.01..765.01 rows=15787 width=9) (actual time=10.326..10.327 rows=20001 loops=3)                                            |
|                                                                           Buckets: 32768 (originally 16384)  Batches: 1 (originally 1)  Memory Usage: 1057kB                                                      |
|                                                                           ->  Seq Scan on "Profile" pr  (cost=0.00..765.01 rows=15787 width=9) (actual time=0.031..5.951 rows=20001 loops=3)                      |
|                                                                                 Filter: (public OR (NOT public))                                                                                                  |
|                                                               ->  Parallel Hash  (cost=4379.26..4379.26 rows=9 width=18) (actual time=22.625..22.627 rows=0 loops=3)                                              |
|                                                                     Buckets: 1024  Batches: 1  Memory Usage: 8kB                                                                                                  |
|                                                                     ->  Hash Join  (cost=8.32..4379.26 rows=9 width=18) (actual time=22.518..22.520 rows=0 loops=3)                                               |
|                                                                           Hash Cond: (f1.follower_id = u_1.id)                                                                                                    |
|                                                                           ->  Parallel Seq Scan on "Followers" f1  (cost=0.00..3914.28 rows=173928 width=12) (actual time=0.009..11.612 rows=98559 loops=3)       |
|                                                                           ->  Hash  (cost=8.30..8.30 rows=1 width=18) (actual time=0.033..0.034 rows=1 loops=3)                                                   |
|                                                                                 Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                      |
|                                                                                 ->  Index Scan using user_username_key on "User" u_1  (cost=0.29..8.30 rows=1 width=18) (actual time=0.028..0.029 rows=1 loops=3) |
|                                                                                       Index Cond: (username = 'jeffrey30'::text)                                                                                  |
|                                       ->  Index Scan using user_pkey on "User" u  (cost=0.29..8.30 rows=1 width=18) (actual time=0.012..0.012 rows=1 loops=10)                                                    |
|                                             Index Cond: (id = p.user_id)                                                                                                                                          |
| Planning Time: 1.680 ms                                                                                                                                                                                           |
| Execution Time: 531.924 ms                                                                                                                                                                                        |

This made the execution time for this single query go from 2361.973 ms to 531.924 ms. However, there is still a sequential scan that scans all the rows in the comments, reactions, profile, posts, and followers table, which is slowing down the query. There is an index scan from the exsisting primary key of the posts table. From this it is clear we need to add more indexes to speed up the query.

Now creating these indexes
- CREATE INDEX idx_post_date ON "Posts" (date);
- CREATE INDEX idx_profile_owner_id_public ON "Profile" (owner_id, public);
- CREATE INDEX idx_followers_follower_id ON "Followers" (follower_id);
- CREATE INDEX idx_reactions_post_id ON "Reactions" (post_id);
- CREATE INDEX idx_comments_post_id ON "Comments" (post_id);

Resulted in this explain query

| QUERY PLAN                                                                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GroupAggregate  (cost=49.06..426.74 rows=156 width=208) (actual time=9.928..9.978 rows=10 loops=1)                                                                                                   |
|   Group Key: p.date, p.post_id, p.user_id, u.username, p.post                                                                                                                                        |
|   ->  Incremental Sort  (cost=49.06..422.06 rows=156 width=201) (actual time=9.717..9.726 rows=34 loops=1)                                                                                           |
|         Sort Key: p.date DESC, p.post_id, p.user_id, u.username, p.post                                                                                                                              |
|         Presorted Key: p.date                                                                                                                                                                        |
|         Full-sort Groups: 1  Sort Method: quicksort  Average Memory: 34kB  Peak Memory: 34kB                                                                                                         |
|         ->  Nested Loop Left Join  (cost=7.88..414.39 rows=156 width=201) (actual time=1.554..9.562 rows=34 loops=1)                                                                                 |
|               ->  Nested Loop Left Join  (cost=7.45..271.62 rows=46 width=193) (actual time=1.445..8.843 rows=19 loops=1)                                                                            |
|                     ->  Nested Loop Left Join  (cost=7.02..95.19 rows=10 width=184) (actual time=1.362..8.054 rows=10 loops=1)                                                                       |
|                           ->  Limit  (cost=6.73..12.04 rows=10 width=174) (actual time=1.250..3.974 rows=10 loops=1)                                                                                 |
|                                 ->  Nested Loop Left Join  (cost=1.43..107271.40 rows=202249 width=174) (actual time=0.510..3.967 rows=20 loops=1)                                                   |
|                                       Join Filter: (p.user_id = f1.user_id)                                                                                                                          |
|                                       Filter: (pr.public OR ((NOT pr.public) AND (u_1.username = 'jeffrey30'::text)))                                                                                |
|                                       Rows Removed by Filter: 5                                                                                                                                      |
|                                       ->  Nested Loop  (cost=0.72..47238.62 rows=228629 width=175) (actual time=0.279..3.702 rows=25 loops=1)                                                        |
|                                             ->  Index Scan Backward using idx_post_date on "Posts" p  (cost=0.42..38037.02 rows=289656 width=174) (actual time=0.181..0.516 rows=25 loops=1)         |
|                                             ->  Memoize  (cost=0.30..0.32 rows=1 width=9) (actual time=0.124..0.125 rows=1 loops=25)                                                                 |
|                                                   Cache Key: p.user_id                                                                                                                               |
|                                                   Cache Mode: logical                                                                                                                                |
|                                                   Hits: 4  Misses: 21  Evictions: 0  Overflows: 0  Memory Usage: 3kB                                                                                 |
|                                                   ->  Index Only Scan using idx_profile_owner_id_public on "Profile" pr  (cost=0.29..0.31 rows=1 width=9) (actual time=0.046..0.047 rows=1 loops=21) |
|                                                         Index Cond: (owner_id = p.user_id)                                                                                                           |
|                                                         Filter: (public OR (NOT public))                                                                                                             |
|                                                         Heap Fetches: 0                                                                                                                              |
|                                       ->  Materialize  (cost=0.71..17.71 rows=15 width=18) (actual time=0.009..0.009 rows=0 loops=25)                                                                |
|                                             ->  Nested Loop  (cost=0.71..17.63 rows=15 width=18) (actual time=0.219..0.220 rows=0 loops=1)                                                           |
|                                                   ->  Index Scan using user_username_key on "User" u_1  (cost=0.29..8.30 rows=1 width=18) (actual time=0.183..0.184 rows=1 loops=1)                  |
|                                                         Index Cond: (username = 'jeffrey30'::text)                                                                                                   |
|                                                   ->  Index Scan using idx_followers_follower_id on "Followers" f1  (cost=0.42..9.00 rows=33 width=12) (actual time=0.033..0.033 rows=0 loops=1)     |
|                                                         Index Cond: (follower_id = u_1.id)                                                                                                           |
|                           ->  Index Scan using user_pkey on "User" u  (cost=0.29..8.30 rows=1 width=18) (actual time=0.403..0.403 rows=1 loops=10)                                                   |
|                                 Index Cond: (id = p.user_id)                                                                                                                                         |
|                     ->  Index Scan using idx_reactions_post_id on "Reactions" r  (cost=0.42..17.59 rows=5 width=17) (actual time=0.067..0.073 rows=2 loops=10)                                       |
|                           Index Cond: (post_id = p.post_id)                                                                                                                                          |
|               ->  Memoize  (cost=0.43..13.04 rows=3 width=16) (actual time=0.034..0.036 rows=2 loops=19)                                                                                             |
|                     Cache Key: p.post_id                                                                                                                                                             |
|                     Cache Mode: logical                                                                                                                                                              |
|                     Hits: 9  Misses: 10  Evictions: 0  Overflows: 0  Memory Usage: 2kB                                                                                                               |
|                     ->  Index Scan using idx_comments_post_id on "Comments" c  (cost=0.42..13.03 rows=3 width=16) (actual time=0.060..0.062 rows=1 loops=10)                                         |
|                           Index Cond: (post_id = p.post_id)                                                                                                                                          |
| Planning Time: 12.038 ms                                                                                                                                                                             |
| Execution Time: 10.705 ms                                                                                                                                                                            |

This resulted in a faster time to view posts, which keeps users happy. These results align with out expections, because adding these indexes greatly will increase lookup time as the query does not have to scan the full tables to search for values. The endpoint execution went from 2205.89 ms to 52.72 ms.

### `/posts/delete/{post_id}` Delete Post: 499.69 ms

Running explain on the queries resulted in

| QUERY PLAN                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------- |
| Delete on "Comments"  (cost=0.00..39309.68 rows=0 width=0) (actual time=137.824..137.826 rows=0 loops=1)         |
|   ->  Seq Scan on "Comments"  (cost=0.00..39309.68 rows=3 width=6) (actual time=137.822..137.824 rows=0 loops=1) |
|         Filter: (post_id = 87)                                                                                   |
|         Rows Removed by Filter: 381880                                                                           |
| Planning Time: 0.200 ms                                                                                          |
| Execution Time: 137.931 ms                                                                                       |                                                                                     |                                                                                    |
| QUERY PLAN                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------- |
| Delete on "Posts"  (cost=0.42..8.44 rows=0 width=0) (actual time=0.896..0.896 rows=0 loops=1)                           |
|   ->  Index Scan using post_pkey on "Posts"  (cost=0.42..8.44 rows=1 width=6) (actual time=0.097..0.099 rows=1 loops=1) |
|         Index Cond: (post_id = 87)                                                                                      |
| Planning Time: 0.487 ms                                                                                                 |
| Trigger for constraint comment_post_id_fkey: time=0.821 calls=1                                                         |
| Execution Time: 1.935 ms                                                                                                |                                                                                            |                                                                                      |

Looking into this explain, there is a sequential scan that scans all the rows in the comments table, which is slowing down the query. There is already an index scan on the posts table because the primary key is post_id. We should add an index on the comments table with post_id.

Now creating this index
- CREATE INDEX idx_comments_post_id ON "Comments" (post_id);

Resulted in this explain query

| QUERY PLAN                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------- |
| Delete on "Comments"  (cost=0.42..13.00 rows=0 width=0) (actual time=4.689..4.691 rows=0 loops=1)                                      |
|   ->  Index Scan using idx_comments_post_id on "Comments"  (cost=0.42..13.00 rows=3 width=6) (actual time=0.676..4.443 rows=7 loops=1) |
|         Index Cond: (post_id = 54)                                                                                                     |
| Planning Time: 0.391 ms                                                                                                                |
| Execution Time: 4.808 ms                                                                                                               |
| QUERY PLAN                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------- |
| Delete on "Posts"  (cost=0.42..8.44 rows=0 width=0) (actual time=0.285..0.286 rows=0 loops=1)                           |
|   ->  Index Scan using post_pkey on "Posts"  (cost=0.42..8.44 rows=1 width=6) (actual time=0.078..0.079 rows=1 loops=1) |
|         Index Cond: (post_id = 54)                                                                                      |
| Planning Time: 0.397 ms                                                                                                 |
| Trigger for constraint comment_post_id_fkey: time=0.962 calls=1                                                         |
| Execution Time: 1.397 ms                                                                                                |                                                                                      |                                                                                              |

This resulted in a faster time to delete comments, which speeds up the whole delete_post endpoint. These results align with our expections, because adding these indexes greatly will increase lookup time as the query does not have to scan the full table to search for values to delete. The endpoint execution went from 499.69 ms to 50.94 ms.
