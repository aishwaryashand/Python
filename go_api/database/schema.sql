CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE base_table(
	created_at TIMESTAMP NOT NULL,
	upted_at TIMESTAMP NOT NULL
);

CREATE TABLE user_sccount(
	id uuid PRIMARY KEY DEFAULT uuid_generate_v1(),
	email VARCHAR(255) UNIQUE NOT NULL,
	password VARCHAR(255) NOT NULL
)INHERITS (base_table)