create table macsn_to_ip
(
    id integer primary key autoincrement,
    mac_addr VARCHAR NOT NULL,
    serno VARCHAR NOT NULL,
    ipaddr VARCHAR NOT NULL,
    fwvers VARCHAR NOT NULL,
    fwstate VARCHAR NOT NULL,
    model VARCHAR NOT NULL,
    fwtype VARCHAR NOT NULL,
    btn VARCHAR NOT NULL,
    last_discovered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ignore BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (mac_addr)
);
