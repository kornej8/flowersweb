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

CREATE OR REPLACE VIEW flowers_core.flowers_thirst
AS WITH _last_watering AS (
         SELECT flowers_watering.id,
            flowers_watering.watering_date,
            flowers_watering.prev_watering_date,
            flowers_watering.dt,
            max(flowers_watering.dt) OVER (PARTITION BY flowers_watering.id) AS max_dt
           FROM flowers_core.flowers_watering
        ), last_watering AS (
         SELECT _last_watering.id,
            _last_watering.watering_date,
            _last_watering.prev_watering_date,
            _last_watering.dt
           FROM _last_watering
          WHERE _last_watering.dt = _last_watering.max_dt
        )
 SELECT t.id,
    t.flower_name,
    t.watering_date,
    t.watering_rate,
    t.days_range
   FROM ( SELECT f.id,
            f.flower_name,
            last_watering.watering_date,
            "substring"(f.watering_rate::text, '\d+'::text)::integer AS watering_rate,
            EXTRACT(day FROM CURRENT_TIMESTAMP - last_watering.dt::timestamp with time zone) AS days_range
           FROM flowers_core.flowers f
             LEFT JOIN last_watering USING (id)) t
  WHERE t.days_range >= t.watering_rate::numeric;