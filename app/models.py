from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
import requests

db = SQLAlchemy()

class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable = False, unique = True)
    ability = db.Column(db.String(45), nullable = False)
    hp = db.Column(db.Integer, nullable = False)
    attack = db.Column(db.Integer, nullable = False)
    defense = db.Column(db.Integer, nullable = False)
    front_shiny = db.Column(db.String, nullable = False) #not listed in ERD
    owner = db.relationship('Catcher', backref='pokemon', cascade='all,delete', lazy=True)

    def __init__(self,poke_id, name, ability, hp, attack, defense, front_shiny):
        self.poke_id = poke_id
        self.name = name
        self.ability = ability
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.front_shiny = front_shiny

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable = False)
    last_name = db.Column(db.String(45), nullable = False)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    pokemon_caught = db.relationship('Catcher', backref='owner', cascade='all,delete', lazy=True)

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()

class Catcher(db.Model):
    __tablename__ = "catcher"

    # id = db.Column(db.Integer, primary_key=True, nullable=False)
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    pokemon_name = db.Column(db.String(30), db.ForeignKey('pokemon.name'), nullable=False)

    def __init__(self, owner_id, pokemon_name):
        self.owner_id = owner_id
        self.pokemon_name = pokemon_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()