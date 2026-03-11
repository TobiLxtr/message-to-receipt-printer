<?php

require_once __DIR__ . "/../config/database.php";
require_once __DIR__ . "/../lib/rate_limit.php";

$event_id = $_POST["event_id"];
$name = trim($_POST["name"] ?? "");
$text = trim($_POST["text"] ?? "");

if ($text === "") {

    echo "Message cannot be empty.";
    exit;

}

$ip = $_SERVER["REMOTE_ADDR"];

// Apply rate limiting

check_rate_limit($pdo, $ip);

// Store entry

$stmt = $pdo->prepare("
INSERT INTO entries
(event_id, created_at, ip_address, name, text)
VALUES (?, NOW(), ?, ?, ?)
");

$stmt->execute([
    $event_id,
    $ip,
    $name,
    $text
]);

echo "Message sent successfully.";