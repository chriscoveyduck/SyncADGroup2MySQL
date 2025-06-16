-- MySQL schema for SmtpEnabledUsers group membership
CREATE TABLE IF NOT EXISTS smtp_enabled_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ad_user_id VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_ad_user_id (ad_user_id)
);
