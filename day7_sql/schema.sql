CREATE TABLE IF NOT EXISTS customers (
    customer_id  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    phone VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parcels (
    parcel_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sender_id BIGINT NOT NULL REFERENCES customers(customer_id),
    receiver_id BIGINT NOT NULL REFERENCES customers(customer_id),
    tracking_number VARCHAR(50) NOT NULL UNIQUE,
    origin VARCHAR(150) NOT NULL,
    destination VARCHAR(150) NOT NULL,
    weight_kg NUMERIC(8, 2) NOT NULL CHECK (weight_kg > 0),
    status VARCHAR(30) NOT NULL DEFAULT 'BOOKED'
        CHECK (status IN (
            'BOOKED',
            'PICKED_UP',
            'IN_TRANSIT',
            'OUT_FOR_DELIVERY',
            'DELIVERED',
            'CANCELLED'
        )),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS parcel_tracking (
    tracking_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    parcel_id BIGINT NOT NULL REFERENCES parcels(parcel_id)
        ON DELETE CASCADE,
    status VARCHAR(30) NOT NULL
        CHECK (status IN (
            'BOOKED',
            'PICKED_UP',
            'IN_TRANSIT',
            'OUT_FOR_DELIVERY',
            'DELIVERED',
            'CANCELLED'
        )),
    location VARCHAR(150) NOT NULL,
    remarks TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_parcels_sender_id
    ON parcels(sender_id);

CREATE INDEX IF NOT EXISTS idx_parcels_receiver_id
    ON parcels(receiver_id);

CREATE INDEX IF NOT EXISTS idx_parcel_tracking_parcel_id
    ON parcel_tracking(parcel_id);

CREATE INDEX IF NOT EXISTS idx_parcel_tracking_updated_at
    ON parcel_tracking(updated_at);


-- Add columns required by the SQL exercises
ALTER TABLE parcels
ADD COLUMN IF NOT EXISTS name VARCHAR(100);

ALTER TABLE parcels
ADD COLUMN IF NOT EXISTS active BOOLEAN NOT NULL DEFAULT TRUE;

-- Populate names for existing parcels
UPDATE parcels
SET name = tracking_number
WHERE name IS NULL;

ALTER TABLE parcels
ALTER COLUMN name SET NOT NULL;


-- Hubs table
CREATE TABLE IF NOT EXISTS hubs (
    hub_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    parcel_id BIGINT NOT NULL REFERENCES parcels(parcel_id)
        ON DELETE CASCADE,
    label VARCHAR(100) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Scan events table
CREATE TABLE IF NOT EXISTS scan_events (
    scan_event_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hub_id BIGINT NOT NULL REFERENCES hubs(hub_id)
        ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    scanned_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- Indexes for relationships and common queries
CREATE INDEX IF NOT EXISTS idx_hubs_parcel_id
    ON hubs(parcel_id);

CREATE INDEX IF NOT EXISTS idx_scan_events_hub_id
    ON scan_events(hub_id);

CREATE INDEX IF NOT EXISTS idx_scan_events_latest
    ON scan_events(hub_id, scanned_at DESC, scan_event_id DESC);

CREATE INDEX IF NOT EXISTS idx_parcels_active_created_at
    ON parcels(active, created_at DESC);
