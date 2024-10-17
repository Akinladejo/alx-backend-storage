-- Task 12: Average weighted score - creates a stored procedure ComputeAverageWeightedScoreForUser that computes and stores the average weighted score for a student.
-- user_id, a users.id value (you can assume user_id is linked to an existing users)
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
    DECLARE w_avg_score FLOAT;
    
    -- Calculate the weighted average score
    SELECT SUM(C.score * P.weight) / SUM(P.weight)
    INTO w_avg_score
    FROM users AS U
    JOIN corrections AS C ON U.id = C.user_id
    JOIN projects AS P ON C.project_id = P.id
    WHERE U.id = user_id;
    
    -- Handle NULL result from division
    IF w_avg_score IS NULL THEN
        SET w_avg_score = 0; -- Or handle it according to your application logic
    END IF;
    
    -- Update the average_score for the user
    UPDATE users SET average_score = w_avg_score WHERE id = user_id;
END $$

DELIMITER ;
