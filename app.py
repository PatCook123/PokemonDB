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

#------------------------------------------------------------------POKEDECKS-------------------------------------------------------------------#
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

        return render_template("search_pokedeck.j2", pokedecks=pokedecks_data, pdropdown=pokedecks_data, trainers=trainers_data)

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

@app.route('/add_poke_to_pokedeck/<int:id>', methods=['POST', 'GET'])
def add_poke_to_pokedeck(id):
    if request.method == 'POST':
        if request.form.get("addPokeToDeck"):
            pokemon_dropdownInput = request.form["pokemon_dropdownInput"]
            
            query = 'INSERT INTO pokedecks_have_pokemon (pokedecks_pokedeck_id, pokemon_pokemon_id) VALUES ("%s", "%s");'
            cur = mysql.connection.cursor()
            cur.execute(query % (id, pokemon_dropdownInput))
            mysql.connection.commit()
            return redirect(f'/add_poke_to_pokedeck/{id}')

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

        query3 = 'SELECT pokedecks.pokedeck_name AS pokedeck_name, pokedecks.pokedeck_id as pokedeck_id, pokemon.pokemon_name AS pokemon_name,\
        pokemon.pokemon_id AS pokemon_id\
        FROM pokedecks_have_pokemon\
        LEFT JOIN pokedecks ON pokedecks.pokedeck_id = pokedecks_have_pokemon.pokedecks_pokedeck_id\
        LEFT JOIN pokemon ON pokemon.pokemon_id = pokedecks_have_pokemon.pokemon_pokemon_id\
        WHERE pokedecks.pokedeck_id = %s;'
        cur.execute(query3 % (id))
        at_pokedeck_data = cur.fetchall()

        query4 = f'SELECT pokemon_id, pokemon_name FROM pokemon WHERE pokemon_id NOT IN\
        (SELECT pokemon_pokemon_id FROM pokedecks_have_pokemon WHERE pokedecks_have_pokemon.pokedecks_pokedeck_id = {id});'
        cur.execute(query4)
        pokemon_data = cur.fetchall()

        query5 = f'SELECT pokedeck_name FROM pokedecks WHERE pokedecks.pokedeck_id = {id};'
        cur.execute(query5)
        deck_name = cur.fetchall()

        return render_template("add_poke_to_pokedeck.j2", pokedecks=pokedecks_data, pdropdown=pokedecks_data, trainers=trainers_data, atpokedeck=at_pokedeck_data, pokemon=pokemon_data, deck_name=deck_name, deck_id=id)

@app.route('/delete_poke_from_pokedeck/<int:deckid>/<int:pokeid>')
def delete_poke_from_pokedeck(deckid, pokeid):
    query = 'DELETE FROM pokedecks_have_pokemon\
    WHERE pokedecks_pokedeck_id = %s AND pokemon_pokemon_id = %s;'
    cur = mysql.connection.cursor()
    cur.execute(query % (deckid, pokeid))
    mysql.connection.commit()
    return redirect(f'/add_poke_to_pokedeck/{deckid}')


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
        return render_template('pokemon_details.j2', pokemon=pokemon_data)  

# Pokemon Deletion
@app.route('/delete_pokemon/<int:id>')
def delete_pokemon(id):
    # SQL query and execution to delete evolution by passed id
    query = "DELETE FROM pokemon WHERE pokemon_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/pokemon')          

# Pokemon Update
@app.route('/update_pokemon/<int:id>', methods=['POST', 'GET'])
def update_pokemon(id):
    if request.method == "POST":
        if request.form.get("Update_Pokemon"):
            pokemon_nameInput = request.form["poke_name"]
            pokemon_heightInput = request.form["poke_height"]
            pokemon_weightInput = request.form["poke_weight"]
            pokemon_evoInput = request.form["hasEvolution"]

            query = 'UPDATE pokemon SET pokemon.pokemon_name = %s, pokemon.height = %s, pokemon.weight = %s, pokemon.evolution = %s \
                     WHERE pokemon_id = "%s";'
            cur = mysql.connection.cursor()
            cur.execute(query, (pokemon_nameInput, pokemon_heightInput, pokemon_weightInput, pokemon_evoInput, id))
            mysql.connection.commit()
            return redirect('/pokemon')   

    if request.method == "GET":
        # Two queries executied. query gets values for the gym for update gym form fields.
        query = 'SELECT pokemon_id, pokemon_name, height, weight, evolution FROM pokemon WHERE pokemon_id = %s' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        u_pokemon_data = cur.fetchall()

        # Query2 gets values for all gyms for page table.
        query2 = 'SELECT pokemon_id, pokemon_name, height, weight, evolution FROM pokemon \
                 ORDER BY pokemon_id;'
        cur.execute(query2)
        pokeman_data = cur.fetchall()
        return render_template('update_evolutions.j2', u_poke = u_pokemon_data, pokemon=pokeman_data)   

@app.route('/manage_poke_abilities', methods=["POST", "GET"])
def manage_abil_page():
    # Contains post request method for adding evolution.
    if request.method == "POST":
        if request.form.get("Manage_Abilities"):
            poke_idInput = request.form["pokemon_dropdownInput"]

        print(poke_idInput)

        query = 'SELECT pokemon_id, pokemon_name, height, weight, evolution FROM pokemon ORDER BY pokemon_id;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pokemon_data = cur.fetchall()

        query2 = f'SELECT pokemon.pokemon_id as pokemon_id, pokemon.pokemon_name as pokemon_name, abilities.abil_id as abil_id,\
                abilities.abil_name AS abil_name, abilities.abil_description as abil_description FROM pokemon_has_abilities\
                JOIN pokemon ON pokemon.pokemon_id = pokemon_has_abilities.pokemon_pokemon_id\
                JOIN abilities ON abilities.abil_id = pokemon_has_abilities.abilities_abil_id\
                WHERE pokemon_id = {poke_idInput}\
                ORDER BY pokemon_name;'
        cur.execute(query2)
        pokemon_abil_data = cur.fetchall()

        query3 = f'SELECT abil_id, abil_name, abil_description FROM `abilities`\
        WHERE abil_id NOT IN (select abilities_abil_id from pokemon_has_abilities\
        WHERE pokemon_has_abilities.pokemon_pokemon_id = {poke_idInput});'
        cur.execute(query3)
        abil_data = cur.fetchall()

        return render_template('manage_poke_abilities.j2', pokemon=pokemon_data, mapokemon=pokemon_abil_data, abilities=abil_data, poke_id=poke_idInput)   


@app.route('/add_abil_to_pokemon/<int:id>', methods=['POST'])
def add_abil_to_pokemon(id):
    if request.method == 'POST':
        if request.form.get("addAbilToPoke"):
            ability_dropdownInput = request.form["ability_dropdownInput"]
            
            query = 'INSERT INTO pokemon_has_abilities (pokemon_pokemon_id, abilities_abil_id) VALUES (%s, %s);'
            cur = mysql.connection.cursor()
            cur.execute(query % (id, ability_dropdownInput))
            mysql.connection.commit()
            return redirect('/pokemon')

@app.route('/delete_abil_from_pokemon/<int:pokeid>/<int:abilid>')
def delete_abil_from_pokemon(pokeid, abilid):
    query = 'DELETE FROM pokemon_has_abilities\
    WHERE pokemon_pokemon_id = %s AND abilities_abil_id = %s;'
    cur = mysql.connection.cursor()
    cur.execute(query % (pokeid, abilid))
    mysql.connection.commit()
    return redirect('/pokemon')

@app.route('/manage_poke_moves', methods=["POST", "GET"])
def manage_move_page():
    # Contains post request method for adding evolution.
    if request.method == "POST":
        if request.form.get("Manage_Moves"):
            poke_idInput = request.form["pokemon_dropdownInput"]

        print(poke_idInput)

        query = 'SELECT pokemon_id, pokemon_name, height, weight, evolution FROM pokemon ORDER BY pokemon_id;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pokemon_data = cur.fetchall()

        query2 = f'SELECT pokemon.pokemon_id as pokemon_id, pokemon.pokemon_name as pokemon_name, moves.move_id as move_id,\
                moves.move_name AS move_name, moves.pp as pp, moves.power as power FROM pokemon_has_moves\
                JOIN pokemon ON pokemon.pokemon_id = pokemon_has_moves.pokemon_pokemon_id\
                JOIN moves ON moves.move_id = pokemon_has_moves.moves_move_id\
                WHERE pokemon_id = {poke_idInput}\
                ORDER BY pokemon_name;'
        cur.execute(query2)
        pokemon_move_data = cur.fetchall()

        query3 = f'SELECT move_id, move_name, pp, power FROM `moves`\
        WHERE move_id NOT IN (select moves_move_id from pokemon_has_moves\
        WHERE pokemon_has_moves.pokemon_pokemon_id = {poke_idInput});'
        cur.execute(query3)
        move_data = cur.fetchall()

        return render_template('manage_poke_moves.j2', pokemon=pokemon_data, mmpokemon=pokemon_move_data, moves=move_data, poke_id=poke_idInput)   


@app.route('/add_move_to_pokemon/<int:id>', methods=['POST'])
def add_move_to_pokemon(id):
    if request.method == 'POST':
        if request.form.get("addMoveToPoke"):
            move_dropdownInput = request.form["move_dropdownInput"]
            
            query = 'INSERT INTO pokemon_has_moves (pokemon_pokemon_id, moves_move_id) VALUES (%s, %s);'
            cur = mysql.connection.cursor()
            cur.execute(query % (id, move_dropdownInput))
            mysql.connection.commit()
            return redirect('/pokemon')

@app.route('/delete_move_from_pokemon/<int:pokeid>/<int:moveid>')
def delete_move_from_pokemon(pokeid, moveid):
    query = 'DELETE FROM pokemon_has_moves\
    WHERE pokemon_pokemon_id = %s AND moves_move_id = %s;'
    cur = mysql.connection.cursor()
    cur.execute(query % (pokeid, moveid))
    mysql.connection.commit()
    return redirect('/pokemon')    

@app.route('/manage_poke_type', methods=["POST", "GET"])
def manage_type_page():
    # Contains post request method for adding evolution.
    if request.method == "POST":
        if request.form.get("Manage_Type"):
            poke_idInput = request.form["pokemon_dropdownInput"]

        print(poke_idInput)

        query = 'SELECT pokemon_id, pokemon_name, height, weight, evolution FROM pokemon ORDER BY pokemon_id;'
        cur = mysql.connection.cursor()
        cur.execute(query)
        pokemon_data = cur.fetchall()

        query2 = f'SELECT pokemon.pokemon_id as pokemon_id, pokemon.pokemon_name as pokemon_name, pokemon_types.poke_type_id as poke_type_id,\
                pokemon_types.type_name AS type_name FROM pokemon_has_pokemon_types\
                JOIN pokemon ON pokemon.pokemon_id = pokemon_has_pokemon_types.pokemon_pokemon_id\
                JOIN pokemon_types ON pokemon_types.poke_type_id = pokemon_has_pokemon_types.pokemon_types_poke_type_id\
                WHERE pokemon_id = {poke_idInput}\
                ORDER BY pokemon_name;'
        cur.execute(query2)
        pokemon_type_data = cur.fetchall()

        query3 = f'SELECT poke_type_id, type_name FROM `pokemon_types`\
        WHERE poke_type_id NOT IN (select pokemon_types_poke_type_id from pokemon_has_pokemon_types\
        WHERE pokemon_has_pokemon_types.pokemon_pokemon_id = {poke_idInput});'
        cur.execute(query3)
        type_data = cur.fetchall()

        return render_template('manage_poke_type.j2', pokemon=pokemon_data, mtpokemon=pokemon_type_data, types=type_data, poke_id=poke_idInput)   


@app.route('/add_type_to_pokemon/<int:id>', methods=['POST'])
def add_type_to_pokemon(id):
    if request.method == 'POST':
        if request.form.get("addTypeToPoke"):
            type_dropdownInput = request.form["type_dropdownInput"]
            
            query = 'INSERT INTO pokemon_has_pokemon_types (pokemon_pokemon_id, pokemon_types_poke_type_id) VALUES (%s, %s);'
            cur = mysql.connection.cursor()
            cur.execute(query % (id, type_dropdownInput))
            mysql.connection.commit()
            return redirect('/pokemon')

@app.route('/delete_type_from_pokemon/<int:pokeid>/<int:typeid>')
def delete_type_from_pokemon(pokeid, typeid):
    query = 'DELETE FROM pokemon_has_pokemon_types\
    WHERE pokemon_pokemon_id = %s AND pokemon_types_poke_type_id = %s;'
    cur = mysql.connection.cursor()
    cur.execute(query % (pokeid, typeid))
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
        return render_template('update_poke_type.j2', u_type = u_type_data, types=type_data)                   

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
    query = "DELETE FROM move_types WHERE move_types_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()
    return redirect('/moves_move-types')

# Pokemon Move Type Update
@app.route('/update_move_type/<int:id>', methods=['POST', 'GET'])
def update_move_type(id):
    if request.method == "POST":
        if request.form.get("Update_Move_Type"):
            movet_nameInput = request.form["move_type_name"]

            query = 'UPDATE move_types SET move_types.move_type_name = %s \
                     WHERE move_types_id = "%s";'
            print(query % (movet_nameInput, id))
            cur = mysql.connection.cursor()
            cur.execute(query, (movet_nameInput, id))
            mysql.connection.commit()
            return redirect('/moves_move-types')   

    if request.method == "GET":
        # Two queries executied. query gets values for the gym for update gym form fields.
        query = 'SELECT move_types_id, move_type_name FROM move_types WHERE move_types_id = %s' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        u_mtype_data = cur.fetchall()

        # Query2 gets values for all gyms for page table.
        query2 = 'SELECT move_types_id, move_type_name FROM move_types \
                 ORDER BY move_types_id;'
        cur.execute(query2)
        move_type_data = cur.fetchall()
        return render_template('update_move_types.j2', u_mtype = u_mtype_data, moveTypes=move_type_data)     

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
        return render_template('update_abilities.j2', u_abil = u_abil_data, abilities=abil_data)       

if __name__ == '__main__':
    app.run(port=31988)