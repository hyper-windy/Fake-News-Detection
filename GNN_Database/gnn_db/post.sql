create table post
(
    id       int        not null
        primary key,
    content  text       not null,
    is_truth tinyint(1) not null
);

