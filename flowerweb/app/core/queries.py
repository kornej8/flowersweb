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

update_watering_rate = r"""
update flowers_core.flowers 
set watering_rate = :watering_rate
where id = :id
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
where dt = max_dt),
_last_fertilizer as (
select *, max(dt) over (partition by id) as max_dt from flowers_core.flowers_fertilizer
), last_fertilizer as (
select 
	id, 
	fertilizer_date, 
	fertilizer_name
	from _last_fertilizer
where dt = max_dt
)
select flower_name, flower_file, 
to_char(f.dt, 'dd.mm.yyyy') as dt,
coalesce(to_char(watering_date, 'dd.mm.yyyy'), '—') as watering_date, 
current_date - coalesce(watering_date, f.dt::date) as days_without_watering,
coalesce((watering_date - prev_watering_date)::varchar, '—') as days_between_previous_watering,
coalesce(to_char(fertilizer_date, 'dd.mm.yyyy'), '—') as fertilizer_date,
case when coalesce(fertilizer_name, '—') = '' then '—' else coalesce(fertilizer_name, '—') end as fertilizer_name
from flowers_core.flowers f
left join flowers_core.flower_pictures using (id)
left join last_watering using (id)
left join last_fertilizer using (id)
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

select_last_fertilizer = """
select id, fertilizer_date from (
select id, fertilizer_date,  dt, 
max(dt) over (partition by id) as max_dt
from flowers_core.flowers_fertilizer
where id in ({ids})) t
where dt = max_dt
"""

insert_watering = """
INSERT INTO flowers_core.flowers_watering
 (id, watering_date, prev_watering_date) 
 VALUES (:id, :watering_date, :prev_watering_date)
"""

insert_fertilizer = """
INSERT INTO flowers_core.flowers_fertilizer
 (id, fertilizer_date, prev_fertilizer_date, fertilizer_name) 
 VALUES (:id, :fertilizer_date, :prev_fertilizer_date, :fertilizer_name)
"""