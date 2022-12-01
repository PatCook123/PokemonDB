SELECT first_name, last_name, xp, gyms.gym_name AS gym, pokedecks.pokedeck_name AS pokedeck FROM trainers
LEFT JOIN gyms ON gyms.gym_id = trainers.gyms_gym_id
LEFT JOIN pokedecks ON pokedecks.trainers_trainer_id = trainers.trainer_id
WHERE first_name LIKE '%He%' OR last_name LIKE '%He%'
GROUP BY trainer_id
ORDER BY trainer_id;