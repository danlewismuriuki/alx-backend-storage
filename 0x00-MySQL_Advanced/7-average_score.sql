-- SQL script that creates stored procedure ComputeAverageScoreForUser
-- computes and store the average score for a student.
-- An average score can be a decimal

-- Drop the existing procedure
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$
-- create the procedure with 1 arg
CREATE PROCEDURE ComputeAverageScoreForUser(
    IN user_id INT
)
BEGIN 
    -- declare variable to stroee temp avg score

    DECLARE avg_score FLOAT;

    -- Calculate the avg score for the corrections Table for score column
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE user_id = user_id;

    -- Updat  the users Table and set the average score
    UPDATE users
    SET average_score = IFNULL(avg_score, 0)
    WHERE id = user_id;

END $$

DELIMITER ;
