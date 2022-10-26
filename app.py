from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
app = Flask(__name__)

bootstrap = Bootstrap4(app)

@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html')

@app.route('/pokemon')
def gympage():
    return render_template('pokemon.html')

@app.route('/gyms')
def gympage():
    return render_template('gyms.html')

@app.route('/trainers')
def trainerpage():
    return render_template("trainers.html")

@app.route('/pokedecks')
def pokedeckspage():
    return render_template("pokedecks.html")

@app.route('/moves_move-types')
def movespage():
    return render_template("moves_move-types.html")

if __name__ == '__main__':
    app.run(port=3000)
