from flask import flash, redirect, render_template, redirect, request, url_for
from app.forms import PokemonForm
import requests
from .models import db, Pokemon, Pokedex
from app import app
from flask_login import current_user, login_required


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

        pokemon_data = {'name': name, 'ability': ability, 'hp': hp, 'attack':attack, 'defense': defense, 'front_shiny': image_url}
        return render_template('pokemonCard.html', pokemon_data = pokemon_data)
    else:
        return redirect(url_for('index', error_message=f'No pokemon found with name "{pokemon_name}"'))

caught_pokemon = {}

@app.route('/catch/<pokemon_name>', methods=['POST'])
@login_required 
def poke_catch(pokemon_name):
    if len(caught_pokemon) >= 5:
        flash('You cannot catch more than 5 pokemons!')
        return render_template('catch.html')

    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}')
    if response.ok:
        data = response.json()
        name = data['name'].capitalize()
        ability = data["abilities"][0]["ability"]["name"]
        image_url = data["sprites"]["front_shiny"]
        stats = data['stats']
        for stat in stats:
            if stat['stat']['name'] == 'attack':
                attack = stat['base_stat']
            elif stat["stat"]["name"] == "defense":
                defense = stat['base_stat']
            elif stat["stat"]["name"] == "hp":
                hp = stat['base_stat']

        pokemon = Pokemon(name=name, ability=ability, hp=hp, attack=attack, defense=defense, front_shiny=image_url)
        db.session.add(pokemon)
        db.session.commit()

        pokedex_entry = Pokedex(user_id=current_user.id, poke_id=pokemon.poke_id)
        db.session.add(pokedex_entry)
        db.session.commit()

        caught_pokemon[name] = {'name': name, 'ability': ability, 'hp': hp, 'attack':attack, 'defense': defense, 'front_shiny': image_url}

        flash(f'You caught {name}!')
        return render_template('catch.html')
    else:
        flash(f'No pokemon found with name "{pokemon_name}"')

    return render_template('pokemon.html', caught_pokemon = caught_pokemon)





@app.route('/caught', methods=['POST'])
def caught_pokemon():
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

    return render_template('pokemon.html', caught_pokemon = caught_pokemon)


@app.route('/add_pokemon', methods=['POST'])
def add_pokemon():
    data = request.get_json()
    name = data['name']
    ability = data['ability']
    hp = data['hp']
    attack = data['attack']
    defense = data['defense']
    caught_pokemon[name] = {'ability': ability, 'hp': hp, 'attack': attack, 'defense': defense}
  

    
