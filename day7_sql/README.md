# Day 7 – PostgreSQL and SQL Exercises

## Project
Parcel Management System

## Overview
This assignment demonstrates PostgreSQL database setup using Docker, relational database design, SQL queries, indexing, SQL injection prevention, and UPSERT operations.

## Database Tables
- `customers` – Stores customer information.
- `parcels` – Stores parcel information.
- `parcel_tracking` – Stores parcel movement history.
- `hubs` – Stores hub records associated with parcels.
- `scan_events` – Stores scan events for each hub.

## Files
- `schema.sql` – Creates tables, constraints, foreign keys, and indexes.
- `seed.sql` – Inserts sample customers and parcels.
- `seed_hubs.sql` – Inserts sample hubs and scan events.
- `exercises.sql` – Contains the eight SQL exercises.
- `security_and_performance.sql` – Demonstrates EXPLAIN, SQL injection, parameterized queries, and UPSERT.

## Technologies
- Docker
- PostgreSQL 17
- SQL
- Ubuntu on WSL

## Running the Project

Start the PostgreSQL container:

```bash
docker start rag-postgres
```

Connect to the database:

```bash
docker exec -it rag-postgres psql -U raguser -d ragdb
```

Execute SQL files from the PostgreSQL prompt:

```sql
\i /tmp/schema.sql
\i /tmp/seed.sql
\i /tmp/seed_hubs.sql
\i /tmp/exercises.sql
\i /tmp/security_and_performance.sql
```

The SQL files must first be copied into the container using `docker cp`, as shown in the project setup instructions.

## Key Concepts Practised

- Primary keys and foreign keys
- Unique and CHECK constraints
- INNER JOIN and LEFT JOIN
- GROUP BY, HAVING and aggregate functions
- Window functions: ROW_NUMBER and RANK
- Common Table Expressions (CTEs)
- EXPLAIN and EXPLAIN ANALYZE
- Database indexing
- SQL injection demonstration
- Parameterized queries
- UPSERT using ON CONFLICT

## Docker Persistence

PostgreSQL data is stored in the named volume `rag_postgres_data`, allowing database data to persist across container stops and starts.