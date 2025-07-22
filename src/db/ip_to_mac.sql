create table ip_to_mac
(
    id integer primary key autoincrement,
    ipaddr VARCHAR NOT NULL,
    mac_addr VARCHAR NOT NULL,
    last_discovered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ipaddr, mac_addr)
);
