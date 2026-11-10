
-- Insert sample hubs and safely handle re-runs.
INSERT INTO hubs (parcel_id, label, amount)
VALUES
    (1, 'NORTH', 500),
    (1, 'SOUTH', 700),
    (1, 'NORTH', 300),
    (2, 'EAST', 900),
    (2, 'WEST', 400),
    (3, 'NORTH', 1200),
    (4, 'SOUTH', 800),
    (4, 'WEST', 600)
ON CONFLICT (hub_id) DO NOTHING;

-- Insert sample scan events.
-- Prevent duplicate sample events using a unique constraint
-- in the next schema improvement if this seed needs rerunning.
INSERT INTO scan_events (hub_id, event_type, scanned_at)
VALUES
    (1, 'ARRIVED', '2026-11-08 09:00:00+05:30'),
    (1, 'SORTED', '2026-11-08 11:00:00+05:30'),
    (2, 'ARRIVED', '2026-11-08 10:00:00+05:30'),
    (2, 'DISPATCHED', '2026-11-08 14:00:00+05:30'),
    (3, 'ARRIVED', '2026-11-09 08:00:00+05:30'),
    (4, 'ARRIVED', '2026-11-09 09:00:00+05:30'),
    (4, 'SORTED', '2026-11-09 12:00:00+05:30'),
    (5, 'ARRIVED', '2026-11-10 10:00:00+05:30'),
    (6, 'ARRIVED', '2026-11-10 11:00:00+05:30'),
    (7, 'ARRIVED', '2026-11-10 12:00:00+05:30'),
    (8, 'ARRIVED', '2026-11-10 13:00:00+05:30');
