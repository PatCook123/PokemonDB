-- Data Manipulation Queries for Pokemon DB

-- GYMS
-- Get gyms to populate the gyms table
-- Shows membership figure of each gym
SELECT gym_name, gym_address, gym_zip, gym_city, gym_state, COUNT(trainers.trainer_id) AS members FROM gyms
JOIN trainers ON trainers.gyms_gym_id = gyms.gym_id
GROUP BY gym_id
ORDER BY gym_name;

-- Get all gym ids for gyms dropdown
SELECT gym_id, gym_name FROM gyms
ORDER BY gym_id;

-- Add a new gym
INSERT INTO gyms (gym_name, gym_address, gym_zip, gym_city, gym_state) 
VALUES (:gym_nameInput, :gym_addressInput, :gym_zipInput, :gym_cityInput, :gym_stateInput);

-- Update an existing gym
UPDATE gyms SET gym_name = :gym_nameInput, gym_address = :gym_addressInput, gym_zip = :gym_zipInput, gym_city = :gym_cityInput, gym_state = :gym_stateInput
WHERE gym_id = :gym_id_from_update_form;

-- Delete a gym
DELETE FROM gyms WHERE gym_id = :gym_id_from_delete_form;

-- TRAINERS
-- Get trainers to populate the trainers table
-- Shows gym each player belongs to and id of pokedeck owned
SELECT first_name, last_name, xp, gyms.gym_name AS gym, pokedecks.pokedeck_name AS pokedeck FROM trainers
JOIN gyms ON gyms.gym_id = trainers.gyms_gym_id
JOIN pokedecks ON pokedecks.trainers_trainer_id = trainers.trainer_id
GROUP BY trainer_id
ORDER BY last_name;

-- Get all trainers for trainers dropdown
SELECT trainer_id, first_name, last_name FROM trainers
ORDER BY trainer_id;

-- Search for a trainer by name
SELECT first_name, last_name, xp, gyms.gym_name AS gym, pokedecks.pokedeck_name AS pokedeck FROM trainers
JOIN gyms ON gyms.gym_id = trainers.gyms_gym_id
JOIN pokedecks ON pokedecks.trainers_trainer_id = trainers.trainer_id
WHERE first_name LIKE '%:first_nameInput%'
GROUP BY trainer_id
ORDER BY last_name;

-- Add a new trainer with nullable gym_id
INSERT INTO trainers (first_name, last_name, xp, gyms_gym_id) 
(IF :gym_id_from_dropdown === "None" THEN :gym_id_from_dropdown = NULL)
VALUES (:first_nameInput, :last_nameInput, :xpInput, :gym_id_from_dropdown;

-- Update an existing trainer
UPDATE trainers SET first_name = :first_nameInput, last_name = :last_nameInput, xp = :xpInput, gyms_gym_id = :gym_id_from_dropdown
WHERE trainer_id = :trainer_id_from_update_form;

-- Delete a trainer
DELETE FROM trainers WHERE trainer_id = :trainer_id_from_delete_form;

-- POKEDECKS
-- Get pokedecks to populate the pokedecks table
SELECT pokedeck_name, trainers.first_name AS owner_first_name, trainers.last_name AS owner_last_name, COUNT(pokedecks_have_pokemon.pokemon_pokemon_id) AS cards
FROM pokedecks
JOIN trainers ON pokedecks.trainers_trainer_id = trainers.trainer_id
JOIN pokedecks_have_pokemon ON pokedecks_have_pokemon.pokedecks_pokedeck_id = pokedecks.pokedeck_id
GROUP BY pokedeck_id
ORDER BY pokedeck_name;

-- Add a new pokedeck
INSERT INTO pokedecks (pokedeck_name, trainers_trainer_id)
(IF :trainers_trainer_id_from_dropdown === "None" THEN :trainers_trainer_id_from_dropdown = NULL)
VALUES (:pokedeck_nameInput, :trainers_trainer_id_from_dropdown);

-- Update an existing pokedeck
UPDATE pokedecks SET pokedeck_name = :pokedeck_nameInput, trainers_trainer_id = :trainers_trainer_id_from_dropdown
WHERE pokedeck_id = :pokedeck_id_from_update_form;

-- Delete a pokedeck
DELETE FROM pokedecks WHERE pokedeck_id = :pokedeck_id_from_delete_form;

-- Get all pokedecks dropdown
SELECT pokedeck_id, pokedeck_name FROM pokedecks
ORDER BY pokedeck_id;

-- Display pokedeck's pokemon
-- Using pokedecks_have_pokemon intersect table
SELECT pokedecks.pokedeck_name AS pokedeck_name, pokemon.pokemon_name AS pokdemon_name FROM pokedecks_have_pokemon
JOIN pokedecks ON pokedecks.pokedeck_id = pokedecks_have_pokemon.pokedecks_pokedeck_id
JOIN pokemon ON pokemon.pokemon_id = pokedecks_have_pokemon.pokemon_pokemon_id
ORDER BY pokedeck_name;    

-- Add pokemon to pokedeck
-- Using pokedecks_have_pokemon intersect table
INSERT INTO pokedecks_have_pokemon (pokedecks_pokedeck_id, pokemon_pokemon_id)
VALUES (:pokedeck_id_from_dropdown, :pokemon_id_from_dropdown);

-- Delete a pokemon from pokedeck
-- Using pokedecks_have_pokemon intersect table
DELETE FROM pokedecks_have_pokemon 
WHERE pokedecks_pokedeck_id = :pokedeck_id_from_delete_form AND pokemon_pokemon_id = :pokemon_id_from_delete_form;

-- MOVES
-- Get moves for the move table
SELECT move_name, pp, power, accuracy, move_types.move_type_name AS type FROM moves
JOIN move_types ON move_types_move_types_id = move_types.move_types_id
ORDER BY move_name;

-- Get all moves for move dropdown
SELECT move_id, move_name FROM moves
ORDER BY move_id;

-- Add a move to moves
INSERT INTO moves (move_name, pp, power, accuracy, move_types_move_types_id)
VALUES (:move_nameInput, :ppInput, :powerInput, :accuracyInput, :move_types_id_from_dropdown);

-- Update an existing move
UPDATE moves SET move_name = :move_nameInput, pp = :ppInput, power = :powerInput, accuracy = :accuracyInput, move_types_move_types_id = :move_types_id_from_dropdown
WHERE move_id = :move_id_from_update_form;

-- Delete a move from moves
DELETE FROM moves WHERE move_id = :move_id_from_delete_form;

-- MOVE_TYPES
-- Get move_types for move_types table
SELECT move_type_name FROM move_types
ORDER BY move_types_id;

-- Get all move types for move types dropdown
SELECT move_types_id, move_types_name FROM move_types
ORDER BY move_types_id;

-- Add a move_type to move_types
INSERT INTO move_types (move_type_name)
VALUES (:move_type_nameInput);

-- Update a move_type in move_types
UPDATE move_types SET move_type_name = :move_type_nameInput
WHERE move_types_id = :move_types_id_from_update_form;

-- Delete a move_type
DELETE FROM move_types WHERE move_type_id = :move_type_id_from_delete_form;

-- POKEMON EVOLUTIONS
-- Get pokemon evolutions for the pokemon_evolutions table
SELECT evolv_name, evolv_level FROM pokemon_evolutions
ORDER BY evolv_id;

-- Add a pokemon evolution to pokemon_evolutions
INSERT INTO pokemon_evolutions (evolv_name, evolv_level)
VALUES (:evolv_nameInput, evolv_levelInput);

-- Update an existing pokemon evolution
UPDATE pokemon_evolutions SET evolv_name = :evolv_nameInput, evolv_level = evolv_levelInput
WHERE evolv_id = :evolv_id_from_update_form;

-- Delete a pokemon evolution move from pokemon_evolutions
DELETE FROM pokemon_evolutions WHERE evolv_id = :evolv_id_from_delete_form;

-- POKEMON_TYPES
-- Get pokemon_types for pokemon_types table
SELECT type_name FROM pokemon_types
ORDER BY poke_type_id;

-- Add a poke_type to poke_types
INSERT INTO poke_types (type_name)
VALUES (:type_nameInput);

-- Update a poke_type in poke_type
UPDATE poke_type SET type_name = :type_nameInput
WHERE poke_type_id = :poke_type_id_from_update_form;

-- Delete a move_type
DELETE FROM poke_types WHERE poke_type_id = :poke_type_id_from_delete_form;

-- ABILTIES
-- Get abilities for the abilities table
SELECT abili_name, abili_description FROM abilities
ORDER BY abili_id;

-- Add an ability to abilities
INSERT INTO abilities (abili_name, abili_description)
VALUES (:abili_nameInput, :abili_descriptionInput);

-- Update an existing ability
UPDATE abilities SET abili_name = :abili_nameInput, abili_description = :abili_descriptionInput
WHERE abili_id = :abili_id_from_update_form;

-- Delete an ability move from ability
DELETE FROM abilities WHERE abili_id = :abili_id_from_delete_form;

-- POKEMON
-- Get pokemon to populate the pokemon table
SELECT pokemon_name, height, weight, evolution
FROM pokemon
ORDER BY pokemon_name;

SELECT move_name, pp, power, accuracy, move_types.move_type_name AS type FROM moves
JOIN move_types ON move_types_move_types_id = move_types.move_types_id
ORDER BY move_name;

-- Search for a pokemon by name
SELECT pokemon_name, height, weight, evolution
FROM pokemon
WHERE pokemon_name LIKE '%:pokemon_nameInput%'
ORDER BY pokemon_name;

-- Add a new pokemon
INSERT INTO pokemon (pokemon_name, height, weight, evolution, pokemon_evolutions_evolv_id)
VALUES (:pokemon_nameInput, :heightInput, :weightInput, :evolutionInput, pokemon_evolutions_evolv_id_from_dropdown);

-- Update an existing pokemon
UPDATE pokemon SET pokemon_name = :pokemon_nameInput, height = :heightInput, weight = :weightInput, evolution = :evolutionInput, pokemon_evolutions_evolv_id = :pokemon_evolutions_evolv_id_from_dropdown
WHERE pokemon_id = :pokemon_id_from_update_form;

-- Delete a pokemon
DELETE FROM pokemon WHERE pokemon_id = :pokemon_id_from_delete_form;

-- Get all pokemon dropdown
SELECT pokemon_id, pokemon_name FROM pokemon
ORDER BY pokemon_id;

-- Display pokemon's moves
-- Using pokemon_has_moves intersect table  
SELECT pokemon.pokemon_name AS pokemon_name, moves.move_name AS move_name FROM pokemon_has_moves
JOIN pokemon ON pokemon.pokemon_id = pokemon_has_moves.pokemon_pokemon_id
JOIN moves ON moves.move_id = pokemon_has_moves.moves_move_id
ORDER BY pokemon_name; 

-- Add move to pokemon
-- Using pokemon_has_moves intersect table
INSERT INTO pokemon_has_moves (pokemon_pokemon_id, moves_move_id)
VALUES (:pokemon_id_from_dropdown, :moves_move_id_from_dropdown);

-- Delete a move from pokemon
-- Using pokemon_has_moves intersect table
DELETE FROM pokemon_has_moves
WHERE pokemon_pokemon_id = :pokemon_id_from_delete_form AND moves_move_id = :move_id_from_delete_form;

-- Display pokemon's abilities
-- Using pokemon_has_abilities intersect table
SELECT pokemon.pokemon_name AS pokemon_name, abilities.abil_name AS abil_name FROM pokemon_has_abilities
JOIN pokemon ON pokemon.pokemon_id = pokemon_has_abilities.pokemon_pokemon_id
JOIN abilties ON abilities.abil_id = pokemon_has_abilities.abilties_abil_id
ORDER BY pokemon_name; 

-- Add ability to pokemon
-- Using pokemon_has_abilities intersect table
INSERT INTO pokemon_has_abilities (pokemon_pokemon_id, abilities_abil_id)
VALUES (:pokemon_id_from_dropdown, :abilities_abil_id_from_dropdown);

-- Delete an ability from pokemon
-- Using pokemon_has_abilities intersect table
DELETE FROM pokemon_has_abilities 
WHERE pokemon_pokemon_id = :pokemon_id_from_delete_form AND abilities_abil_id = :abilities_abil_id_from_delete_form;

-- Display pokemon's type
-- Using pokemon_has_pokemon_types intersect table
SELECT pokemon.pokemon_name AS pokemon_name, pokemon_types.type_name AS type_name FROM pokemon_has_pokemon_types
JOIN pokemon ON pokemon.pokemon_id = pokemon_has_pokemon_types.pokemon_pokemon_id
JOIN pokemon_types ON pokemon_types.poke_type_id = pokemon_has_pokemon_types.pokemon_types.poke_type_id;
ORDER BY pokemon_name; 

-- Add type to pokemon
-- Using pokemon_has_pokemon_types intersect table
INSERT INTO pokemon_has_pokemon_types (pokemon_pokemon_id, pokemon_types_poke_type_id)
VALUES (:pokemon_id_from_dropdown, :pokemon_type_id_from_dropdown);

-- Delete an type from pokemon
-- Using pokedecks_have_pokemon intersect table
DELETE FROM pokemon_has_pokemon_types 
WHERE pokemon_pokemon_id = :pokemon_id_from_delete_form AND pokemon_types_poke_type_id = :pokemon_type_id_from_delete_form;
