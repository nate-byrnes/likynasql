create table selector
(
    id integer primary key autoincrement,
    name varchar not null,
    matchattr varchar, -- the attribute in the data to apply matchstr against
    matchstr varchar -- regex or similar to be used to apply the selector
);