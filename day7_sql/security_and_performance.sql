
-- ============================================================
-- DAY 7 SQL ASSIGNMENT
-- EXPLAIN, SQL INJECTION, PARAMETERIZED QUERIES AND UPSERT
-- Database: Parcel Management System
-- ============================================================


-- ============================================================
-- PART 1: EXPLAIN BEFORE AND AFTER ADDING AN INDEX
-- ============================================================

-- Remove the index if it already exists.
-- This allows us to demonstrate the query plan before indexing.
DROP INDEX IF EXISTS idx_parcels_origin;

-- BEFORE INDEX:
-- Check how PostgreSQL retrieves parcels from Kolkata.
EXPLAIN
SELECT *
FROM parcels
WHERE origin = 'Kolkata';


-- Create an index on the origin column.
CREATE INDEX idx_parcels_origin
ON parcels(origin);

-- Update PostgreSQL statistics.
ANALYZE parcels;

-- AFTER INDEX:
-- Check the execution plan again.
EXPLAIN
SELECT *
FROM parcels
WHERE origin = 'Kolkata';

-- Check actual execution statistics.
EXPLAIN ANALYZE
SELECT *
FROM parcels
WHERE origin = 'Kolkata';


-- Optional demonstration:
-- Encourage PostgreSQL to use the index so we can
-- observe the index access path on our small sample table.
SET enable_seqscan = OFF;

EXPLAIN
SELECT *
FROM parcels
WHERE origin = 'Kolkata';

-- Restore PostgreSQL's normal planner behaviour.
RESET enable_seqscan;


-- ============================================================
-- PART 2: DEMONSTRATE SQL INJECTION
-- ============================================================

-- Create a deliberately vulnerable toy function.
-- User input is directly concatenated into the SQL statement.

CREATE OR REPLACE FUNCTION vulnerable_parcel_lookup(
    p_tracking_number TEXT
)
RETURNS SETOF parcels
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY EXECUTE
        'SELECT * FROM parcels WHERE tracking_number = '''
        || p_tracking_number
        || '''';
END;
$$;


-- Test 1: Normal input.
-- Expected: One parcel (PRC1001).

SELECT *
FROM vulnerable_parcel_lookup('PRC1001');


-- Test 2: Malicious input.
-- Expected: All parcels because the injected condition is true.
-- This demonstrates the SQL injection vulnerability.

SELECT *
FROM vulnerable_parcel_lookup(
    $input$' OR '1'='1' --$input$
);


-- ============================================================
-- PART 3: FIX SQL INJECTION USING PARAMETERIZED QUERIES
-- ============================================================

-- Create a secure function.
-- The input is passed separately using the USING clause.

CREATE OR REPLACE FUNCTION safe_parcel_lookup(
    p_tracking_number TEXT
)
RETURNS SETOF parcels
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY EXECUTE
        'SELECT * FROM parcels WHERE tracking_number = $1'
        USING p_tracking_number;
END;
$$;


-- Test 1: Normal input.
-- Expected: One parcel (PRC1001).

SELECT *
FROM safe_parcel_lookup('PRC1001');


-- Test 2: The same malicious input.
-- Expected: Zero rows.
-- The entire input is now treated as a tracking number.

SELECT *
FROM safe_parcel_lookup(
    $input$' OR '1'='1' --$input$
);


-- ============================================================
-- PART 4: UPSERT - INSERT OR UPDATE
-- ============================================================

-- Demonstrate a repeatable customer insert.
-- The email column has a UNIQUE constraint.
-- If the email already exists, update the existing record.

INSERT INTO customers (full_name, email, phone)
VALUES (
    'Assignment Test Customer',
    'upsert-test@example.com',
    '9000000000'
)
ON CONFLICT (email)
DO UPDATE SET
    full_name = EXCLUDED.full_name,
    phone = EXCLUDED.phone;


-- Run the same UPSERT again.
-- It updates the existing record instead of creating a duplicate.

INSERT INTO customers (full_name, email, phone)
VALUES (
    'Assignment Test Customer',
    'upsert-test@example.com',
    '9000000000'
)
ON CONFLICT (email)
DO UPDATE SET
    full_name = EXCLUDED.full_name,
    phone = EXCLUDED.phone;


-- Verify that only one record exists for this email.

SELECT
    customer_id,
    full_name,
    email,
    phone
FROM customers
WHERE email = 'upsert-test@example.com';


-- ============================================================
-- END OF ASSIGNMENT DEMONSTRATION
-- ============================================================
