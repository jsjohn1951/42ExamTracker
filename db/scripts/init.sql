CREATE TABLE IF NOT EXISTS admin (
	username VARCHAR(255),
	hashauthentication VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS breaks (
	id INT,
	perfacility INT,
	perperson INT
);

CREATE TABLE IF NOT EXISTS history (
	id INT,
	user_id VARCHAR(255),
	event_oc VARCHAR(255),
	time_stamp VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS started (
	isstarted BOOLEAN,
	timestarted VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dbuser (
	id INT,
	user_id VARCHAR(255),
	gender VARCHAR(255),
	usr_status VARCHAR(255),
	num INT,
	time_stamp VARCHAR(255)
);