-- CREATE TYPE
--DROP TYPE IF EXISTS results;
CREATE TYPE results AS ENUM (
    'player1',
    'player2',
    'tie'
);

-- CREATE TABLES
CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL
);


--DROP TABLE IF EXISTS games;
CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY NOT NULL,
    date TIMESTAMP NOT NULL,
    result results NOT NULL,
    player_id_ONE INT NOT NULL,
    player_id_TWO INT NOT NULL,
    CONSTRAINT fk_player_ONE
        FOREIGN KEY(player_id_ONE)
	        REFERENCES players(player_id),
	CONSTRAINT fk_player_TWO
        FOREIGN KEY(player_id_TWO)
	        REFERENCES players(player_id)
);

-- INSERT VALUES
INSERT INTO players VALUES (default, 'Tomasz', 'Sikora');
INSERT INTO players VALUES (default, 'Katarzyna', 'Zalesińska');
INSERT INTO players VALUES (default, 'Natalia', 'Kowal');
INSERT INTO players VALUES (default, 'Jarosław', 'Nowak');