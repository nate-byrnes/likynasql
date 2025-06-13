create table argument
(
    id integer primary key autoincrement,
    argstr varchar not null, -- the -[?] or --[words] aspect of the argument
    command_id integer not null,
    selector_id integer, -- the id of the selector+setting to resolve to populate the value aspect of this argument
    priority integer, -- used to sort the arguments for a command
    separator varchar not null default ' ',
    foreign key (command_id) references command(id)
);