from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
import requests

db = SQLAlchemy()

# class Pokemon:
#     def __init__(self, name):
#         self.name = name
#         self.data = self._get_pokemon_data(name)

#     def _get_pokemon_data(self, name):
#         url = f'https://pokeapi.co/api/v2/pokemon/{name}'
#         response = requests.get(url)
#         data = response.json()
#         return data

#     def get_image_url(self):
#         return self.data["sprites"]["front_shiny"]


class Pokemon(db.Model):
    poke_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable = False, unique = True)
    ability = db.Column(db.String(45), nullable = False)
    hp = db.Column(db.Integer, nullable = False)
    attack = db.Column(db.Integer, nullable = False)
    defense = db.Column(db.Integer, nullable = False)
    front_shiny = db.Column(db.String, nullable = False) #not listed in ERD

    def __init__(self, name, ability, hp, attack, defense, front_shiny):
        self.name = name
        self.ability = ability
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.front_shiny = front_shiny

    def saveToDB(self):
        db.session.add(self)
        db.session.commit(self)

    def deletePokemon(self):
        db.session.delete(self)
        db.session.commit(self)

    def _attack(self, pokemon):
        if self.attack > pokemon.defense:
            pokemon.hp -= self.attack - pokemon.defense
            db.session.commit()
            if pokemon.hp < 1:
                owner = User.query.get(pokemon.user_id)
                owner.deaths += 1
                owner2 = User.query.get(self.user_id)
                owner2.kills += 1
                db.sessioncommit()
                pokemon.delete_pokemon()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable = False)
    last_name = db.Column(db.String(45), nullable = False)
    username = db.Column(db.String(45), nullable = False, unique = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())

    def __init__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def saveChanges(self):
        db.session.commit()