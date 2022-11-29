SELECT move_types.move_type_name as type FROM moves
JOIN move_types ON move_types_move_types_id = move_types.move_types_id
WHERE move_types_move_types_id NOT IN (SELECT move_types.move_types_id as type FROM moves
JOIN move_types ON moves.move_types_move_types_id = move_types.move_types_id
WHERE move_id = 2)