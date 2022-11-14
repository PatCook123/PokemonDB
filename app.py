from flask import Flask, render_template, json, redirect, request
from flask_mysqldb import MySQL
from flask_bootstrap import Bootstrap
import os


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_cookpat'
app.config['MYSQL_PASSWORD'] = '1134' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_cookpat'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

@app.route('/')
def homepage():  
    return render_template('index.html')

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

             # Only gym_name is non-nullable. 
             # Conditions below to handle differnt sets of inputs.
             if gym_addressInput == gym_zipInput == gym_cityInput ==gym_stateInput == "":
                query = "INSERT INTO gyms (gym_name) VALUES (%s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (gym_nameInput))
                mysql.connection.commit()

             else:
                query = "INSERT INTO gyms (gym_name, gym_address, gym_zip, gym_city, gym_state) \
                        VALUES (%s, %s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (gym_nameInput, gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput))
                mysql.connection.commit()
                return redirect('/gyms')
                
    if request.method == "GET":
        # SQL query and execution to populate table on gyms.html
        query = "SELECT gym_id, gym_name, gym_address, gym_zip, gym_city, gym_state, COUNT(trainers.trainer_id) AS members FROM gyms\
        LEFT JOIN trainers ON trainers.gyms_gym_id = gyms.gym_id\
        GROUP BY gym_id\
        ORDER BY gym_name;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        gym_data = cur.fetchall()
        return render_template('gyms.html', gyms=gym_data)

# Gym Deletion
@app.route('/delete_gym/<int:id>')
def delete_gym(id):
     # SQL query and execution to delete gym by passed id
     query = "DELETE FROM gyms WHERE gym_id = '%s'"
     cur = mysql.connection.cursor()
     cur.execute(query, (id,))
     mysql.connection.commit()
     return redirect('/gyms')

# Gym Update
@app.route('/update_gym/<int:id>', methods=['POST', 'GET'])
def update_gym(id):
    if request.method == "GET":
        query = 'SELECT * FROM gyms WHERE gym_id = %s' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        gym_data = cur.fetchall()
        return render_template('update_gyms_modal.j2', gyms=gym_data)

    if request.method == "POST":
         if request.form.get("Update_Gym"):
             gym_nameInput = request.form["gym_name"]
             gym_addressInput = request.form["gym_address"]
             gym_zipInput = request.form["gym_zip"]
             gym_cityInput = request.form["gym_city"]
             gym_stateInput = request.form["gym_state"]

             # Only gym_name is non-nullable. 
             # Conditions below to handle differnt sets of inputs.
             if gym_addressInput == gym_zipInput == gym_cityInput ==gym_stateInput == "":
                query = "UPDATE gyms SET gyms.gym_name = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (gym_nameInput))
                mysql.connection.commit()

             else:
                query = "UPDATE gyms SET gyms.gym_name = %s, gyms.gym_address = %s, gyms.gym_zip = %s, gyms.gym_city = %s, gyms.gym_state = %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (gym_nameInput, gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput))
                mysql.connection.commit()
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
    cur = mysql.connection.cursor()
    cur.execute(query)
    pokemon_data = cur.fetchall()
    return render_template('pokemon.html', pokemon=pokemon_data)

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