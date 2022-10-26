# Group 89
# Patrick Cook & Cheyenne Plutchak

from flask_bootstrap import Bootstrap4
from flask import Flask, render_template, url_for
import os


# Configuration

app = Flask(__name__, template_folder = '/cs340_pokemondb/templates')
"""db_connection = db.connect_to_database()"""
bootstrap = Bootstrap4(app)

# Routes 

@app.route('/')
def root():
    return render_template("index.html")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 50050))
    app.run(port=port, debug=True)