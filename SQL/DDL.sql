SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS gyms;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS pokedecks;
DROP TABLE IF EXISTS pokedecks_have_pokemon;
DROP TABLE IF EXISTS pokemon;
DROP TABLE IF EXISTS abilities;
DROP TABLE IF EXISTS pokemon_has_abilities;
DROP TABLE IF EXISTS moves;
DROP TABLE IF EXISTS move_types;
DROP TABLE IF EXISTS pokemon_has_moves;
DROP TABLE IF EXISTS pokemon_types;
DROP TABLE IF EXISTS pokemon_has_pokemon_types;
DROP TABLE IF EXISTS pokemon_evolutions;


-- -----------------------------------------------------
-- Table `gyms`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `gyms` (
  `gym_id` INT NOT NULL AUTO_INCREMENT,
  `gym_name` VARCHAR(45) NOT NULL,
  `gym_address` VARCHAR(100),
  `gym_zip` INT,
  `gym_city` VARCHAR(45),
  `gym_state` VARCHAR(2),
  PRIMARY KEY (`gym_id`),
  UNIQUE INDEX `gym_id_UNIQUE` (`gym_id` ASC) VISIBLE,
  UNIQUE INDEX `gym_name_UNIQUE` (`gym_name` ASC) VISIBLE,
  UNIQUE INDEX `gym_address_UNIQUE` (`gym_address` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokedecks`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokedecks` (
  `pokedeck_id` INT NOT NULL AUTO_INCREMENT,
  `pokedeck_name` VARCHAR(45) NOT NULL,
  `trainers_trainer_id` INT NULL,
  PRIMARY KEY (`pokedeck_id`),
  UNIQUE INDEX `pokedeck_id_UNIQUE` (`pokedeck_id` ASC) VISIBLE,
  UNIQUE INDEX `pokedeck_name_UNIQUE` (`pokedeck_name` ASC) VISIBLE,
  INDEX `fk_pokedecks_trainers1_idx` (`trainers_trainer_id` ASC) VISIBLE,
  CONSTRAINT `fk_pokedecks_trainers1`
    FOREIGN KEY (`trainers_trainer_id`)
    REFERENCES `trainers` (`trainer_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;



-- -----------------------------------------------------
-- Table `trainers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `trainers` (
  `trainer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NULL,
  `xp` INT UNSIGNED NOT NULL DEFAULT 0,
  `gyms_gym_id` INT NULL,
  PRIMARY KEY (`trainer_id`),
  UNIQUE INDEX `trainer_id_UNIQUE` (`trainer_id` ASC) VISIBLE,
  INDEX `fk_trainers_gyms_idx` (`gyms_gym_id` ASC) VISIBLE,
  CONSTRAINT `fk_trainers_gyms`
    FOREIGN KEY (`gyms_gym_id`)
    REFERENCES `gyms` (`gym_id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokemon_evolutions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokemon_evolutions` (
  `evolv_id` INT NOT NULL AUTO_INCREMENT,
  `evolv_level` INT UNSIGNED NOT NULL,
  `evolv_name` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`evolv_id`),
  UNIQUE INDEX `evolv_id INT_UNIQUE` (`evolv_id` ASC) VISIBLE,
  UNIQUE INDEX `evolv_name_UNIQUE` (`evolv_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokemon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokemon` (
  `pokemon_id` INT NOT NULL AUTO_INCREMENT,
  `pokemon_name` VARCHAR(12) NOT NULL,
  `height` INT UNSIGNED NOT NULL,
  `weight` INT UNSIGNED NOT NULL,
  `evolution` TINYINT(2) NOT NULL DEFAULT 1,
  `pokemon_evolutions_evolv_id` INT NULL,
  PRIMARY KEY (`pokemon_id`),
  UNIQUE INDEX `pokemon_id_UNIQUE` (`pokemon_id` ASC) VISIBLE,
  INDEX `fk_pokemon_pokemon_evolutions1_idx` (`pokemon_evolutions_evolv_id` ASC) VISIBLE,
  CONSTRAINT `fk_pokemon_pokemon_evolutions1`
    FOREIGN KEY (`pokemon_evolutions_evolv_id`)
    REFERENCES `pokemon_evolutions` (`evolv_id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `move_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `move_types` (
  `move_types_id` INT NOT NULL AUTO_INCREMENT,
  `move_type_name` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`move_types_id`),
  UNIQUE INDEX `move_types_id_UNIQUE` (`move_types_id` ASC) VISIBLE,
  UNIQUE INDEX `move_type_name_UNIQUE` (`move_type_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `moves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `moves` (
  `move_id` INT NOT NULL AUTO_INCREMENT,
  `move_name` VARCHAR(45) NOT NULL,
  `pp` INT UNSIGNED NOT NULL,
  `power` INT UNSIGNED NULL,
  `accuracy` DECIMAL(5,2) UNSIGNED NULL,
  `move_types_move_types_id` INT NOT NULL,
  PRIMARY KEY (`move_id`),
  UNIQUE INDEX `move_id_UNIQUE` (`move_id` ASC) VISIBLE,
  UNIQUE INDEX `move_name_UNIQUE` (`move_name` ASC) VISIBLE,
  INDEX `fk_moves_move_types1_idx` (`move_types_move_types_id` ASC) VISIBLE,
  CONSTRAINT `fk_moves_move_types1`
    FOREIGN KEY (`move_types_move_types_id`)
    REFERENCES `move_types` (`move_types_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokemon_has_moves`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokemon_has_moves` (
  `pokemon_pokemon_id` INT NOT NULL,
  `moves_move_id` INT NOT NULL,
  PRIMARY KEY (`pokemon_pokemon_id`, `moves_move_id`),
  INDEX `fk_pokemon_has_moves_moves1_idx` (`moves_move_id` ASC) VISIBLE,
  INDEX `fk_pokemon_has_moves_pokemon1_idx` (`pokemon_pokemon_id` ASC) VISIBLE,
  CONSTRAINT `fk_pokemon_has_moves_pokemon1`
    FOREIGN KEY (`pokemon_pokemon_id`)
    REFERENCES `pokemon` (`pokemon_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pokemon_has_moves_moves1`
    FOREIGN KEY (`moves_move_id`)
    REFERENCES `moves` (`move_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokemon_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokemon_types` (
  `poke_type_id` INT NOT NULL AUTO_INCREMENT,
  `type_name` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`poke_type_id`),
  UNIQUE INDEX `poke_type_id_UNIQUE` (`poke_type_id` ASC) VISIBLE,
  UNIQUE INDEX `type_name_UNIQUE` (`type_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokemon_has_pokemon_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokemon_has_pokemon_types` (
  `pokemon_pokemon_id` INT NOT NULL,
  `pokemon_types_poke_type_id` INT NOT NULL,
  PRIMARY KEY (`pokemon_pokemon_id`, `pokemon_types_poke_type_id`),
  INDEX `fk_pokemon_has_pokemon_types_pokemon_types1_idx` (`pokemon_types_poke_type_id` ASC) VISIBLE,
  INDEX `fk_pokemon_has_pokemon_types_pokemon1_idx` (`pokemon_pokemon_id` ASC) VISIBLE,
  CONSTRAINT `fk_pokemon_has_pokemon_types_pokemon1`
    FOREIGN KEY (`pokemon_pokemon_id`)
    REFERENCES `pokemon` (`pokemon_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pokemon_has_pokemon_types_pokemon_types1`
    FOREIGN KEY (`pokemon_types_poke_type_id`)
    REFERENCES `pokemon_types` (`poke_type_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokedecks_have_pokemon`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokedecks_have_pokemon` (
  `pokedecks_pokedeck_id` INT NOT NULL,
  `pokemon_pokemon_id` INT NOT NULL,
  PRIMARY KEY (`pokedecks_pokedeck_id`, `pokemon_pokemon_id`),
  INDEX `fk_pokedeck_has_pokemon_pokemon1_idx` (`pokemon_pokemon_id` ASC) VISIBLE,
  INDEX `fk_pokedeck_has_pokemon_pokedeck1_idx` (`pokedecks_pokedeck_id` ASC) VISIBLE,
  CONSTRAINT `fk_pokedeck_has_pokemon_pokedeck1`
    FOREIGN KEY (`pokedecks_pokedeck_id`)
    REFERENCES `pokedecks` (`pokedeck_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pokedeck_has_pokemon_pokemon1`
    FOREIGN KEY (`pokemon_pokemon_id`)
    REFERENCES `pokemon` (`pokemon_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `abilities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `abilities` (
  `abil_id` INT NOT NULL AUTO_INCREMENT,
  `abil_name` VARCHAR(24) NOT NULL,
  `abil_description` VARCHAR(81) NOT NULL,
  PRIMARY KEY (`abil_id`),
  UNIQUE INDEX `abil_id_UNIQUE` (`abil_id` ASC) VISIBLE,
  UNIQUE INDEX `abil_name_UNIQUE` (`abil_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pokemon_has_abilities`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pokemon_has_abilities` (
  `pokemon_pokemon_id` INT NOT NULL,
  `abilities_abil_id` INT NOT NULL,
  PRIMARY KEY (`pokemon_pokemon_id`, `abilities_abil_id`),
  INDEX `fk_pokemon_has_abilities_abilities1_idx` (`abilities_abil_id` ASC) VISIBLE,
  INDEX `fk_pokemon_has_abilities_pokemon1_idx` (`pokemon_pokemon_id` ASC) VISIBLE,
  CONSTRAINT `fk_pokemon_has_abilities_pokemon1`
    FOREIGN KEY (`pokemon_pokemon_id`)
    REFERENCES `pokemon` (`pokemon_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_pokemon_has_abilities_abilities1`
    FOREIGN KEY (`abilities_abil_id`)
    REFERENCES `abilities` (`abil_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


/*pokemon_evolutions table data*/
INSERT INTO pokemon_evolutions (
    evolv_level,
    evolv_name
) 
VALUES
(
    16,
    "Ivysaur"
),
(
    32,
    "Venusaur"
),
(
    16,
    "Charmeleon"
),
(
    36,
    "Charizard"
),
(
    16,
    "Wartortle"
),
(
    36,
    "Blastoise"
);


/*pokemon table data*/
INSERT INTO pokemon (
    pokemon_name,
    height,
    weight,
    evolution,
    pokemon_evolutions_evolv_id
) 
VALUES
(
    "Bulbasaur",
    2,
    15,
    1,
    (SELECT evolv_id FROM pokemon_evolutions
    WHERE pokemon_evolutions.evolv_name = "Ivysaur")
),
(
    "Ivysaur",
    3,
    29,
    1,
    (SELECT evolv_id FROM pokemon_evolutions
    WHERE pokemon_evolutions.evolv_name = "Venusaur")
),
(
    "Venusaur",
    6,
    221,
    0,
    (SELECT evolv_id FROM pokemon_evolutions
    WHERE pokemon_evolutions.evolv_name = "Venusaur")
),
(
    "Charmander",
    2,
    19,
    1,
    (SELECT evolv_id FROM pokemon_evolutions
    WHERE pokemon_evolutions.evolv_name = "Charmeleon")
),
(
    "Charmeleon",
    3,
    42,
    1,
    (SELECT evolv_id FROM pokemon_evolutions
    WHERE pokemon_evolutions.evolv_name = "Charizard")
),
(
    "Charizard",
    5,
    200,
    0,
    (SELECT evolv_id FROM pokemon_evolutions
    WHERE pokemon_evolutions.evolv_name = "Charizard")
);


/*pokemon_types table data*/
INSERT INTO pokemon_types (
    type_name
) 
VALUES
(
    "Normal"
),
(
    "Fire"
),
(
    "Grass"
),
(
    "Water"
),
(
    "Poison"
),
(
    "Flying"
);

/*abilities table data*/
INSERT INTO abilities (
    abil_name,
    abil_description
) 
VALUES
(
    "Overgrow",
    "Powers up Grass-type moves when the Pokémon's HP is low."
),
(
    "Chlorophyll",
    "Boosts the Pokémon's Speed stat in harsh sunlight."
),
(
    "Blaze",
    "Powers up Fire-type moves when the Pokémon's HP is low."
),
(
    "Solar Power",
    "Boosts the Sp. Atk stat in harsh sunlight, but HP decreases every turn."
),
(
    "Torrent",
    "Powers up Water-type moves when the Pokémon's HP is low."
),
(
    "Rain Dish",
    "The Pokémon gradually regains HP in rain."
);

/*pokemon_has_pokemon_types table data*/
INSERT INTO pokemon_has_pokemon_types (
    pokemon_pokemon_id,
    pokemon_types_poke_type_id
) 
VALUES
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Bulbasaur"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Grass")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Bulbasaur"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Poison")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Ivysaur"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Grass")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Ivysaur"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Poison")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Venusaur"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Grass")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Venusaur"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Poison")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charmander"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Fire")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charmeleon"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Fire")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charizard"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Fire")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charizard"),
    (SELECT poke_type_id FROM pokemon_types
    WHERE pokemon_types.type_name = "Flying")
);

/*pokemon_has_abilities table data*/
INSERT INTO pokemon_has_abilities (
    pokemon_pokemon_id,
    abilities_abil_id
) 
VALUES
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Bulbasaur"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Overgrow")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Bulbasaur"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Chlorophyll")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Ivysaur"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Overgrow")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Ivysaur"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Chlorophyll")
),

(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Venusaur"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Overgrow")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Venusaur"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Chlorophyll")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charmander"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Blaze")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charmander"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Solar Power")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charmeleon"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Blaze")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charmeleon"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Solar Power")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charizard"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Blaze")
),
(
    (SELECT pokemon_id FROM pokemon
    WHERE pokemon.pokemon_name = "Charizard"),
    (SELECT abil_id FROM abilities
    WHERE abilities.abil_name = "Solar Power")
);

INSERT INTO move_types (
  move_type_name
)
VALUES
(
  "Normal"
),
(
  "Grass"
),
(
  "Poison"
),
(
  "Flying"
),
(
  "Dragon"
),
(
  "Fire"
);

INSERT INTO moves (
  move_name,
  pp,
  power,
  accuracy,
  move_types_move_types_id
)
VALUES
(
  "Growl",
  40,
  NULL,
  100,
  (SELECT move_types_id FROM move_types
  WHERE move_types.move_type_name = "Normal")
),
(
  "Scratch",
  35,
  40,
  100,
  (SELECT move_types_id FROM move_types
  WHERE move_types.move_type_name = "Normal")
),
(
  "Ember",
  25,
  40,
  100,
  (SELECT move_types_id FROM move_types
  WHERE move_types.move_type_name = "Fire")
),
(
  "Air Slash",
  15,
  75,
  95,
  (SELECT move_types_id FROM move_types
  WHERE move_types.move_type_name = "Flying")
),
(
  "Vine Whip",
  25,
  45,
  100,
  (SELECT move_types_id FROM move_types
  WHERE move_types.move_type_name = "Grass")
),
(
  "Poison Powder",
  35,
  NULL,
  75,
  (SELECT move_types_id FROM move_types
  WHERE move_types.move_type_name = "Poison")
),
(
  "Dragon Breath",
  20,
  60,
  100,
  (SELECT move_types_id FROM move_types
  WHERE move_types.move_type_name = "Dragon")
);

INSERT INTO pokemon_has_moves (
  pokemon_pokemon_id,
  moves_move_id
)
VALUES
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Bulbasaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Growl")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Bulbasaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Scratch")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Bulbasaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Vine Whip")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Ivysaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Growl")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Ivysaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Scratch")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Ivysaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Vine Whip")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Ivysaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Poison Powder")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Venusaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Growl")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Venusaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Scratch")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Venusaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Vine Whip")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Venusaur"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Poison Powder")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charmander"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Growl")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charmander"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Scratch")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charmander"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Ember")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charmeleon"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Growl")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charmeleon"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Scratch")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charmeleon"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Ember")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charmeleon"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Dragon Breath")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charizard"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Growl")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charizard"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Scratch")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charizard"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Ember")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charizard"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Air Slash")
),
(
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = "Charizard"),
  (SELECT move_id FROM moves
  WHERE moves.move_name = "Dragon Breath")
);

INSERT INTO gyms (
    gym_name,
    gym_address,
    gym_zip,
    gym_city,
    gym_state
) 
VALUES
(
    "Bend's Finest Gym",
    "123 Main St.",
    97701,
    "Bend",
    "OR"
),
(
    "Bob's West Coast Burgers",
    "562 Beech Ave.",
    97333,
    "Corvallis",
    "OR"
),
(
    "Mew's Marina Mansion",
    "4830 NE I Ave.",
    97364,
    "Neotsu",
    "OR"
),
(
    "Oregon Online Gym",
    NULL,
    NULL,
    NULL,
    "OR"
);

INSERT INTO trainers (
    first_name,
    last_name,
    xp,
    gyms_gym_id
) 
VALUES 
(
    "Hector",
    "Zerone",
    1084,
    (SELECT gym_id FROM gyms
    WHERE gyms.gym_name = "Bend's Finest Gym")
),
(
    "Tina",
    "Belcher",
    15024,
    (SELECT gym_id FROM gyms
    WHERE gyms.gym_name = "Bob's West Coast Burgers")
),
(
    "Bob",
    "Belcher",
    94,
    (SELECT gym_id FROM gyms
    WHERE gyms.gym_name = "Bob's West Coast Burgers")
),
(
    "Luna",
    "Lovegood",
    978,
    (SELECT gym_id FROM gyms
    WHERE gyms.gym_name = "Mew's Marina Mansion")
),
(
    "Pelé",
    NULL,
    4351,
    (SELECT gym_id FROM gyms
    WHERE gyms.gym_name = "Oregon Online Gym")
);

INSERT INTO pokedecks ( 
  pokedeck_name,
  trainers_trainer_id
)
VALUES 
(
  'Zero`s Heroes',
  (SELECT trainer_id FROM trainers
    WHERE trainers.first_name = "Hector")
),
(
  'Tina`s Crew',
  (SELECT trainer_id FROM trainers
    WHERE trainers.first_name = "Tina")
),
(
  'Bob`s Employees',
  (SELECT trainer_id FROM trainers
    WHERE trainers.first_name = "Bob")
),
(
  'Nargils',
  (SELECT trainer_id FROM trainers
    WHERE trainers.first_name = "Luna")
),
(
  'Brazil`s Finest',
  (SELECT trainer_id FROM trainers
    WHERE trainers.first_name = "Pelé")
);

INSERT INTO pokedecks_have_pokemon (
  pokedecks_pokedeck_id,
  pokemon_pokemon_id
)
VALUES 
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Zero`s Heroes'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Charmeleon')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Zero`s Heroes'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Ivysaur')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Tina`s Crew'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Venusaur')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Tina`s Crew'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Charmander')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Bob`s Employees'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Bulbasaur')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Bob`s Employees'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Charmander')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Nargils'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Venusaur')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Nargils'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Charmeleon')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Brazil`s Finest'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Charizard')
),
(
  (SELECT pokedeck_id FROM pokedecks
  WHERE pokedecks.pokedeck_name = 'Brazil`s Finest'),
  (SELECT pokemon_id FROM pokemon
  WHERE pokemon.pokemon_name = 'Venusaur')
);


SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET FOREIGN_KEY_CHECKS=1;
COMMIT;