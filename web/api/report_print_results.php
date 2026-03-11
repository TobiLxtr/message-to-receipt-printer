<?php

require_once __DIR__ . "/../config/database.php";
require_once __DIR__ . "/../lib/auth.php";
require_once __DIR__ . "/../lib/response.php";

require_api_key();

/**
 * Read JSON body
 */

$data = json_decode(file_get_contents("php://input"), true);

$public_id = $data["event"] ?? null;

if (!$public_id) {

    http_response_code(400);
    echo "Missing event";
    exit;

}

/**
 * Resolve event_id
 */

$stmt = $pdo->prepare("
SELECT id
FROM events
WHERE public_id = ?
");

$stmt->execute([$public_id]);

$event = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$event) {

    http_response_code(404);
    echo "Event not found";
    exit;

}

$event_id = $event["id"];

$printed = $data["printed_ids"] ?? [];
$failed = $data["failed"] ?? [];

/**
 * Mark printed entries
 */

foreach ($printed as $id) {

    $stmt = $pdo->prepare("
        UPDATE entries
        SET status='printed', printed_at=NOW()
        WHERE id=? AND event_id=?
    ");

    $stmt->execute([$id, $event_id]);

}

/**
 * Mark failed entries
 */

foreach ($failed as $entry) {

    $stmt = $pdo->prepare("
        UPDATE entries
        SET status='failed', error=?
        WHERE id=? AND event_id=?
    ");

    $stmt->execute([
        $entry["error"],
        $entry["id"],
        $event_id
    ]);

}

json_response(["success"=>true]);