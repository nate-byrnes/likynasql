create table metric
(
    id INTEGER primary key autoincrement,
    name varchar not null,
    value numeric(15,5), -- null is allowed as a failed sensing attempt should be known
    last_updated timestamp not null default CURRENT_TIMESTAMP,
    last_updated_unix integer not null default (cast(strftime('%s', CURRENT_TIMESTAMP) as INTEGER )),
    unique (name)
);

create index metric_name_idx on metric(name);

CREATE TRIGGER trig_metric_upd 
AFTER UPDATE OF name, value ON metric 
FOR EACH ROW 
BEGIN
    UPDATE METRIC 
    SET last_updated_unix = cast(strftime('%s', CURRENT_TIMESTAMP) as INTEGER )
    WHERE ID = NEW.ID; 
END;
