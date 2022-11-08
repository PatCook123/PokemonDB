from flask import Flask, render_template, json, redirect, request
from flask_bootstrap import Bootstrap4
import os
import static.database.db_connector as db

app = Flask(__name__)

db_connection = db.connect_to_database()

bootstrap = Bootstrap4(app)

@app.route('/')
def homepage():  
    return render_template('index.html')

# Gym Read and Create
@app.route('/gyms', methods=["POST", "GET"])
def gyms_page():
    # Contains post request method for adding gym.
    if request.method == "POST":
        if request.form.get("Add_Gym"):
            gym_nameInput = request.form["gym_name"]
            gym_addressInput = request.form["gym_address"]
            gym_zipInput = request.form["gym_zip"]
            gym_cityInput = request.form["gym_city"]
            gym_stateInput = request.form["gym_state"]

            for _ in [gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput]:
                if _ == "":
                    _ = "NULL"

            query = f"INSERT INTO gyms (gym_name, gym_address, gym_zip, gym_city, gym_state) \
                    VALUES (\"{gym_nameInput}\", \"{gym_addressInput}\", {gym_zipInput}, \"{gym_cityInput}\", \"{gym_stateInput}\");"
            print(query)
            cursor = db.execute_query(db_connection=db_connection, query=query)
            return redirect('/gyms')

            # Only gym_name is non-nullable. 
            # Conditions below to handle differnt sets of inputs.
            if gym_addressInput == gym_zipInput == gym_cityInput ==gym_stateInput == "":
                query = f"INSERT INTO gyms (gym_name) VALUES (\"{gym_nameInput}\");"
                print(query)
                cursor = db.execute_query(db_connection=db_connection, query=query)
                return redirect('/gyms')
                
    if request.method == "GET":
        # SQL query and execution to populate table on gyms.html
        query = "SELECT gym_id, gym_name, gym_address, gym_zip, gym_city, gym_state, COUNT(trainers.trainer_id) AS members FROM gyms\
        LEFT JOIN trainers ON trainers.gyms_gym_id = gyms.gym_id\
        GROUP BY gym_id\
        ORDER BY gym_name;"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template('gyms.html', gyms=results)

# Gym Deletion
@app.route('/delete_gym/<int:id>')
def delete_gym(id):
    # SQL query and execution to delete gym by passed id
    query = f"DELETE FROM gyms WHERE gym_id = \"{id}\""
    cursor = db.execute_query(db_connection=db_connection, query=query)
    return redirect('/gyms')


@app.route('/trainers')
def trainer_page():
    return render_template("trainers.html")

@app.route('/pokedecks')
def pokedecks_page():
    return render_template("pokedecks.html")

@app.route('/pokemon')
def pokemon_page():
    query = "SELECT pokemon_id, pokemon_name, height, weight, evolution FROM pokemon ORDER BY pokemon_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template('pokemon.html', pokemon=results)

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
