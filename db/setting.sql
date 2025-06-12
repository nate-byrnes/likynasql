create table setting
(
    id integer primary key autoincrement,
    name varchar not null,
    value varchar not null,
    selector_id integer, -- null here means default value
    priority integer,
    forattrn varchar,
    forattrv varchar,
    foreign key (selector_id) references selector(id)
);