migrations_list = [
    ("0", "CREATE TABLE IF NOT EXISTS users (user_id text NOT NULL UNIQUE,email text NOT NULL,verification_code text NOT NULL, verified integer,public_key text NOT NULL,signed_email_identifier text NULL);"),
    ("0", "CREATE TABLE IF NOT EXISTS migrations (migration_id text NOT NULL);"),
    ("1", "ALTER TABLE users ADD COLUMN phone text NULL;"),
    ("2", "ALTER TABLE users ADD COLUMN sms_verification_code text NULL;"),
    ("3", "ALTER TABLE users ADD COLUMN sms_verified integer NULL;"),
    ("4", "ALTER TABLE users ADD COLUMN signed_phone_identifier text NULL;"),

]