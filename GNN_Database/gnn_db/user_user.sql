create table user_user
(
    id           int        not null
        primary key,
    user_id_1    int        not null,
    user_id_2    int        not null,
    relationship varchar(6) not null comment '2 type: folow and friend'
);

create index user_id_1
    on user_user (user_id_1);

create index user_id_2
    on user_user (user_id_2);

