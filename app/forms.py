from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    pokemon_name = StringField('Pokemon Name', validators=[DataRequired()], render_kw={'autofocus': True})
    submit = SubmitField('Submit')

class Attackform(FlaskForm):
    attacker = StringField("Attacker" , validators = [DataRequired()], render_kw={'autofocus': True})
    defender = StringField("Defender" , validators = [DataRequired()])
    submit = SubmitField('Submit')

class UserAttackForm(FlaskForm):
    opponent = StringField("Opponent username" , validators = [DataRequired()], render_kw={'autofocus': True})
    submit_user = SubmitField()
    
