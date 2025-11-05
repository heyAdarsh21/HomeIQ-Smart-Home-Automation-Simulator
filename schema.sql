-- schema.sql

-- USERS
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255) NOT NULL
);

-- ROOMS
CREATE TABLE IF NOT EXISTS rooms (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL
);

-- DEVICES
CREATE TABLE IF NOT EXISTS devices (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  status BOOLEAN DEFAULT false,
  energy_usage INTEGER,  -- watts when ON
  room_id INT REFERENCES rooms(id)
);

-- ENERGY LOGS (for analytics) — we append a row whenever a device state changes or periodically
CREATE TABLE IF NOT EXISTS energy_logs (
  id SERIAL PRIMARY KEY,
  device_id INT REFERENCES devices(id),
  ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  energy_wh INTEGER  -- watt-hours consumed during the logged interval (or simulated)
);

-- OPTIONAL: ensure some indices for speed
CREATE INDEX IF NOT EXISTS idx_energy_logs_ts ON energy_logs(ts);
