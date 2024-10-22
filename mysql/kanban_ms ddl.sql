CREATE DATABASE kanban_ms;

USE kanban_ms;

CREATE TABLE kanban_user
(
	user_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	password_hash varchar(20) NOT NULL,
	unique(email)
);

CREATE TABLE task
(
	task_id bigint UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	task_name varchar(50) NOT NULL,
	description text NULL,
	priority enum('low', 'medium', 'high') NOT NULL,
	deadline datetime NOT NULL,
	stage enum('To do', 'In progress', 'Done') NOT NULL,
	created_by int UNSIGNED NOT NULL,
	created_at timestamp NOT NULL,
	updated timestamp NOT NULL
);

CREATE TABLE task_assignment
(
	task_id bigint UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_id int UNSIGNED NOT NULL,
	start_time datetime NOT NULL,
	end_time datetime NOT NULL
);

ALTER TABLE task
	ADD CONSTRAINT created_by_user_id_fk FOREIGN KEY (created_by) REFERENCES kanban_user(user_id);

ALTER TABLE task_assignment
	ADD CONSTRAINT task_id_fk FOREIGN KEY (task_id) REFERENCES task(task_id),
	ADD CONSTRAINT user_id_fk FOREIGN KEY (user_id) REFERENCES kanban_user(user_id);

COMMIT;