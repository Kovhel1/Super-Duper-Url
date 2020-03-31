import os

#создание экземпляра класса
from flask import Flask
app = Flask(__name__)

# file config
from config import Config
app.config.from_object(Config)

#возврат шаблонов с помощью функции render_template и друие функции для routes
from flask import render_template
from flask import request, redirect




#MODESL
#инициализация БД
from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy(app)  

#миграции
from flask_migrate import Migrate
migrate = Migrate(app, db)

import string
from random import choices

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(3), unique=True)
    visits = db.Column(db.Integer, default=0)
    
    #ссылка на функцию, для создания короткой ссылки
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_link()
        
    #функция создания короткой ссылки    
    def generate_short_link(self):
        characters = string.digits + string.ascii_letters
        short_url = ''.join(choices(characters, k=3))

        link = self.query.filter_by(short_url=short_url).first()

        if link:
            return self.generate_short_link()
        
        return short_url
    
    #необязательный метод, служит для отладки и тестирования бд 
    def __repr__(self):
        return '<Link {}>'.format(self.original_url) 



#ROUTES
@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    link.visits = link.visits + 1
    db.session.commit()
    return redirect(link.original_url) 

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/add_link', methods=['POST'])
def add_link():
    original_url = request.form['original_url']
    link = Link(original_url=original_url)
    db.session.add(link)
    db.session.commit()

    return render_template('link_added.html', 
        new_link=link.short_url, original_url=link.original_url)

@app.route('/stats')
def stats():
    links = Link.query.all()

    return render_template('stats.html', links=links)

#должно возвращаться 200
#недопустимый маршрут
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#исключение кода
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
