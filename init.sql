-- CREATE TYPE
--DROP TYPE IF EXISTS results;
CREATE TYPE results AS ENUM (
    'player1',
    'player2',
    'tie'
);

-- CREATE TABLE
--DROP TABLE IF EXISTS games;
CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY NOT NULL,
    date TIMESTAMP NOT NULL,
    result results NOT NULL
);