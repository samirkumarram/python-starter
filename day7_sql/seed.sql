
-- Insert customers
INSERT INTO customers (full_name, email, phone)
VALUES
    ('Rahul Sharma', 'rahul@example.com', '9876543210'),
    ('Priya Das', 'priya@example.com', '9876543211'),
    ('Amit Kumar', 'amit@example.com', '9876543212'),
    ('Sneha Roy', 'sneha@example.com', '9876543213'),
    ('Arjun Singh', 'arjun@example.com', '9876543214');

-- Insert parcels
INSERT INTO parcels (
    sender_id, receiver_id, tracking_number,
    origin, destination, weight_kg, status
)
VALUES
    (1, 2, 'PRC1001', 'Kolkata', 'Bangalore', 2.50, 'IN_TRANSIT'),
    (2, 3, 'PRC1002', 'Delhi', 'Mumbai', 1.20, 'DELIVERED'),
    (3, 4, 'PRC1003', 'Asansol', 'Kolkata', 5.00, 'BOOKED'),
    (4, 1, 'PRC1004', 'Mumbai', 'Delhi', 3.75, 'OUT_FOR_DELIVERY'),
    (1, 5, 'PRC1005', 'Bangalore', 'Hyderabad', 0.80, 'DELIVERED');

-- Insert tracking history
INSERT INTO parcel_tracking (
    parcel_id, status, location, remarks
)
VALUES
    (1, 'BOOKED', 'Kolkata', 'Parcel booked'),
    (1, 'PICKED_UP', 'Kolkata', 'Parcel picked up'),
    (1, 'IN_TRANSIT', 'Bhubaneswar', 'Parcel in transit'),
    (2, 'BOOKED', 'Delhi', 'Parcel booked'),
    (2, 'DELIVERED', 'Mumbai', 'Successfully delivered'),
    (3, 'BOOKED', 'Asansol', 'Parcel booked'),
    (4, 'OUT_FOR_DELIVERY', 'Delhi', 'Out for delivery'),
    (5, 'DELIVERED', 'Hyderabad', 'Successfully delivered');


-- Insert hubs for existing parcels
INSERT INTO hubs (parcel_id, label, amount)
VALUES
    (1, 'NORTH', 500),
    (1, 'SOUTH', 700),
    (1, 'NORTH', 300),
    (2, 'EAST', 900),
    (2, 'WEST', 400),
    (3, 'NORTH', 1200),
    (4, 'SOUTH', 800),
    (4, 'WEST', 600);

-- Insert scan events for hubs
INSERT INTO scan_events (hub_id, event_type, scanned_at)
VALUES
    (1, 'ARRIVED', '2026-11-08 09:00:00+05:30'),
    (1, 'SORTED',  '2026-11-08 11:00:00+05:30'),
    (2, 'ARRIVED', '2026-11-08 10:00:00+05:30'),
    (2, 'DISPATCHED', '2026-11-08 14:00:00+05:30'),
    (3, 'ARRIVED', '2026-11-09 08:00:00+05:30'),
    (4, 'ARRIVED', '2026-11-09 09:00:00+05:30'),
    (4, 'SORTED', '2026-11-09 12:00:00+05:30'),
    (5, 'ARRIVED', '2026-11-10 10:00:00+05:30'),
    (6, 'ARRIVED', '2026-11-10 11:00:00+05:30'),
    (7, 'ARRIVED', '2026-11-10 12:00:00+05:30'),
    (8, 'ARRIVED', '2026-11-10 13:00:00+05:30');
