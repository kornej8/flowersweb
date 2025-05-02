import os
import io
from PIL import Image
from flowerweb.app.core.queries import (insert_new_picture, insert_new_flower)
from flowerweb.app.core.check_save_request import check_request
from sqlalchemy import text


class FlowerPicture:
    def __init__(self, request):
        self._file = request.files['flower_img']
        self.file_name = self._file.filename


    @property
    def file(self):
        bytea = io.BytesIO()
        img = self._file
        img.save(bytea)
        self._file.seek(0)
        return bytea.getvalue()

class SaveFromRequest:
    @classmethod
    @check_request
    def save_flower_name(cls, db, request):
        with db.connect() as con:
            values = {
                'flower_name': request.values['flower_name']
            }

            r = con.execute(text(insert_new_flower), values)

            con.commit()

            return r.fetchall()[0][0]


    @classmethod
    @check_request
    def save_picture(cls, db, request, id):

        flower = FlowerPicture(request)


        with db.connect() as con:
            values = {
                'id': id,
                'flower_file': flower.file,
                'flower_file_name' : flower.file_name
            }
            con.execute(text(insert_new_picture), values)
            con.commit()



class _AddedFlowerPage:
    INDEX_PAGE = '/added_flower_page.html'
    CLOSE = "fas fa-close"
    CHECK = "fas fa-check"


    def __init__(self, name, picture, render_template):
        self.name = name
        self.picture = picture
        self.render_template = render_template


    def generate_page(self):
        name = self.get_icon(self.name)
        picture = self.get_icon(self.picture)

        return self.render_template(self.INDEX_PAGE,
                                    **locals())

    def get_icon(self, _bool):
        return self.CHECK if _bool else self.CLOSE

    @property
    def html(self):
        return self.generate_page()


    @classmethod
    def show(cls, name, picture, render_template):
        page = cls(name, picture, render_template)
        return page.html

class AddedFlowerPage:
    def __new__(cls, name, picture, render_template):
        return _AddedFlowerPage.show(name, picture, render_template)


class GetNewFlower:
    def __new__(cls, db, request, render_template):
        name = SaveFromRequest.save_flower_name(db=db, request=request)
        picture = SaveFromRequest.save_picture(db=db, request=request, id=name)
        return AddedFlowerPage(name=name, picture=picture, render_template=render_template)
