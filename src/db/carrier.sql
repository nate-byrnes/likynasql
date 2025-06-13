create table carrier
(
    id INTEGER primary key autoincrement,
    mac_addr VARCHAR not null,
    ip_addr varchar not null,
    serno varchar not null,
    detected_ts text not null default CURRENT_TIMESTAMP,
    batch_id integer,
    foreign key (batch_id) references batch(id)
);

create index carrier_ipaddr_idx on carrier(ip_addr);
create index carrier_serno_idx on carrier(serno);