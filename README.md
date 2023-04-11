# cs340_pokemondb Group 89 - Patrick Cook & Cheyenne Plutchak

The implementation of a SQL RDBMS managed via a CRUD app. Our group was ambitious in it's aim to build an RDMBS which would service a fictional Pokemon club. We implemented 13 tables representing 9 entity-types which included 4 N:M relationships that each required an intersection table. 

Within this repo are a DDL and DML file which showcase the database's structure and operations. Additionally, app.py showcases the backend operations, written in python, which service the HTML and Jinja files which comprise the UI.

# Overview:

Members of the Oregon Backwoods Pokémon Community are constantly trading, finding, training, and evolving their pokémon and currently track all changes via personal notebooks. During monthly gym meetings, members update a large poster board with all of the previous month’s changes to member’s pokedecks and respective pokémon. Issues often arise when personal notebooks contain differing information of which pokémon were traded between which trainers and annual Gym Reports detailing member’s pokedecks have become plagued with inaccuracies and are increasingly tedious to compile. In an effort to modernize the community and reduce time spent on data correction and report compilation, a database project has been commissioned. 

The Oregon Backwoods Pokemon Community is home to upwards of 60 members, or Trainers, each with their own pokedeck, belonging to one of 6 Pokémon Gyms. A database website will record Trainers who belong to Gyms, each possessing a pokedeck containing a set of pokémon. Each pokémon has specific characteristics and is of one pokémon type. Additionally, each pokémon is capable of one or more Moves and Evolutions, and possesses one or more abilities. Each Move belongs to one move_types. There are in excess of 151 pokémon in the known world which can belong to many pokedecks. 

# Tables:

gyms: Contains information about each pokémon gym.
gym_id: INT(11), auto_increment, unique, not NULL, PK
gym_name: VARCHAR(45), unique, not NULL
gym_address: VARCHAR(100), unique
gym_zip: INT (11)
gym_city: VARCHAR(45)
gym_state: VARCHAR(2)
Relationship: 1:M relationship with trainers with gym_id as FK inside trainers.

trainers: Contains information on each pokémon trainer.
trainer_id: INT (11), auto_increment, unique, not NULL, PK
first_name: VARCHAR(45), not NULL
last_name: VARCHAR(45)
xp: INT(10), not NULL, unsigned, default: 0
gyms_gym_id: INT(11), FK
Relationship: M:1 relationship with gyms by way of gym_leader_id as FK and 1:M relationship with pokedecks by way of trainers_trainer_id as FK in pokedecks.

pokedecks: Contains each pokedeck’s name and owner.
pokedeck_id: INT, auto_increment, unique, not NULL, PK
pokedeck_name: VARCHAR(45), unique, not NULL
trainers_trainer_id: INT,  FK
Relationship: M:1 relationship with trainers by way of trainers_trainer_id as FK. M:M relationship with Pokémon with pokedeck_id and poke_id as FKs in intersection table (pokedeck_poke_id as FK of intersection table).

moves: Contains information about possible moves for pokémon to possess. 
move_id: INT(11), auto_increment, unique, not NULL, PK
move_name: VARCHAR(45), not NULL, Unique
pp: INT(10), unsigned, not NULL
power: INT(10), unsigned
accuracy: DECIMAL(5, 2), unsigned
move_type: movetypes_move_type_id, INT(11), not NULL, FK
Relationship: M:M relationship with pokémon with move_id and poke_id as FKs in intersection table (poke_moves_id being FK of intersection table) and M:1 relationship with move_type by way of move_type_id as FK.

move_types: Contains all types of pokémon moves. 
move_type_id: INT(11), auto_increment, unique, not NULL, PK
move_type_name: VARCHAR(16), unique, not NULL
Relationship: 1:M relationship with moves by way of move_type_id as FK in moves.

pokemon: Contains information about each base pokémon, not including evolutions.
pokemon_id INT(11), Unique, not NULL, PK
pokemon_name VARCHAR(12), not NULL, Unique
height INT(10), not NULL
weight INT(10), not NULL
evolution BOOL (TINYINT(2), not NULL
pokemon_evolutions_pokemon_evolv_id INT(11), FK
Relationship: 1:M relationship with pokémon and pokémon evolutions with poke_id as FK inside pokémon evolutions. M:M relationship with pokemon moves via pokemon_has_moves intersection table. M:M relationship with abilities via pokemon_has_abilities intersection table. M:M relationship with pokedeck via pokedeck_has_pokemon. M:M relationship with pokemon_types via pokemon_has_pokemon_types.

pokemon_evolutions: Contains the evolutions specific to each pokémon.
evolv_id INT(11), autoincrement, Unique, not NULL, PK
evolv_name VARCHAR(16), Unique, Not NULL
evolv_level INT(10), not NULL
Relationship: 1:M relationship with pokémon and pokémon evolutions with poke_id as FK inside pokémon_evolutions. Ex: Bulbarsar has two evolutions, Ivysaur and Venusaur, but those two evolutions will only ever have Bulbasaur as their base pokémon.

pokemon_types: Contains the pokémon types associated with each pokémon.
poke_type_id INT(11), autoincrement, Unique, not NULL, PK
type_name VARCHAR(16) Unique, not NULL
Relationship: M:M relationship with pokémon via pokemon_has_pokemon_types intersection table.

abilities: Contains the pokémon abilities.
abil_id INT(11), Unique, not NULL, PK
abli_name VARCHAR(24), Unique, not NULL
abil_description VARCHAR(81), not NULL
Relationship: M:M relationship with pokémon and pokémon_types with poke_id and abil_id as FK.

# Schema
<img width="563" alt="Screen Shot 2023-01-03 at 1 47 25 PM" src="https://user-images.githubusercontent.com/76977450/210430378-825a8c69-e0de-43fb-b102-263925099a6e.png">

# ERD
<img width="554" alt="Screen Shot 2023-01-03 at 1 47 35 PM" src="https://user-images.githubusercontent.com/76977450/210430389-7d3cd9ca-c88e-4118-8277-5be48759dd77.png">





