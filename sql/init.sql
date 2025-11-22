-- users
CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMP DEFAULT now()
);

-- pets
CREATE TABLE IF NOT EXISTS pets (
  id serial PRIMARY KEY,
  owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  species VARCHAR(100),
  breed VARCHAR(100),
  created_at TIMESTAMP DEFAULT now()
);

-- tracks (seguimiento de ubicacion / estado)
CREATE TABLE IF NOT EXISTS tracks (
  id serial PRIMARY KEY,
  pet_id INTEGER REFERENCES pets(id) ON DELETE CASCADE,
  latitude NUMERIC,
  longitude NUMERIC,
  note TEXT,
  created_at TIMESTAMP DEFAULT now()
);
