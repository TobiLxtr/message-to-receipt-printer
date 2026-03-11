<?php

// Send JSON response and exit script

function json_response($data)
{
    header("Content-Type: application/json");
    echo json_encode($data);
    exit;
}