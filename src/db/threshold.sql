create table threshold
(
    id integer primary key,
    level number not null,
    direction text not null default 'UNDER_OK',
    message text,
    check (direction in ('UNDER_OK', 'ABOVE_OK', 'EQUAL_OK', 'EQUAL_BAD')),
    foreign key (id) references metric(id)
);