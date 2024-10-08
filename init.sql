CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS sc_groups (
id SERIAL PRIMARY KEY,
title TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS sc_prep (
id SERIAL PRIMARY KEY,
fio TEXT NOT NULL UNIQUE,
chair TEXT,
degree TEXT,
photo TEXT,
student_id INTEGER,
archive BOOL DEFAULT 'f'
);

CREATE TABLE IF NOT EXISTS sc_disc (
id SERIAL PRIMARY KEY,
title TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS sc_rasp (
id SERIAL PRIMARY KEY,
disc_id INTEGER REFERENCES sc_disc(id),    
prep_id INTEGER REFERENCES sc_prep(id),
weekday INTEGER,
week INTEGER,
lesson INTEGER,
group_id INTEGER REFERENCES sc_groups(id),
subgroup INTEGER
);
