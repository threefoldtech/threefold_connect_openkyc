migrations_list = [
    # ("0", "CREATE TABLE IF NOT EXISTS users (user_id text NOT NULL UNIQUE,email text NOT NULL,verification_code text NOT NULL, verified integer,public_key text NOT NULL,signed_email_identifier text NULL);"),
    # ("0", "CREATE TABLE IF NOT EXISTS migrations (migration_id text NOT NULL);"),
    ("1", "CREATE TABLE IF NOT EXISTS phone_users (user_id text NOT NULL UNIQUE,phone text NOT NULL,verification_code text NOT NULL, verified integer,public_key text NOT NULL,signed_phone_identifier text NULL);"),
]