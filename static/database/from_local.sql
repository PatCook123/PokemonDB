SELECT evolv_id, evolv_name FROM `pokemon_evolutions`
WHERE evolv_id NOT IN (SELECT pokemon_evolutions_evolv_id FROM pokemon
WHERE pokemon.pokemon_id = 8);