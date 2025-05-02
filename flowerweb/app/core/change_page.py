from sqlalchemy import text
from datetime import datetime
from flowerweb.app.core.queries import (select_checkbox_flower,
                              select_last_watering,
                              insert_watering)


class _ShowPage:

    @classmethod
    def html(cls, row):
        return {
            'flower_id': row[0],
            'flower_name': row[1],
            'flower_creation': row[2]
        }

    @classmethod
    def get_data(cls, db):
        with db.connect() as con:
            data = con.execute(text(select_checkbox_flower)).fetchall()
        return list(map(cls.html, data))

    @classmethod
    def show(cls, db, render_template, index, with_data):
        if with_data:
            data = cls.get_data(db)
            return render_template(index, data=data)
        return render_template(index)


class ChangePage:
    def __new__(cls, db, render_template):
        INDEX = '/changes_page.html'
        return _ShowPage.show(db, render_template, INDEX, with_data=False)


class WateringPage:
    def __new__(cls, db, render_template):
        INDEX = '/watering_page.html'
        return _ShowPage.show(db, render_template, INDEX, with_data=True)



class Request:

    @classmethod
    def get_last_watering(cls, db, request):
        with db.connect() as con:
            ids = request.form.getlist('watering')
            last_watering_dict = {}
            if len(ids) > 0:
                ids = ','.join(ids)
                select = select_last_watering.format(ids=ids)
            else:
                return last_watering_dict

            last_waterings = con.execute(text(select)).fetchall()

            for watering in last_waterings:
                last_watering_dict[watering[0]] = watering[1]

            return last_watering_dict

    @classmethod
    def save(cls, db, request):
        last_waterting = cls.get_last_watering(db, request)

        ids = list(map(int, request.form.getlist('watering')))

        for id in ids:
            with db.connect() as con:
                values = {
                             'id': id,
                             'watering_date': datetime.now().strftime('%Y-%m-%d'),
                              'prev_watering_date': last_waterting.get(id)

                }

                con.execute(text(insert_watering), values)
                con.commit()

class WateringSavePage:
    def __new__(cls, db, render_template, request):
        INDEX = '/watering_added_page.html'
        Request.save(db=db, request=request)
        return _ShowPage.show(db, render_template, INDEX, with_data=False)