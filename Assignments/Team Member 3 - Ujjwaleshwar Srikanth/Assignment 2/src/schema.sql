create table if not exists users (
    rollnumber int not null,
    email varchar(255),
    username varchar(255) not null,
    password varchar(255) not null,
    PRIMARY KEY (rollnumber)
);