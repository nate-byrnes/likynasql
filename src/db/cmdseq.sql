create table cmdseq
(
    id integer primary key autoincrement,
    name varchar not null,
    overssh boolean not null default 0,
    ssh_as varchar,
    unique (name)
);