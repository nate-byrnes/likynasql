create table alert
(
    id integer primary key,
    sent datetime not null default CURRENT_TIMESTAMP
);