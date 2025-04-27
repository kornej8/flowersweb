from flask import Flask, render_template, request, redirect, url_for
from app.core.init_flower import AddFlowerPage
from app.core.save_flower_picture import GetNewFlower
from app.core.main_page import MainPage
from app.core.change_page import ChangePage, WateringPage, WateringSavePage
from db.db_connector import DBConnect

app = Flask("flowers_website")
db = DBConnect()


@app.route('/')
def main():
    return MainPage(db, render_template=render_template)


@app.route('/search/', methods=['GET'])
def search():
    flower_name = request.args.get('flower_name')
    return redirect(url_for('flower_page', flower_name=flower_name))


@app.route('/<string:flower_name>')
def flower_page(flower_name):
    return MainPage(db=db, render_template=render_template, filter=flower_name)


@app.route('/add_new_flower')
def add_new_flower():
    return AddFlowerPage(db=db, render_template=render_template)


@app.route('/add_new_flower_post', methods=['POST'])
def add_new_flower_post():
    return GetNewFlower(db=db, render_template=render_template, request=request)


@app.route('/changes')
def changes_page():
    return ChangePage(db=db, render_template=render_template)


@app.route('/watering')
def watering_page():
    return WateringPage(db=db, render_template=render_template)

@app.route('/watering', methods=['POST'])
def watering_page_post():
    return WateringSavePage(db=db, render_template=render_template, request=request)

if __name__ == '__main__':
    app.run(host="192.168.1.10", port=5000, debug=False)
