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

        # Allows for null inputs on nullable values
        for _ in [gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput]:
            if _ == "":
                _ = "NULL"

        else:
            query = "INSERT INTO gyms (gym_name, gym_address, gym_zip, gym_city, gym_state) \
                    VALUES (%s, %s, %s, %s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query % (gym_nameInput, gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput))
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
    if request.method == "POST":
        if request.form.get("Update_Gym"):
            gym_nameInput = request.form["gym_name"]
            gym_addressInput = request.form["gym_address"]
            gym_zipInput = request.form["gym_zip"]
            gym_cityInput = request.form["gym_city"]
            gym_stateInput = request.form["gym_state"]

            # Allows for null inputs on nullable values
            for _ in [gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput]:
                if _ == "":
                    _ = "NULL"

            query = "UPDATE gyms SET gyms.gym_name = %s, gyms.gym_address = %s, gyms.gym_zip = %s, gyms.gym_city = %s, gyms.gym_state = %s WHERE gyms.gym_id = %s;"
            print(query % (gym_nameInput, gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput, id))
            cur = mysql.connection.cursor()
            cur.execute(query, (gym_nameInput, gym_addressInput, gym_zipInput, gym_cityInput, gym_stateInput, id))
            mysql.connection.commit()
            return redirect('/gyms')   

    if request.method == "GET":
        # Two queries executied. query gets values for the gym for update gym form fields.
        query = 'SELECT gym_id, gym_name, gym_address, gym_zip, gym_city, gym_state FROM gyms WHERE gym_id = %s' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        u_gym_data = cur.fetchall()

        # Query2 gets values for all gyms for page table.
        query2 = 'SELECT gym_id, gym_name, gym_address, gym_zip, gym_city, gym_state, COUNT(trainers.trainer_id) AS members FROM gyms\
        LEFT JOIN trainers ON trainers.gyms_gym_id = gyms.gym_id\
        GROUP BY gym_id\
        ORDER BY gym_name;'
        cur.execute(query2)
        gym_data = cur.fetchall()
        return render_template('update_gyms_modal.j2', u_gym = u_gym_data, gyms=gym_data)    

@app.route('/trainers', methods=['POST', 'GET'])
def trainer_page():
    # Contains post request method for adding trainer.
    if request.method == 'POST':
        if request.form.get("Add_Trainer"):
            first_nameInput = request.form["first_name"]
            last_nameInput = request.form["last_name"]
            xpInput = request.form["xp"]
            gyms_gym_idInput = request.form["gym_id_dropdown"]

        # Allows for null inputs on nullable values
        for _ in [first_nameInput, last_nameInput, xpInput, gyms_gym_idInput]:
            if _ == "":
                _ = "NULL"

        else:
            query = 'INSERT INTO trainers (first_name, last_name, xp, gyms_gym_id) VALUES ("%s", "%s", "%s", "%s");'
            print(query % (first_nameInput, last_nameInput, xpInput, gyms_gym_idInput))
            cur = mysql.connection.cursor()
            cur.execute(query % (first_nameInput, last_nameInput, xpInput, gyms_gym_idInput))
            mysql.connection.commit()
            return redirect('/trainers')

    if request.method == 'GET':
        # Provide values to populate trainers table
        query = 'SELECT trainer_id, first_name, last_name, xp, gyms.gym_name AS gym, pokedecks.pokedeck_name AS pokedeck FROM trainers\
                    LEFT JOIN gyms ON gyms.gym_id = trainers.gyms_gym_id\
                    LEFT JOIN pokedecks ON pokedecks.trainers_trainer_id = trainers.trainer_id\
                    GROUP BY trainer_id\
                    ORDER BY trainer_id;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        trainer_data = cur.fetchall()
         
        query2 = 'SELECT gym_id, gym_name FROM gyms\
                ORDER BY gym_id;'
        cur.execute(query2)
        gym_dropdown_data = cur.fetchall()

        return render_template('trainers.html', trainers=trainer_data, gyms=gym_dropdown_data)

# Trainer Deletion
@app.route('/delete_trainer/<int:id>')
def delete_trainer(id):
     # SQL query and execution to delete gym by passed id
     query = "DELETE FROM trainers WHERE trainer_id = '%s'"
     cur = mysql.connection.cursor()
     cur.execute(query, (id,))
     mysql.connection.commit()
     return redirect('/trainers')

# Trainer Update
# Gym Update
@app.route('/update_trainer/<int:id>', methods=['POST', 'GET'])
def update_trainer(id):
    if request.method == "POST":
        if request.form.get("Update_Trainer"):
            first_nameInput = request.form["first_name"]
            last_nameInput = request.form["last_name"]
            xpInput = request.form["xp"]
            gyms_gym_idInput = request.form["gym_id_dropdown"]

            # Allows for null inputs on nullable values
            for _ in [last_nameInput, xpInput, gyms_gym_idInput]:
                if _ == "":
                    _ = "NULL"

            query = 'UPDATE trainers SET first_name = "%s", last_name = "%s", xp = "%s", gyms_gym_id = "%s"\
                    WHERE trainer_id = "%s"'
            print(query % (first_nameInput, last_nameInput, xpInput, gyms_gym_idInput, id))
            cur = mysql.connection.cursor()
            cur.execute(query % (first_nameInput, last_nameInput, xpInput, gyms_gym_idInput, id))
            mysql.connection.commit()
            return redirect('/trainers')   

    if request.method == "GET":
        # Three queries executied. query gets values for the gym for update gym form fields.
        query = 'SELECT trainer_id, first_name, last_name, xp, gyms.gym_name AS gym, pokedecks.pokedeck_name AS pokedeck FROM trainers\
                    LEFT JOIN gyms ON gyms.gym_id = trainers.gyms_gym_id\
                    LEFT JOIN pokedecks ON pokedecks.trainers_trainer_id = trainers.trainer_id\
                    GROUP BY trainer_id\
                    ORDER BY trainer_id;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        trainer_data = cur.fetchall()
         
        query2 = 'SELECT gym_id, gym_name FROM gyms\
                ORDER BY gym_id;'
        cur.execute(query2)
        gym_dropdown_data = cur.fetchall()

        query3 = 'SELECT trainer_id, first_name, last_name, xp, gyms.gym_name AS gym FROM trainers\
                    LEFT JOIN gyms ON gyms.gym_id = trainers.gyms_gym_id\
                    WHERE trainer_id = %s;'
        cur.execute(query3 % (id))
        u_trainer_data = cur.fetchall()

        return render_template('update_trainers.j2', trainers=trainer_data, gyms=gym_dropdown_data, u_trainer=u_trainer_data)   


@app.route('/trainers_search', methods=['POST'])
def search_trainers():
    if request.method == "POST":
        if request.form.get("Search_Trainers"):
            print('search received')
            searchInput = request.form["searchInput"]
            if searchInput in ["", None]:
                searchInput = "NULL"
            query = 'SELECT first_name, last_name, xp, gyms.gym_name AS gym, pokedecks.pokedeck_name AS pokedeck FROM trainers\
                LEFT JOIN gyms ON gyms.gym_id = trainers.gyms_gym_id\
                LEFT JOIN pokedecks ON pokedecks.trainers_trainer_id = trainers.trainer_id\
                GROUP BY trainer_id\
                ORDER BY trainer_id;'
            cur = mysql.connection.cursor()
            cur.execute(query % (searchInput))
            trainer_data = cur.fetchall()

            query2 = 'SELECT gym_id, gym_name FROM gyms\
                    ORDER BY gym_id;'
            cur.execute(query2)
            gym_dropdown_data = cur.fetchall()

            return render_template('trainers.html', trainers=trainer_data, gyms=gym_dropdown_data)

#WHERE first_name LIKE "%:%s%"\

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