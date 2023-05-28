#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Animal, Zookeeper, Enclosure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    if not animal:
        response_body = '<h1>404 not found </h1>'

    response_body = f''
    response_body += f'<ul>ID: {animal.id}</ul>'
    response_body += f'<ul>Name: {animal.name}</ul>'
    response_body += f'<ul>Species: {animal.species}</ul>'
    response_body += f'<ul>Zookeeper: {animal.zookeeper.name}</ul>'
    response_body += f'<ul>Enclosure: {animal.enclosure.environment}</ul>'
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    if not zookeeper:
        response_body = '<h1>404 not found </h1>'

    response_body = f'<ul>Name: {zookeeper.name}</ul> \
                    <ul>Birthday: {zookeeper.birthday}</ul>'
    
    animals = Animal.query.filter(Animal.zookeeper_id == zookeeper.id).all()
    for animal in animals:
        response_body += f'<ul>Animal: {animal.name}</ul>'
    response = make_response(response_body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    response_body = f''
    response_body += f'<ul>ID: {enclosure.id}</ul>'
    response_body += f'<ul>Environment: {enclosure.environment}</ul>'
    response_body += f'<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'

    animals = Animal.query.filter(Animal.enclosure_id == enclosure.id).all()
    for animal in animals:
        response_body += f'<ul>Animal: {animal.name}</ul>'
    response = make_response(response_body)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
