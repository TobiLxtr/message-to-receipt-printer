<?php

require_once __DIR__ . "/../config/config.php";

/**
 * Retrieve API key from request headers.
 * Handles different server configurations.
 */
function get_api_key()
{
    $headers = getallheaders();

    foreach ($headers as $name => $value) {

        if (strtolower($name) === "x-api-key") {
            return $value;
        }

    }

    return null;
}

/**
 * Require a valid API key for API access.
 */
function require_api_key()
{

    $api_key = get_api_key();

    if (!$api_key) {

        http_response_code(401);
        echo "Missing API key";
        exit;

    }

    if ($api_key !== API_KEY) {

        http_response_code(403);
        echo "Invalid API key";
        exit;

    }

}