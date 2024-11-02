delimiter //

CREATE PROCEDURE insert_task_stage_log (IN task_id bigint, IN task_name varchar(50), IN stage varchar(15))
BEGIN
	INSERT INTO task_stage_log (task_id, task_name, stage)
	VALUES (task_id, task_name, stage);
END;
//

CREATE TRIGGER task_update
BEFORE UPDATE ON task
FOR EACH ROW
BEGIN
	SET NEW.updated = current_timestamp();
END;
//

CREATE TRIGGER update_task_stage_log
AFTER UPDATE ON task
FOR EACH ROW
BEGIN
	CALL insert_task_stage_log (NEW.task_id, NEW.task_name, NEW.stage);
END;
//

CREATE TRIGGER insert_task_stage_log
AFTER INSERT ON task
FOR EACH ROW
BEGIN
	CALL insert_task_stage_log (NEW.task_id, NEW.task_name, NEW.stage);
END;
//

CREATE PROCEDURE insert_user_activity_log (IN user_id int, IN user_name varchar(50), modified_table varchar(50), action_type varchar(50))
BEGIN
	INSERT INTO user_activity_log (user_id, user_name, modified_table, action_type)
	VALUES (user_id, user_name, modified_table, action_type);	
END;
//