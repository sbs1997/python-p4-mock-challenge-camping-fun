#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers', methods=['GET', 'POST'])
def get_campers():
    if request.method == 'GET':
        campers = Camper.query.all()
        campers_dict = []
        for camper in campers:
            campers_dict.append(camper.to_dict(rules=('-signups',)))
        response = make_response(campers_dict, 200)
    
    return response

@app.route('/campers/<int:id>', methods= ['GET', 'PATCH'])
def camper_by_id(id):
    camper = Camper.query.filter(Camper.id == id).first()
    error = {"error": "Camper not found"}
    if camper:
        if request.method == 'GET':
            response = make_response(camper.to_dict(), 200)
        elif request.method == 'PATCH':
            old_camper = camper
            for attr in request.form:
                setattr(camper, attr, request.form.get(attr))
            db.session.commit()
            if old_camper != camper:
                response = make_response(camper.to_dict(), 201)
            else:
                error = {"errors": ["validation errors"]}
                response = make_response(jsonify(error), 400)
    else:
        response = make_response(jsonify(error), 404)
    
    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
