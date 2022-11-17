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

#------------------------------------------------------------------GYMS--------------------------------------------------------------#
# Populate gyms table and add new gyms
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
            query = 'INSERT INTO gyms (gym_name, gym_address, gym_zip, gym_city, gym_state) \
                    VALUES ("%s", "%s", "%s", "%s", "%s");'
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

#------------------------------------------------------------------TRAINERS--------------------------------------------------------------#
# Populate trainers table and add new trainers
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
    # SQL query and execution to delete trainer by passed id
    query = "DELETE FROM trainers WHERE trainer_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/trainers')

# Trainer Update
@app.route('/update_trainer/<int:id>', methods=['POST', 'GET'])
def update_trainer(id):
    if request.method == "POST":
        if request.form.get("Update_Trainer"):
            first_nameInput = request.form["first_nameInput"]
            last_nameInput = request.form["last_nameInput"]
            xpInput = request.form["xpInput"]
            gyms_gym_idInput = request.form["gym_id_dropdownInput"]

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
         
        # Need to tweak query and logic to show current gym first 
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

#------------------------------------------------------------------POKEDECK TYPES--------------------------------------------------------------#
@app.route('/pokedecks', methods=['POST', 'GET'])
def pokedecks_page():
    if request.method == 'POST':
        if request.form.get("Add_Pokedeck"):
            pokedeck_nameInput = request.form["pokedeck_nameInput"]
            trainers_trainer_idInput = request.form["trainer_id_dropdown"]

            # Allows for null inputs on nullable values
            if trainers_trainer_idInput == "":
                trainers_trainer_idInput = "NULL"

            query = 'INSERT INTO pokedecks (pokedeck_name, trainers_trainer_id)\
                    VALUES ("%s", %s);'
            cur = mysql.connection.cursor()
            cur.execute(query % (pokedeck_nameInput, trainers_trainer_idInput))
            mysql.connection.commit()
            return redirect('/pokedecks')

    if request.method == 'GET':
        query = 'SELECT pokedeck_id, pokedeck_name, CONCAT(first_name, SPACE(1), last_name) AS name,\
                COUNT(pokedecks_have_pokemon.pokemon_pokemon_id) AS cards FROM pokedecks\
                LEFT JOIN trainers ON pokedecks.trainers_trainer_id = trainers.trainer_id\
                LEFT JOIN pokedecks_have_pokemon ON pokedecks_have_pokemon.pokedecks_pokedeck_id = pokedecks.pokedeck_id\
                GROUP BY pokedeck_id\
                ORDER BY pokedeck_name;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pokedecks_data = cur.fetchall()
        
        query2 = 'SELECT trainer_id, CONCAT(first_name, SPACE(1), last_name) as name FROM trainers ORDER BY trainer_id;'
        cur.execute(query2)
        trainers_data = cur.fetchall()

        return render_template("pokedecks.html", pokedecks=pokedecks_data, trainers=trainers_data)

# Pokedeck Deletion
@app.route('/delete_pokedeck/<int:id>')
def delete_pokedeck(id):
    # SQL query and execution to delete pokedeck by passed id
    query = "DELETE FROM pokedecks WHERE pokedeck_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/pokedecks')

@app.route('/update_pokedeck/<int:id>', methods=['POST', 'GET'])
def update_pokedeck(id):
    if request.method == 'POST':
        if request.form.get("Update_Pokedeck"):
            pokedeck_idInput = request.form["pokedeck_id"]
            pokedeck_nameInput = request.form["pokedeck_nameInput"]
            trainers_trainer_idInput = request.form["trainer_id_dropdown"]

            # Allows for null inputs on nullable values
            if trainers_trainer_idInput == "":
                trainers_trainer_idInput = "NULL"

            query = 'UPDATE pokedecks SET pokedeck_name = "%s", trainers_trainer_id = "%s"\
                    WHERE pokedeck_id = "%s";'
            cur = mysql.connection.cursor()
            cur.execute(query % (pokedeck_nameInput, trainers_trainer_idInput, pokedeck_idInput))
            mysql.connection.commit()
            return redirect('/pokedecks')

    if request.method == 'GET':
        query = 'SELECT pokedeck_id, pokedeck_name, CONCAT(first_name, SPACE(1), last_name) AS owner_name,\
                COUNT(pokedecks_have_pokemon.pokemon_pokemon_id) AS cards FROM pokedecks\
                LEFT JOIN trainers ON pokedecks.trainers_trainer_id = trainers.trainer_id\
                LEFT JOIN pokedecks_have_pokemon ON pokedecks_have_pokemon.pokedecks_pokedeck_id = pokedecks.pokedeck_id\
                GROUP BY pokedeck_id\
                ORDER BY pokedeck_name;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pokedecks_data = cur.fetchall()
        
        # Need to tweak query and logic to show current owner first
        query2 = 'SELECT trainer_id, CONCAT(first_name, SPACE(1), last_name) as name FROM trainers ORDER BY trainer_id;'
        cur.execute(query2)
        trainers_data = cur.fetchall()

        query3 ='SELECT pokedeck_id, pokedeck_name, CONCAT(first_name, SPACE(1), last_name) AS owner_name FROM pokedecks\
                LEFT JOIN trainers ON pokedecks.trainers_trainer_id = trainers.trainer_id\
                WHERE pokedeck_id = "%s"\
                GROUP BY pokedeck_id\
                ORDER BY pokedeck_name;'
        cur.execute(query3 % (id))
        u_pokedeck_data = cur.fetchall()
        return render_template('update_pokedecks.j2', pokedecks=pokedecks_data, trainers=trainers_data, u_pokedeck=u_pokedeck_data)

#------------------------------------------------------------------POKEMON--------------------------------------------------------------#
# Populate pokemon table and add new pokemon
@app.route('/pokemon', methods=["POST", "GET"])
def pokemon_page():
    # Contains post request method for adding evolution.
    if request.method == "POST":
        if request.form.get("Add_Pokemon"):
            pokemon_nameInput = request.form["poke_name"]
            pokemon_heightInput = request.form["poke_height"]
            pokemon_weightInput = request.form["poke_weight"]
            pokemon_evoInput = request.form["hasEvolution"]

            query = 'INSERT INTO pokemon (pokemon_name, height, weight, evolution) \
                    VALUES ("%s", "%s", "%s", "%s");'
            cur = mysql.connection.cursor()
            cur.execute(query % (pokemon_nameInput, pokemon_heightInput, pokemon_weightInput, pokemon_evoInput))
            mysql.connection.commit()
            return redirect('/pokemon')
                
    if request.method == "GET":
        # SQL query and execution to populate table on pokemon_evolutions.html
        query = "SELECT pokemon_id, pokemon_name, height, weight, evolution FROM pokemon ORDER BY pokemon_id; \
                 ORDER BY pokemon_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        pokemon_data = cur.fetchall()
        return render_template('pokemon.html', pokemon=pokemon_data)  

# Pokemon Deletion
@app.route('/delete_pokemon/<int:id>')
def delete_pokemon(id):
    # SQL query and execution to delete evolution by passed id
    query = "DELETE FROM pokemon WHERE pokemon_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/pokemon')          

#------------------------------------------------------------------EVOLUTION TYPES--------------------------------------------------------------#
# Populate pokemon evolutions table and add new pokemon evolutions
@app.route('/pokemon_evolutions', methods=["POST", "GET"])
def poke_evolutions_page():
    # Contains post request method for adding evolution.
    if request.method == "POST":
        if request.form.get("Add_Evolution"):
            evolv_nameInput = request.form["evolv_name"]
            evolv_levelInput = request.form["evolv_level"]

            query = 'INSERT INTO pokemon_evolutions (evolv_name, evolv_level) \
                    VALUES ("%s", "%s");'
            cur = mysql.connection.cursor()
            cur.execute(query % (evolv_nameInput, evolv_levelInput))
            mysql.connection.commit()
            return redirect('/pokemon_evolutions')
                
    if request.method == "GET":
        # SQL query and execution to populate table on pokemon_evolutions.html
        query = "SELECT evolv_id, evolv_name, evolv_level FROM pokemon_evolutions \
                 ORDER BY evolv_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        evolv_data = cur.fetchall()
        return render_template('pokemon_evolutions.html', pEvolvs=evolv_data)

# Pokemon Evolutions Deletion
@app.route('/delete_evolv/<int:id>')
def delete_evolvs(id):
    # SQL query and execution to delete evolution by passed id
    query = "DELETE FROM pokemon_evolutions WHERE evolv_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/pokemon_evolutions')   

# Pokemon Evolutions Update
@app.route('/update_evolv/<int:id>', methods=['POST', 'GET'])
def update_evolv(id):
    if request.method == "POST":
        if request.form.get("Update_Evolution"):
            evolv_nameInput = request.form["evolv_name"]
            evolv_level = request.form["evolv_level"]

            query = 'UPDATE pokemon_evolutions SET pokemon_evolutions.evolv_name = %s, pokemon_evolutions.evolv_level = %s \
                     WHERE evolv_id = "%s";'
            print(query % (evolv_nameInput, evolv_level, id))
            cur = mysql.connection.cursor()
            cur.execute(query, (evolv_nameInput, evolv_level, id))
            mysql.connection.commit()
            return redirect('/pokemon_evolutions')   

    if request.method == "GET":
        # Two queries executied. query gets values for the gym for update gym form fields.
        query = 'SELECT evolv_id, evolv_name, evolv_level FROM pokemon_evolutions WHERE evolv_id = %s' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        u_evolv_data = cur.fetchall()

        # Query2 gets values for all gyms for page table.
        query2 = 'SELECT evolv_id, evolv_name, evolv_level FROM pokemon_evolutions \
                 ORDER BY evolv_id;'
        cur.execute(query2)
        evolv_data = cur.fetchall()
        return render_template('update_evolutions.j2', u_evolv = u_evolv_data, pEvolvs=evolv_data)             

#------------------------------------------------------------------POKEMON TYPES--------------------------------------------------------------#
# Populate pokemon types table and add new pokemon types
@app.route('/pokemon_types', methods=["POST", "GET"])
def poke_types_page():
    # Contains post request method for adding type.
    if request.method == "POST":
        if request.form.get("Add_Type"):
            type_nameInput = request.form["type_name"]

            query = 'INSERT INTO pokemon_types (type_name) \
                    VALUES ("%s");'
            cur = mysql.connection.cursor()
            cur.execute(query % (type_nameInput))
            mysql.connection.commit()
            return redirect('/pokemon_types')
                
    if request.method == "GET":
        # SQL query and execution to populate table on pokemon_types.html
        query = "SELECT poke_type_id, type_name FROM pokemon_types \
                 ORDER BY poke_type_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        type_data = cur.fetchall()
        return render_template('pokemon_types.html', types=type_data)   

# Pokemon Type Deletion
@app.route('/delete_type/<int:id>')
def delete_type(id):
    # SQL query and execution to delete type by passed id
    query = "DELETE FROM pokemon_types WHERE poke_type_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/pokemon_types')    

# Pokemon Type Update
@app.route('/update_poke_type/<int:id>', methods=['POST', 'GET'])
def update_poke_type(id):
    if request.method == "POST":
        if request.form.get("Update_Poke_Type"):
            type_nameInput = request.form["type_name"]

            query = 'UPDATE pokemon_types SET pokemon_types.type_name = %s \
                     WHERE poke_type_id = "%s";'
            print(query % (type_nameInput, id))
            cur = mysql.connection.cursor()
            cur.execute(query, (type_nameInput, id))
            mysql.connection.commit()
            return redirect('/pokemon_types')   

    if request.method == "GET":
        # Two queries executied. query gets values for the pokemon type for update gym form fields.
        query = 'SELECT poke_type_id, type_name FROM pokemon_types WHERE poke_type_id = %s' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        u_type_data = cur.fetchall()

        # Query2 gets values for all pokemon types for page table.
        query2 = 'SELECT poke_type_id, type_name FROM pokemon_types \
                 ORDER BY poke_type_id;'
        cur.execute(query2)
        type_data = cur.fetchall()
        return render_template('update_evolutions.j2', u_type = u_type_data, types=type_data)                   

#------------------------------------------------------------------MOVE TYPES--------------------------------------------------------------#
# Populate move types table and add new move types
@app.route('/moves_move-types', methods=["POST", "GET"])
def move_types_page():
    # Contains post request method for adding type.
    if request.method == "POST":
        if request.form.get("Add_Move_Type"):
            move_typeNameInput = request.form["move_type_name"]

            query = 'INSERT INTO move_types (move_type_name) \
                    VALUES ("%s");'
            cur = mysql.connection.cursor()
            cur.execute(query % (move_typeNameInput))
            mysql.connection.commit()
            return redirect('/moves_move-types')
                
    if request.method == "GET":
        # SQL query and execution to populate table on pokemon_types.html
        query = "SELECT move_types_id, move_type_name FROM move_types \
                 ORDER BY move_types_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        move_type_data = cur.fetchall()
        return render_template('moves_move-types.html', moveTypes=move_type_data)   

# Pokemon Move Type Deletion
@app.route('/delete_move_type/<int:id>')
def delete_move_type(id):
    # SQL query and execution to delete type by passed id
    query = "DELETE FROM move_types WHERE move_type_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/moves_move-types') 

#------------------------------------------------------------------ABILITIES--------------------------------------------------------------#
# Populate pokemon abilities table and add new pokemon abilities
@app.route('/abilities', methods=["POST", "GET"])
def abilities_page():
    # Contains post request method for adding ability.
    if request.method == "POST":
        if request.form.get("Add_Ability"):
            ability_nameInput = request.form["ability_name"]
            ability_descInput = request.form["ability_desc"]

            query = 'INSERT INTO abilities (abil_name, abil_description) \
                    VALUES ("%s", "%s");'
            cur = mysql.connection.cursor()
            cur.execute(query % (ability_nameInput, ability_descInput))
            mysql.connection.commit()
            return redirect('/abilities')
                
    if request.method == "GET":
        # SQL query and execution to populate table on abilities.html
        query = "SELECT abil_id, abil_name, abil_description FROM abilities \
                 ORDER BY abil_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        abil_data = cur.fetchall()
        return render_template('abilities.html', abilities=abil_data)  

# Pokemon Ability Deletion
@app.route('/delete_ability/<int:id>')
def delete_ability(id):
    # SQL query and execution to delete ability by passed id
    query = "DELETE FROM abilities WHERE abil_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/abilities')         

# Pokemon Ability Update
@app.route('/update_ability/<int:id>', methods=['POST', 'GET'])
def update_ability(id):
    if request.method == "POST":
        if request.form.get("Update_Ability"):
            abil_nameInput = request.form["abil_name"]
            abil_descInput = request.form["abil_desc"]

            query = 'UPDATE abilities SET abilities.abil_name = %s, abilities.abil_description = %s \
                     WHERE abil_id = "%s";'
            print(query % (abil_nameInput, abil_descInput, id))
            cur = mysql.connection.cursor()
            cur.execute(query, (abil_nameInput, abil_descInput, id))
            mysql.connection.commit()
            return redirect('/abilities')   

    if request.method == "GET":
        # Two queries executied. query gets values for the gym for update gym form fields.
        query = 'SELECT abil_id, abil_name, abil_description FROM abilities WHERE abil_id = %s' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        u_abil_data = cur.fetchall()

        # Query2 gets values for all gyms for page table.
        query2 = 'SELECT abil_id, abil_name, abil_description FROM abilities \
                 ORDER BY abil_id;'
        cur.execute(query2)
        abil_data = cur.fetchall()
        return render_template('update_evolutions.j2', u_abil = u_abil_data, abilities=abil_data)       

if __name__ == '__main__':
    app.run(port=31988)