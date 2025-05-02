create schema if not exists flowers_core;

create table if not exists flowers_core.flowers (
	id serial,
	flower_name varchar,
	dt timestamp default current_timestamp
);


CREATE TABLE flowers_core.flower_pictures (
    id serial,
    flower_file_name text not null,
    flower_file bytea not null,
    dt timestamp default current_timestamp
);