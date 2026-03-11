<?php

/**
 * Database connection using PDO.
 * Reads credentials from config.php
 */

require_once __DIR__ . "/config.php";

try {

    $pdo = new PDO(
        "mysql:host=" . DB_HOST . ";dbname=" . DB_NAME . ";charset=utf8mb4",
        DB_USER,
        DB_PASS,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
        ]
    );

} catch (PDOException $e) {

    http_response_code(500);
    echo "Database connection failed.";
    exit;

}