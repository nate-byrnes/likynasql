create table batch
(
    id integer primary key autoincrement,
    name varchar not null,
    enabled boolean not null default 1,
    status varchar not null default 'STOPPED',
    cmdseq_id integer,
    foreign key (cmdseq_id) references cmdseq (id)
);