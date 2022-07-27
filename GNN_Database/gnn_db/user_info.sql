create table user_info
(
    id                    int        not null
        primary key,
    statuses_count        int        not null,
    followers_count       int        not null,
    friends_count         int        not null,
    favourites_count      int        not null,
    listed_count          int        not null,
    default_profile       tinyint(1) not null,
    default_profile_image tinyint(1) not null,
    protected             tinyint(1) not null,
    verified              tinyint(1) not null,
    updated               datetime   null,
    created_at            datetime   not null,
    name                  text       not null,
    screen_name           text       null,
    description           text       null,
    clone_or_not          tinyint(1) not null
);

