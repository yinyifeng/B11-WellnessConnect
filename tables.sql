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