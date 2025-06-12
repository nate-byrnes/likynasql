create table chip
(
    id INTEGER primary key autoincrement,
    carrier_id INTEGER not null,
    slot int not null,
    dna varchar,
    foreign key (carrier_id) references carrier(id)
);