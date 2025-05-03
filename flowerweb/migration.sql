create schema if not exists flowers_core;

create table if not exists flowers_core.flowers (
	id serial,
	flower_name varchar,
	dt timestamp default current_timestamp
);

CREATE TABLE if not exists flowers_core.flower_pictures (
    id serial,
    flower_file_name text not null,
    flower_file bytea not null,
    dt timestamp default current_timestamp
);

alter table flowers_core.flower_pictures
add column flower_file_square bytea;


ALTER TABLE flowers_core.flowers ADD PRIMARY key (id);


alter table flowers_core.flower_pictures
drop column flower_file_square;

ALTER TABLE flowers_core.flower_pictures ADD CONSTRAINT fk_name FOREIGN KEY (id) REFERENCES flowers_core.flowers(id);


create table flowers_core.flowers_watering (
	id serial,
	watering_date date,
	prev_watering_date date,
	dt timestamp default current_timestamp
);

ALTER TABLE flowers_core.flowers_watering ADD CONSTRAINT fk_name FOREIGN KEY (id) REFERENCES flowers_core.flowers(id);
