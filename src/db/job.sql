create table job
(
    id integer primary key autoincrement,
    batch_id integer not null,
    commandline varchar not null,
    pid integer,
    started_ts datetime not null default CURRENT_TIMESTAMP,
    completed_ts datetime,
    exit_status integer,
    foreign key (batch_id) references batch(id)
);

CREATE TRIGGER trig_job_upd 
AFTER UPDATE ON job 
FOR EACH ROW 
BEGIN
    DELETE FROM job
    WHERE completed_ts < (SELECT min(completed_ts)
                 FROM job
                 WHERE batch_id = NEW.batch_id
                 -- AND commandline = NEW.commandline
                 AND completed_ts IS NOT NULL
                 ORDER BY completed_ts DESC
                 LIMIT 10 * (select count(*) FROM carrier AS c WHERE c.batch_id = NEW.batch_id))
    AND batch_id = NEW.batch_id;
    --AND commandline = NEW.commandline;
    
END;

CREATE TRIGGER trig_job_ins
AFTER INSERT ON job 
FOR EACH ROW 
BEGIN
    DELETE FROM job
    WHERE started_ts < (SELECT min(started_ts)
                 FROM job
                 WHERE batch_id = NEW.batch_id
                 -- AND commandline = NEW.commandline
                 AND completed_ts IS NULL
                 ORDER BY started_ts DESC
                 LIMIT 10 * (select count(*) FROM carrier AS c WHERE c.batch_id = NEW.batch_id))
    AND batch_id = NEW.batch_id;
    --AND commandline = NEW.commandline;
    
END;