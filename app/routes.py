from flask import flash, redirect, render_template, redirect, request, url_for
from app.forms import PokemonForm
import requests
from .models import db, Pokemon
from app import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def index():
    form = PokemonForm()
    if form.validate_on_submit():
        return redirect(url_for('pokemon_search', pokemon_name=form.pokemon_name.data))
    return render_template('index.html', form=form)

@app.route('/search/<pokemon_name>', methods=['GET', 'POST'])
def pokemon_search(pokemon_name):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
    if response.ok:
        data = response.json()
        name = data['name'].capitalize()
        ability = data["abilities"][0]["ability"]["name"]
        base_experience = data['base_experience']
        image_url  = data["sprites"]["front_shiny"]
        stats = data['stats']
        for stat in stats:
            if stat['stat']['name'] == 'attack':
                attack = stat['base_stat']
            elif stat["stat"]["name"] == "defense":
                defense = stat['base_stat']
            elif stat["stat"]["name"] == "hp":
                hp = stat['base_stat']


        return render_template('pokemon.html', name=name, ability=ability, base_experience=base_experience, image_url=image_url, attack=attack, defense=defense, hp=hp)
    else:
        return redirect(url_for('index', error_message=f'No pokemon found with name "{pokemon_name}"'))
    
caught_pokemon = {}
@app.route('/catch', methods=['GET', 'POST'])
def poke_catch(pokemon_name):
    form = PokemonForm()
    if form.validate_on_submit:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}')
        if response.ok:
            data = response.json()
            name = data['name'].capitalize()
            ability = data["abilities"][0]["ability"]["name"]
            base_experience = data['base_experience']
            image_url  = data["sprites"]["front_shiny"]
            stats = data['stats']
            for stat in stats:
                if stat['stat']['name'] == 'attack':
                    attack = stat['base_stat']
                elif stat["stat"]["name"] == "defense":
                    defense = stat['base_stat']
                elif stat["stat"]["name"] == "hp":
                    hp = stat['base_stat']
            caught_pokemon[pokemon_name] = {
                    'name': name,
                    'ability': ability,
                    'base_experience': base_experience,
                    'image_url': image_url,
                    'attack': attack,
                    'defense': defense,
                    'hp': hp,
            }
            return redirect(url_for('pokemon_search', pokemon_name=pokemon_name))
        else:
                flash(f'No pokemon found with name "{pokemon_name}"')
    return render_template('catch.html', form=form)


@app.route('/caught', methods=['POST'])
def add_caught_pokemon():
    form_data = request.form
    pokemon_name = form_data['pokemon_name']
    trainer_name = form_data['first_name']
    level = form_data['level']

    pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
    if pokemon:
        pokemon.trainer_name = trainer_name
        pokemon.level = level
    else:
        pokemon = Pokemon(name=pokemon_name, trainer_name=trainer_name, level=level)
        db.session.add(pokemon)

    db.session.commit()

    return redirect(url_for('index'))

    
