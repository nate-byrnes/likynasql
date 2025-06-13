create table command
(
    id integer primary key autoincrement,
    path varchar not null default './',
    executable varchar not null,
    static_args varchar,
    killaftersecs integer, -- if set, kill this command after so many seconds
    killaftertxt varchar, -- if set, watch output for the given text and kill once seen
    stdoutscraper varchar, -- if set, the modulename to use to scrape STDOUT
    stderrscraper varchar, -- if set, the modulename to use to scrape STDERR
    autorestarttimes integer, -- if set, the number of times to automatically restart the process, negative means always
    enabled boolean default 1, -- used to retain a command but not run it for a given execution
    priority integer not null, -- used to order the commands within a command sequence
    cmdseq_id integer, -- the command sequence this command is part of
    ssh boolean default NULL, -- execute over SSH, 0 - no, 1 - yes, NULL - defer to cmdseq
    ssh_as varchar, -- if SSHing, the user as which to log in, NULL will defer to cmdseq as needed
    ignore_nzretcode boolean default 0, -- COMPLETE vs ERR_QUIT when exit status is non-zero (allows pipeline to complete)
    continueaftersecs integer not null default -1, -- zero and positive values will leave job running, but continue pipeline
    foreign key (cmdseq_id) references cmdseq (id),
    unique (cmdseq_id, priority) -- ensure there are no sibling priorities in a cmdseq
);