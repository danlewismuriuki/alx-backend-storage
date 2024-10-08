-- script that creates a stored procedure AddBonus
-- adds a new correction for a student.

DELIMITER $$

CREATE PROCEDURE AddBonus(
	IN user_id INT,
	IN project_name VARCHAR(255),
	IN score INT
)
BEGIN
    DECLARE project_id INT;

    -- CHECK IF PROJECT ALREADY EXISTS
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;
    
    -- If project does not exists instert it and set the new project ID
    IF project_id IS NULL THEN
	    INSERT INTO projects (name) VALUES(project_name);
	    SET project_id = LAST_INSERT_ID();
    END IF;

    -- Insert the corrections with the project_id
    INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, project_id, score);

END $$

DELIMITER ;
