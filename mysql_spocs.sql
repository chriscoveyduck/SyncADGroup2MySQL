-- Example stored procedure for adding a user
DELIMITER //
CREATE PROCEDURE sp_add_smtp_enabled_user(IN p_ad_user_id VARCHAR(255), IN p_email VARCHAR(255))
BEGIN
    INSERT INTO smtp_enabled_users (ad_user_id, email)
    VALUES (p_ad_user_id, p_email)
    ON DUPLICATE KEY UPDATE email = p_email, updated_at = CURRENT_TIMESTAMP;
END //
DELIMITER ;

-- Example stored procedure for removing a user
DELIMITER //
CREATE PROCEDURE sp_remove_smtp_enabled_user(IN p_ad_user_id VARCHAR(255))
BEGIN
    DELETE FROM smtp_enabled_users WHERE ad_user_id = p_ad_user_id;
END //
DELIMITER ;
