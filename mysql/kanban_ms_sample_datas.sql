INSERT INTO kanban_user (name, email, password_hash) VALUES ('Alice Johnson', 'alice.johnson@codecompany.com', 'pbkdf2:sha256:260000$9tSwWumwYM2eQxtY$82ece4080812fd861fac18cd3af3d765b84159bf04dc582d68f2263003e8673b'),('Bob Smith', 'bob.smith@codecompany.com', 'pbkdf2:sha256:260000$gIFfQUMGpi2WzbLV$710b309945a9762329e3edecbe5db80ee8221c7bbf46bd30154d4d7e39e57fe9'),('Charlie Davis', 'charlie.davis@codecompany.com', 'pbkdf2:sha256:260000$ZY5Zy5zuKOP71lWU$11115dcb5f2aec787bc704386fa4feb8a482a45ce9917a40ce9608a55173f28b'),('Diana Moore', 'diana.moore@codecompany.com', 'pbkdf2:sha256:260000$qqy7eIZffWRRhQIn$5ee8a97e415003e2ca004b0edac97a4b0f20d5ecd8d643400354c7a719d515ce'),('Eve Adams', 'eve.adams@codecompany.com', 'pbkdf2:sha256:260000$LAj9cwkBLW5zAjng$f5c610cfa2876984836b6b3b655c70f289cbcc8443625eadbb03753e60dbbc25');

INSERT INTO task (task_name, description, priority, deadline, stage, created_by) VALUES
    ('Design Homepage', 'Create the main homepage layout and design', 'High', '2024-10-31 09:00:00', 'To Do',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ('Write API Documentation', 'Document all API endpoints for the project', 'Medium', '2024-11-05 17:00:00', 'In Progress',
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com')),
    ('Fix Login Bug', 'Resolve the issue causing login failures for some users', 'High', '2024-10-25 12:00:00', 'In Progress',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com')),
    ('Optimize Database', 'Improve query performance by optimizing database indexes', 'Low', '2024-12-01 15:00:00', 'To Do',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ('Create Unit Tests', 'Write unit tests for the authentication module', 'Medium', '2024-11-10 18:00:00', 'To Do',
        (SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com'));
       
INSERT INTO task_assignment (task_id, user_id, start_time, assigned_by) VALUES
    ((SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com'),
        '2024-10-20 09:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com'),
        '2024-10-20 09:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com'),
        '2024-10-19 08:30:00',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Optimize Database' AND deadline = '2024-12-01 15:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com'),
        '2024-10-22 11:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Create Unit Tests' AND deadline = '2024-11-10 18:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com'),
        '2024-10-23 14:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com'),
        '2024-10-21 09:30:00',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com'),
        '2024-10-21 11:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com'),
        '2024-10-22 13:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Optimize Database' AND deadline = '2024-12-01 15:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'eve.adams@codecompany.com'),
        '2024-10-23 10:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Create Unit Tests' AND deadline = '2024-11-10 18:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com'),
        '2024-10-23 15:30:00',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'eve.adams@codecompany.com'),
        '2024-10-21 12:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com'),
        '2024-10-22 09:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com'),
        '2024-10-23 09:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Create Unit Tests' AND deadline = '2024-11-10 18:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com'),
        '2024-10-24 11:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Optimize Database' AND deadline = '2024-12-01 15:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com'),
        '2024-10-24 14:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Design Homepage' AND deadline = '2024-10-31 09:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com'),
        '2024-10-25 13:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Write API Documentation' AND deadline = '2024-11-05 17:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'eve.adams@codecompany.com'),
        '2024-10-24 16:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com')),
    ((SELECT task_id FROM task WHERE task_name = 'Fix Login Bug' AND deadline = '2024-10-25 12:00:00'),
        (SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com'),
        '2024-10-24 12:00:00',
        (SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com'));

INSERT INTO task_stage_log (task_id, task_name, stage, changed_at) VALUES
	((SELECT task_id FROM task WHERE task_name = 'Design Homepage'), 'Design Homepage', 'To Do', '2024-10-20 08:00:00'),
	((SELECT task_id FROM task WHERE task_name = 'Design Homepage'), 'Design Homepage', 'In Progress', '2024-10-22 14:00:00'),
	((SELECT task_id FROM task WHERE task_name = 'Write API Documentation'), 'Write API Documentation', 'To Do', '2024-10-18 10:00:00'),
	((SELECT task_id FROM task WHERE task_name = 'Write API Documentation'), 'Write API Documentation', 'In Progress', '2024-10-21 11:30:00'),
	((SELECT task_id FROM task WHERE task_name = 'Fix Login Bug'), 'Fix Login Bug', 'To Do', '2024-10-15 09:00:00'),
	((SELECT task_id FROM task WHERE task_name = 'Fix Login Bug'), 'Fix Login Bug', 'In Progress', '2024-10-23 15:00:00'),
	((SELECT task_id FROM task WHERE task_name = 'Fix Login Bug'), 'Fix Login Bug', 'Done', '2024-10-24 16:00:00'),
	((SELECT task_id FROM task WHERE task_name = 'Optimize Database'), 'Optimize Database', 'To Do', '2024-10-20 09:00:00'),
	((SELECT task_id FROM task WHERE task_name = 'Create Unit Tests'), 'Create Unit Tests', 'To Do', '2024-10-20 09:00:00');

INSERT INTO user_activity_log (user_id, user_name, modified_table, action_type, modification_time) VALUES
 	((SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com'), 'Alice Johnson', 'task', 'insert', '2024-10-22 14:00:00'),
 	((SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com'), 'Bob Smith', 'task_assignment', 'update', '2024-10-21 11:00:00'),
 	((SELECT user_id FROM kanban_user WHERE email = 'charlie.davis@codecompany.com'), 'Charlie Davis', 'task', 'update', '2024-10-23 10:30:00'),
 	((SELECT user_id FROM kanban_user WHERE email = 'diana.moore@codecompany.com'), 'Diana Moore', 'kanban_user', 'delete', '2024-10-24 13:15:00'),
 	((SELECT user_id FROM kanban_user WHERE email = 'eve.adams@codecompany.com'), 'Eve Adams', 'task', 'insert', '2024-10-25 11:45:00'),
 	((SELECT user_id FROM kanban_user WHERE email = 'alice.johnson@codecompany.com'), 'Alice Johnson', 'task_assignment', 'insert', '2024-10-25 16:00:00'),
 	((SELECT user_id FROM kanban_user WHERE email = 'bob.smith@codecompany.com'), 'Bob Smith', 'task_stage_log', 'update', '2024-10-24 09:00:00');

COMMIT;