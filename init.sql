--CREATE EXTENSION dblink;
--CREATE ROLE moderator CREATEDB LOGIN PASSWORD '123';

CREATE OR REPLACE PROCEDURE create_procedures() AS $func$
SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION show_cinema() RETURNS SETOF cinema AS $func1$
SELECT * FROM cinema;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION insert_cinema(n text, a text) RETURNS void AS $func1$
INSERT INTO cinema (name, address) VALUES (n, a);
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION show_film() RETURNS SETOF film AS $func1$
SELECT * FROM film;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION insert_film(n text, g text, dur time,
										  year integer, country text, director text) RETURNS void AS $func1$
INSERT INTO film (name, genre, duration, year, country, director) VALUES (n, g, dur, year, country, director);
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION show_session() RETURNS SETOF session AS $func1$
SELECT * FROM session;
$func1$ language sql; $$);


SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION insert_session(hall integer, time2 timestamp, film integer, cinema integer) RETURNS void AS $func1$
INSERT INTO session (hall, time, film, cinema) VALUES (hall, time2, film, cinema);
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION show_ticket() RETURNS SETOF ticket AS $func1$
SELECT * FROM ticket;
$func1$ language sql; $$);


SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION insert_ticket(seat integer, row2 integer, session integer, price integer) RETURNS void AS $func1$
INSERT INTO ticket (seat, row, session, price) VALUES (seat, row2, session, price);
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION clear_all() RETURNS void AS $func1$
DELETE FROM ticket;
DELETE FROM session;
DELETE FROM cinema;
DELETE FROM film;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_genre(gen text) RETURNS SETOF film AS $func1$
SELECT * FROM film WHERE film.genre = gen;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ 
CREATE OR REPLACE FUNCTION set_ticket_time() RETURNS trigger as $func1$
BEGIN
NEW.bought_date = CURRENT_TIMESTAMP;
RETURN NEW;
END; $func1$ language plpgsql;

CREATE OR REPLACE TRIGGER set_ticket_time_trigger BEFORE INSERT OR UPDATE ON ticket
FOR EACH ROW EXECUTE FUNCTION set_ticket_time(); $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_by_name(n text) RETURNS SETOF film AS $func1$
SELECT * FROM film WHERE film.name = n;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION update_location(tid integer, s integer, r integer) RETURNS void AS $func1$
UPDATE ticket SET seat = s, row = r WHERE id = tid;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION delete_genre(g text) RETURNS void AS $func1$
DELETE FROM film WHERE genre = g;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION delete_cinema(i integer) RETURNS void AS $func1$
DELETE FROM cinema WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION delete_film(i integer) RETURNS void AS $func1$
DELETE FROM film WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_film_by_id(i integer) RETURNS SETOF film AS $func1$
SELECT * FROM film WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_cinema_by_name(n text) RETURNS SETOF cinema AS $func1$
SELECT * FROM cinema WHERE name = n;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_session_by_id(i integer) RETURNS SETOF session AS $func1$
SELECT * FROM session WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_cinema_by_id(i integer) RETURNS SETOF cinema AS $func1$
SELECT * FROM cinema WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION delete_session(i integer) RETURNS void AS $func1$
DELETE FROM session WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION delete_ticket(i integer) RETURNS void AS $func1$
DELETE FROM ticket WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_ticket_by_id(i integer) RETURNS SETOF ticket AS $func1$
SELECT * FROM ticket WHERE id = i;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION find_specific_sessions(cin integer, film integer) RETURNS SETOF session AS $func1$
SELECT * FROM session WHERE cinema = cin and film = film;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION get_genres() RETURNS SETOF text AS $func1$
SELECT DISTINCT genre FROM film;
$func1$ language sql; $$);

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123',
$$ CREATE OR REPLACE FUNCTION get_recommendations(gen text) RETURNS SETOF text AS $func1$
SELECT name FROM film WHERE genre = gen;
$func1$ language sql; $$);

$func$ language sql;


CREATE OR REPLACE PROCEDURE create_db() AS
$func$
SELECT dblink_exec('host=localhost port=5432
				   dbname=postgres user=moderator password=123', 
'CREATE DATABASE lab_tickets;');

GRANT CREATE ON DATABASE lab_tickets TO moderator;

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123', 
'CREATE TABLE cinema (
	id serial PRIMARY KEY,
	name text,
	address text
);');
SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123', 
'CREATE TABLE film (
	id serial PRIMARY KEY,
	name text,
    genre text,
	duration time,
	year integer,
	country text,
	director text
);');
SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123', 
'CREATE TABLE session (
	id serial PRIMARY KEY,
	hall integer,
    time timestamp,
	film integer references film(id) ON DELETE CASCADE,
	cinema integer references cinema(id) ON DELETE CASCADE
);');
SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123', 
'CREATE TABLE ticket (
	id serial PRIMARY KEY,
	seat integer,
    row integer,
	session integer references session(id) ON DELETE CASCADE,
	price integer,
	bought_date timestamp
);');

SELECT dblink_exec('host=localhost port=5432
				   dbname=lab_tickets user=moderator password=123', 
$$ CREATE INDEX ON film(name) $$);
CALL create_procedures();
$func$ language sql;


CREATE OR REPLACE PROCEDURE drop_db() AS $$
SELECT dblink_exec('host=localhost port=5432
				   dbname=postgres user=moderator password=123', 
				   'DROP DATABASE lab_tickets');
$$ language sql;

--CALL create_db();
--CALL drop_db();