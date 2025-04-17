-- Create ENUM type for roles
CREATE TYPE user_role AS ENUM ('Customer', 'SystemAdmin', 'CompanyAdmin');

-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    primary_phone_number VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    profile_picture VARCHAR(255),
    points_balance INTEGER DEFAULT 0,
    streak_count INTEGER DEFAULT 0,
    role user_role NOT NULL DEFAULT 'Customer'
);

-- ENUM types remain unchanged
CREATE TYPE activity_type_enum AS ENUM ('water', 'steps', 'exercise', 'sleep');
CREATE TYPE unit_enum AS ENUM ('oz', 'steps', 'miles', 'hours', 'min', 'km');
CREATE TYPE exercise_type_enum AS ENUM ('yoga', 'run', 'cycling', 'strength');

-- Updated table
CREATE TABLE activity_log (
    log_id SERIAL PRIMARY KEY, -- renamed from id
    user_id INTEGER NOT NULL,
    activity_type activity_type_enum NOT NULL,
    value NUMERIC NOT NULL,
    unit unit_enum,
    exercise_type exercise_type_enum,
    proof BOOLEAN DEFAULT FALSE,
    proof_valid BOOLEAN DEFAULT NULL,
    logged_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);
