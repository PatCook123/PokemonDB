from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
app = Flask(__name__)

bootstrap = Bootstrap4(app)

@app.route('/')
def homepage():  # put application's code here
    return render_template('index.html')

@app.route('/gyms')
def gympage():
    return render_template('gyms.html')

@app.route('/pokemon')
def root():
    return render_template("pokemon.html")
    
@app.route('/pokemon_evolutions')
def root():
    return render_template("pokemon_evolutions.html")

@app.route('/pokemon_types')
def root():
    return render_template("pokemon_types.html")

@app.route('/abilities')
def root():
    return render_template("abilities.html")  

if __name__ == '__main__':
    app.run(port=3000)
