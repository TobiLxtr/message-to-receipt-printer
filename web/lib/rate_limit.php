<?php

require_once __DIR__ . "/../config/config.php";

// Check rate limit per IP address

function check_rate_limit($pdo, $ip)
{

    $stmt = $pdo->prepare("
        SELECT COUNT(*)
        FROM entries
        WHERE ip_address = ?
        AND created_at > (NOW() - INTERVAL ? SECOND)
    ");

    $stmt->execute([$ip, RATE_LIMIT_WINDOW_SECONDS]);

    $count = $stmt->fetchColumn();

    if ($count >= RATE_LIMIT_MAX_MESSAGES) {

        echo "Rate limit exceeded. Please try later.";
        exit;

    }

}