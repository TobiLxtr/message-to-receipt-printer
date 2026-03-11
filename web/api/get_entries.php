<?php

require_once __DIR__ . "/../config/database.php";
require_once __DIR__ . "/../lib/auth.php";
require_once __DIR__ . "/../lib/response.php";

require_api_key();

/**
 * Retrieve event using public_id
 */

$public_id = $_GET["event"] ?? null;

if (!$public_id) {

    http_response_code(400);
    echo "Missing event parameter";
    exit;

}

/**
 * Resolve event_id from public_id
 */

$stmt = $pdo->prepare("
SELECT id, type
FROM events
WHERE public_id = ?
AND is_active = 1
");

$stmt->execute([$public_id]);

$event = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$event) {

    http_response_code(404);
    echo "Event not found";
    exit;

}

$event_id = $event["id"];
$type = $event["type"];

/**
 * Retrieve pending entries for this event
 */

$stmt = $pdo->prepare("
SELECT id, created_at, name, text, image_url
FROM entries
WHERE event_id = ?
AND status = 'pending'
ORDER BY created_at ASC
LIMIT 50
");

$stmt->execute([$event_id]);

$entries = $stmt->fetchAll(PDO::FETCH_ASSOC);

/**
 * Return response
 */

json_response([
    "type" => $type,
    "entries" => $entries
]);