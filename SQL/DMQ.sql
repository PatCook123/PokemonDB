-- Data Manipulation Queries for Pokemon DB

-- GYMS
-- Get gyms to populate the gyms dropdown
-- Shows membership figure of each gym
SELECT gym_name, gym_address, gym_zip, gym_city, gym_state, COUNT(trainers.trainer_id) as members FROM gyms
JOIN trainers on trainers.gyms_gym_id = gyms.gym_id
GROUP BY gym_id
ORDER BY gym_name;

-- Get all gym ids for gyms dropdown
SELECT gym_id, gym_name FROM gyms;

-- Add a new gym
INSERT INTO gyms (gym_name, gym_address, gym_zip, gym_city, gym_state) 
VALUES (:gym_nameInput, :gym_addressInput, :gym_zipInput, :gym_cityInput, :gym_stateInput);

-- Update an existing gym
UPDATE gyms SET gym_name = :gym_nameInput, gym_address = :gym_addressInput, gym_zip = :gym_zipInput, gym_city = :gym_cityInput, gym_state = :gym_stateInput
WHERE gym_id = :gym_id_from_update_form;

-- Delete a gym
DELETE FROM gyms WHERE gym_id = :gym_id_from_delete_form;

-- TRAINERS
-- Get trainers to populate the trainers dropdown
-- Shows gym each player belongs to and id of pokedeck owned
SELECT first_name, last_name, xp, gyms.gym_name as gym, pokedecks.pokedeck_id as pokedeck FROM trainers
JOIN gyms on gyms.gym_id = trainers.gyms_gym_id
JOIN pokedecks on pokedecks.trainers_trainer_id = trainers.trainer_id
GROUP BY trainer_id
ORDER BY last_name;

-- Get all trainers for trainers dropdown
SELECT trainer_id, first_name, last_name FROM trainers;

-- Add a new trainer
INSERT INTO trainers (first_name, last_name, xp, gyms_gym_id) 
VALUES (:first_nameInput, :last_nameInput, :xpInput, :gym_id_from_dropdown_input);

-- Update an existing trainer
UPDATE trainers SET first_name = :first_nameInput, last_name = :last_nameInput, xp = :xpInput, gyms_gym_id = :gym_id_from_dropdown_input
WHERE trainer_id = :trainer_id_from_update_form;

-- Delete a trainer
DELETE FROM trainers WHERE trainer_id = :trainer_id_from_delete_form;
