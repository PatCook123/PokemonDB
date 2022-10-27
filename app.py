from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
app = Flask(__name__)

bootstrap = Bootstrap4(app)

@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html')

@app.route('/gyms')
def gyms_page():
    return render_template('gyms.html')

@app.route('/trainers')
def trainer_page():
    return render_template("trainers.html")

@app.route('/pokedecks')
def pokedecks_page():
    return render_template("pokedecks.html")

@app.route('/pokemon')
def pokemon_page():
    return render_template('pokemon.html')

@app.route('/pokemon_evolutions')
def poke_evolutions_page():
    return render_template('pokemon_evolutions.html')    

@app.route('/pokemon_types')
def poke_types_page():
    return render_template('pokemon_types.html')        

@app.route('/moves_move-types')
def moves_page():
    return render_template("moves_move-types.html")

@app.route('/abilities')
def abilities_page():
    return render_template("abilities.html")

if __name__ == '__main__':
    app.run(port=31988)
