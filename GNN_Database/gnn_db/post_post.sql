create table post_post
(
    id        int     not null
        primary key,
    post_id_1 int     not null,
    post_id_2 int     not null,
    action    char(3) not null comment 'include 2 action: share(shr) and comment(cmt)',
    constraint post_post_ibfk_1
        foreign key (post_id_1) references post (id),
    constraint post_post_ibfk_2
        foreign key (post_id_2) references post (id)
);

