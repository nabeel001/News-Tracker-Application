create table if not exists users (
    id int not null generated always as identity (start with 1, increment by 1),
    email varchar(255) not null unique,
    username varchar(255) not null,
    password varchar(255) not null,
    PRIMARY KEY(id)
);