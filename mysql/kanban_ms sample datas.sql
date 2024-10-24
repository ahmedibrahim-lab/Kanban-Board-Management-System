USE kanban_ms;

INSERT INTO kanban_user (name, email, password_hash)	/* passworrd_hash: using MD5 hash	*/
	SELECT 'Alice Johnson', 'alice.johnson@codecompany.com', '5f4dcc3b5aa765d61d8327deb882cf99'				-- password
	UNION SELECT 'Bob Smith', 'bob.smith@codecompany.com', '202cb962ac59075b964b07152d234b70'				-- 123
	UNION SELECT 'Charlie Davis', 'charlie.davis@codecompany.com', '81dc9bdb52d04dc20036dbd8313ed055'		-- 1234
	UNION SELECT 'Diana Moore', 'diana.moore@codecompany.com', '098f6bcd4621d373cade4e832627b4f6'			-- test
	UNION SELECT 'Eve Adams', 'eve.adams@codecompany.com', 'e99a18c428cb38d5f260853678922e03';				-- abc123


INSERT INTO task (task_name, description, priority, deadline, stage, created_by)
	SELECT 'Design Homepage', 'Create the main homepage layout and design', 'High', '2024-10-31 09:00:00', 'To Do', 
		(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS created_by		
	UNION SELECT 'Write API Documentation', 'Document all API endpoints for the project', 'Medium', '2024-11-05 17:00:00', 'In Progress',
		(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS created_by		
	UNION SELECT 'Fix Login Bug', 'Resolve the issue causing login failures for some users', 'High', '2024-10-25 12:00:00', 'In Progress',
		(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS created_by		
	UNION SELECT 'Optimize Database', 'Improve query performance by optimizing database indexes', 'Low', '2024-12-01 15:00:00', 'To Do',
		(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS created_by		
	UNION SELECT 'Create Unit Tests', 'Write unit tests for the authentication module', 'Medium', '2024-11-10 18:00:00', 'To Do',
		(SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com') AS created_by;


INSERT INTO task_assignment (task_id, user_id, start_time, assigned_by)
	SELECT 	
			(SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS user_id,
			'2024-10-20 09:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by
	UNION SELECT 
			(SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS user_id,
			'2024-10-20 09:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS user_id,
			'2024-10-19 08:30:00',
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Optimize Database' AND deadline = '2024-12-01 15:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS user_id,
			'2024-10-22 11:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Create Unit Tests' AND deadline = '2024-11-10 18:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com') AS user_id,
			'2024-10-23 14:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS user_id,
			'2024-10-21 09:30:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS user_id,
			'2024-10-21 11:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com') AS user_id,
			'2024-10-22 13:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Optimize Database' AND deadline = '2024-12-01 15:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'eve.adams@codecompany.com') AS user_id,
			'2024-10-23 10:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Create Unit Tests' AND deadline = '2024-11-10 18:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS user_id,
			'2024-10-23 15:30:00',
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'eve.adams@codecompany.com') AS user_id,
			'2024-10-21 12:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS user_id,
			'2024-10-22 09:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS user_id,
			'2024-10-23 09:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Create Unit Tests' AND deadline = '2024-11-10 18:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS user_id,
			'2024-10-24 11:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Optimize Database' AND deadline = '2024-12-01 15:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS user_id,
			'2024-10-24 14:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com') AS user_id,
			'2024-10-23 16:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS user_id,
			'2024-10-24 08:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'eve.adams@codecompany.com') AS user_id,
			'2024-10-24 13:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com') AS assigned_by
	UNION SELECT
			(SELECT task_id FROM task WHERE task_name = 'Optimize Database' AND deadline = '2024-12-01 15:00:00') AS task_id,
			(SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com') AS user_id,
			'2024-10-25 09:00:00',
			(SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com') AS assigned_by;

COMMIT;