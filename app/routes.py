from flask import flash, redirect, render_template, request, url_for
from app.forms import PokemonForm, Attackform, UserAttackForm
import requests
from .models import db, Pokemon, User, Catcher
from app import app
from flask_login import current_user, login_required
from random import randint

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
        poke_id = data['id']
        name = data['name'].capitalize()
        ability = data["abilities"][0]["ability"]["name"]
        front_shiny = data["sprites"]["front_shiny"]
        stats = data['stats']
        for stat in stats:
            if stat['stat']['name'] == 'attack':
                attack = stat['base_stat']
            elif stat["stat"]["name"] == "defense":
                defense = stat['base_stat']
            elif stat["stat"]["name"] == "hp":
                hp = stat['base_stat']

        pokemon_data = {'poke_id': poke_id, 'name': name, 'ability': ability, 'hp': hp, 'attack': attack, 'defense': defense,
                        'front_shiny': front_shiny}
        
        pokemon = Pokemon(poke_id, name, ability, hp, attack, defense, front_shiny)

        pokemon.save_to_db()

        return render_template('pokemonCard.html', pokemon_data=pokemon_data)
    else:
        return redirect(url_for('index', error_message=f'No pokemon found with name "{pokemon_name}"'))

@app.route('/catch/<pokemon_name>', methods=['GET', 'POST'])
@login_required
def poke_catch(pokemon_name):
    if request.method == 'POST':
        pokemon = Pokemon.query.filter_by(name=pokemon_name).first()
        print(pokemon)

        if pokemon:
            caught_list = Catcher.query.filter_by(owner_id=current_user.id).all()
            print(caught_list)

            if len(caught_list) < 5:
                if pokemon in caught_list:
                    flash('This pokemon is already caught!', 'danger')
                    return redirect(url_for('pokemon_search'))
                
                team_id = randint(1,10000)
                my_pokemon = Catcher(current_user.id, pokemon.name)          
                print(my_pokemon)
                my_pokemon.save_to_db()

                # print(f'You have successfully caught {pokemon_name}')

                # caught_poke = Catcher.query.filter_by(owner_id=current_user.id)
                # caught_list = [poke[0] for poke in caught_poke]

                print(f'Caught list: {pokemon.name}')

            else:
                flash('Cannot catch more than 5 pokemons!', 'danger')
        else:
            flash('The pokemon you are trying to catch does not exist!', 'danger')

        return redirect(url_for('caught_pokemon'))

    return render_template('catch.html', pokemon_name=pokemon_name)


@app.route('/caught_pokemon')
@login_required
def caught_pokemon():
    pokedex = Catcher.query.filter_by(owner_id=current_user.id).all()
    pokemon_data = []

    for poke in pokedex:
        pokemon = {
            'name': poke.pokemon_name,
            'ability': poke.pokemon.ability,
            'hp': poke.pokemon.hp,
            'attack': poke.pokemon.attack,
            'defense': poke.pokemon.defense,
            'front_shiny': poke.pokemon.front_shiny
        }
        pokemon_data.append(pokemon)

    return render_template('pokemon.html', pokemon_data=pokemon_data)


# @app.route('/', methods=["GET"])
# def home_page():
#     return render_template('index.html')


# @app.route('/battle', methods = ['GET', 'POST'])
# def battle():
#     form = Attackform()
#     opponentform = UserAttackForm()
#     pokemons = Pokemon.query.filter_by(user_id = current_user.id)

#     if request.method == 'POST':
#         if opponentform.validate():
#             opponent_user_name = opponentform.opponent.data
#             if opponent_user_name.lower() == "random":
#                 opponents = User.query.all()
#                 randomindex = randint(0, len(opponents)-1)
#                 opponent_user_name = 

