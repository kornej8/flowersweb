insert_new_picture = """
INSERT INTO flowers_core.flower_pictures
(flower_file_name, flower_file, id)
VALUES (:flower_file_name, :flower_file, :id)
"""

insert_new_flower = r"""
INSERT INTO flowers_core.flowers 
 (flower_name) 
 VALUES (:flower_name) returning id
"""

select_flowers = """
with _last_watering as (
select *, max(dt) over (partition by id) as max_dt from flowers_core.flowers_watering
), last_watering as (
select 
	id, 
	watering_date, 
	prev_watering_date
	from _last_watering
where dt = max_dt)
select flower_name, flower_file, 
to_char(f.dt, 'dd.mm.yyyy') as dt,
coalesce(to_char(watering_date, 'dd.mm.yyyy'), '—') as watering_date, 
current_date - coalesce(watering_date, f.dt::date) as days_without_watering,
coalesce((watering_date - prev_watering_date)::varchar, '—') as days_between_previous_watering
from flowers_core.flowers f
left join flowers_core.flower_pictures using (id)
left join last_watering using (id)
where flower_name ilike '%{_filter}%'
order by f.dt desc
"""

select_checkbox_flower = """
select id, flower_name, to_char(dt, 'dd.mm.yyyy') as dt from flowers_core.flowers
where flower_name is not null and flower_name <> ''
"""

select_last_watering = """
select id, watering_date from (
select id, watering_date,  dt, 
max(dt) over (partition by id) as max_dt
from flowers_core.flowers_watering
where id in ({ids})) t
where dt = max_dt
"""

insert_watering = """
INSERT INTO flowers_core.flowers_watering
 (id, watering_date, prev_watering_date) 
 VALUES (:id, :watering_date, :prev_watering_date)
"""