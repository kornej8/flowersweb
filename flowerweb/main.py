import os.path
from flask import Flask, render_template, request, redirect, url_for
from flowerweb.app.core.init_flower import AddFlowerPage
from flowerweb.app.core.save_flower_picture import GetNewFlower
from flowerweb.app.core.main_page import MainPage
from flowerweb.app.core.change_page import (ChangePage,
                                            WateringPage,
                                            WateringSavePage,
                                            FertilizerPage,
                                            FertilizerSavePage)
from flowerweb.db.db_connector import DBConnect

template_path = os.path.join(os.path.dirname(__file__), 'templates')
application = Flask("flowers_website", template_folder=template_path)
db = DBConnect()

@application.route('/')
def main():
    return MainPage(db, render_template=render_template)


@application.route('/search/', methods=['GET'])
def search():
    flower_name = request.args.get('flower_name')
    return redirect(url_for('flower_page', flower_name=flower_name))


@application.route('/<string:flower_name>')
def flower_page(flower_name):
    return MainPage(db=db, render_template=render_template, filter=flower_name)


@application.route('/add_new_flower')
def add_new_flower():
    return AddFlowerPage(db=db, render_template=render_template)


@application.route('/add_new_flower_post', methods=['POST'])
def add_new_flower_post():
    return GetNewFlower(db=db, render_template=render_template, request=request)


@application.route('/changes')
def changes_page():
    return ChangePage(db=db, render_template=render_template)


@application.route('/watering')
def watering_page():
    return WateringPage(db=db, render_template=render_template)

@application.route('/watering', methods=['POST'])
def watering_page_post():
    return WateringSavePage(db=db, render_template=render_template, request=request)

@application.route('/fertilizer')
def fertilizer_page():
    return FertilizerPage(db=db, render_template=render_template)

@application.route('/fertilizer', methods=['POST'])
def fertilizer_page_post():
    return FertilizerSavePage(db=db, render_template=render_template, request=request)

if __name__ == '__main__':
    application.run()