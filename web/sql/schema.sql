--  Run for example in phphMyAdmin
CREATE TABLE events (

    id INT AUTO_INCREMENT PRIMARY KEY,

    public_id VARCHAR(32) NOT NULL UNIQUE,

    slug VARCHAR(100) UNIQUE,

    name VARCHAR(255) NOT NULL,

    type VARCHAR(50),

    event_date DATETIME NULL,

    submission_deadline DATETIME NULL,

    is_active BOOLEAN DEFAULT TRUE,

    created_at DATETIME NOT NULL,

    INDEX(public_id)

) ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;


CREATE TABLE entries (

    id INT AUTO_INCREMENT PRIMARY KEY,

    event_id INT NOT NULL,

    created_at DATETIME NOT NULL,

    printed_at DATETIME NULL,

    ip_address VARCHAR(45),

    name VARCHAR(100),

    text TEXT,

    image_url VARCHAR(255),

    status ENUM('pending','printed','failed') DEFAULT 'pending',

    error TEXT NULL,

    FOREIGN KEY (event_id) REFERENCES events(id),

    INDEX(event_id),
    INDEX(status)

) ENGINE=InnoDB
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;