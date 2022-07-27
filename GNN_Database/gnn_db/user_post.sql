create table user_post
(
    id      int not null
        primary key,
    user_id int not null,
    post_id int not null
);

create index account_post_ibfk_1
    on user_post (user_id);

create index account_post_ibfk_2
    on user_post (post_id);

