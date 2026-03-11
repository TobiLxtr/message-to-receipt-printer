<?php

/**
 * Copy this file to config.php and adjust the values.
 */

/*
|--------------------------------------------------------------------------
| Database configuration
|--------------------------------------------------------------------------
*/

define("DB_HOST", "localhost");
define("DB_NAME", "db_name");
define("DB_USER", "db_user");
define("DB_PASS", "db_password");


/*
|--------------------------------------------------------------------------
| API authentication
|--------------------------------------------------------------------------
*/

define("API_KEY", "CHANGE_THIS_SECRET_KEY");


/*
|--------------------------------------------------------------------------
| Rate limiting
|--------------------------------------------------------------------------
*/

define("RATE_LIMIT_MAX_MESSAGES", 10);
define("RATE_LIMIT_WINDOW_SECONDS", 3600);