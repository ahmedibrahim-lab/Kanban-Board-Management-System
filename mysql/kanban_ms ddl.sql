-- drop database kanban_ms
CREATE DATABASE kanban_ms;

USE kanban_ms;

CREATE TABLE kanban_user
(
	user_id int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	password_hash varchar(255) NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	updated timestamp NOT NULL DEFAULT now(),
	unique(email)
);

CREATE TABLE task
(
	task_id bigint UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	task_name varchar(50) NOT NULL,
	description text,
	priority enum('Low', 'Medium', 'High') NOT NULL,
	deadline datetime NOT NULL,
	stage enum('To Do', 'In Progress', 'Done') NOT NULL,
	created_by int UNSIGNED NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	updated timestamp NOT NULL DEFAULT now()
);

CREATE TABLE task_assignment
(
	task_id bigint UNSIGNED NOT NULL,
	user_id int UNSIGNED NOT NULL,
	start_time datetime NOT NULL,
	end_time datetime,
	assigned_by int UNSIGNED NOT NULL,
	created_at timestamp NOT NULL DEFAULT now(),
	updated timestamp NOT NULL DEFAULT now()
);

CREATE TABLE task_stage_log
(
	task_id bigint UNSIGNED NOT NULL,
	task_name varchar(50) NOT NULL,
	stage SMALLINT NOT NULL,			/* 1 - to do, 2 - in progress, 3 - done */
	changed_at timestamp NOT NULL DEFAULT now()
);

CREATE TABLE user_activity_log
(
	user_id int UNSIGNED NOT NULL,
	user_name varchar (50),
	modified_table varchar(50) NOT NULL,
	modified_field varchar(50) NOT NULL,
	modification_time timestamp NOT NULL DEFAULT now()
);


ALTER TABLE task
	ADD CONSTRAINT task_created_by_user_id_fk FOREIGN KEY (created_by) REFERENCES kanban_user(user_id) ON DELETE CASCADE;

ALTER TABLE task_assignment
	ADD CONSTRAINT task_assignment_task_id_fk FOREIGN KEY (task_id) REFERENCES task(task_id) ON DELETE CASCADE,
	ADD CONSTRAINT task_assignment_user_id_fk FOREIGN KEY (user_id) REFERENCES kanban_user(user_id) ON DELETE CASCADE,
	ADD CONSTRAINT task_assignment_assigned_by_user_id_fk FOREIGN KEY (assigned_by) REFERENCES kanban_user(user_id) ON DELETE CASCADE;

COMMIT;