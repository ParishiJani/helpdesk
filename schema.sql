CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(120) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	password VARCHAR(60) NOT NULL, 
	is_admin BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
CREATE TABLE ticket (
	id INTEGER NOT NULL, 
	title VARCHAR(100) NOT NULL, 
	description TEXT NOT NULL, 
	created_at DATETIME, 
	user_id INTEGER NOT NULL, 
	status VARCHAR(50) NOT NULL, notes TEXT NOT NULL DEFAULT '', 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
