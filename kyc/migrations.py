migrations_list = [
    ("0",
     "CREATE TABLE IF NOT EXISTS users (user_id text NOT NULL UNIQUE,email text NOT NULL,verification_code text NOT NULL, verified integer,public_key text NOT NULL,signed_email_identifier text NULL);"),
    ("1", "CREATE TABLE IF NOT EXISTS migrations (migration_id text NOT NULL);"),
    ("2",
     "CREATE TABLE IF NOT EXISTS phone_users (user_id text NOT NULL UNIQUE,phone text NOT NULL,verification_code text NOT NULL, verified integer,public_key text NOT NULL,signed_phone_identifier text NULL);"),
    ("3",
     "CREATE TABLE IF NOT EXISTS identity_users (user_id text NOT NULL UNIQUE, verification_code text NOT NULL, verified integer,public_key text NOT NULL, signed_identity_name_identifier text NULL, signed_identity_country_identifier text NULL, signed_identity_dob_identifier text NULL, signed_identity_document_meta_identifier text NULL, signed_identity_gender_identifier text NULL);"),
    ("4",
     "CREATE TABLE IF NOT EXISTS shufti_requests (day DATETIME NOT NULL, hash_spi text NOT NULL);"),
]
