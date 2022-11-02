SELECT pokemon_name, height, weight, evolution
FROM pokemon
WHERE pokemon_name LIKE '%c%'
ORDER BY pokemon_name;