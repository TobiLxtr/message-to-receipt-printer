<?php

require_once __DIR__ . "/../config/database.php";

$public_id = $_GET["event"] ?? "";

$stmt = $pdo->prepare("
SELECT * FROM events WHERE public_id=? AND is_active=1
");

$stmt->execute([$public_id]);

$event = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$event) {

    echo "Event not found.";
    exit;

}

// Check submission deadline

if ($event["submission_deadline"] !== null) {

    if (strtotime($event["submission_deadline"]) < time()) {

        echo "Submissions are closed.";
        exit;

    }

}

?>

<h2><?php echo htmlspecialchars($event["name"]); ?></h2>

<form method="POST" action="submit.php">

<input type="hidden" name="event_id" value="<?php echo $event["id"]; ?>">

<input name="name" placeholder="Your name">

<br><br>

<textarea name="text" placeholder="Message"></textarea>

<br><br>

<button type="submit">Send</button>

</form>