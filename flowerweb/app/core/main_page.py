import io
import base64
from sqlalchemy import text
from flowerweb.app.core.queries import (select_flowers)

class _MainPage:

    INDEX = '/index.html'

    def __init__(self, db, render_template, filter):
        self.db = db
        self.render_template = render_template
        self.filter = filter
        self.data = None


    @staticmethod
    def get_flower_picture(flower_picture):
        img = io.BytesIO(bytes(flower_picture))
        return base64.b64encode(img.getvalue()).decode('UTF-8')

    def to_html(self, flower):
        return {
            'flower_name': flower[0],
            'flower_picture': self.get_flower_picture(flower[1]),
            'flower_create': flower[2],
            'flower_watering': flower[3],
            'wo_watering_days': flower[4],
            'watering_last_days': flower[5]
        }


    def get_main_page_data(self):
        with self.db.connect() as con:

            get_flowers= select_flowers.format(_filter=self.filter)

            data = con.execute(text(get_flowers)).fetchall()
        self.data = list(map(self.to_html, data))


    def show(self):

        if not self.data:
            self.get_main_page_data()

        return self.render_template(self.INDEX, flowers=self.data)


class MainPage:
    def __new__(cls, db, render_template, filter=''):
        page = _MainPage(db, render_template, filter)
        return page.show()
