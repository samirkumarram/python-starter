
-- Q1: First 10 active parcels, newest first
SELECT *
FROM parcels
WHERE active = TRUE
ORDER BY created_at DESC, parcel_id DESC
LIMIT 10;


-- Q2: Count parcels per status
SELECT status, COUNT(*) AS total_parcels
FROM parcels
GROUP BY status
ORDER BY status;


-- Q3: Show each hub with its parent parcel name
SELECT
    h.*,
    p.name AS parcel_name
FROM hubs h
JOIN parcels p ON h.parcel_id = p.parcel_id;


-- Q4: Find parcels having more than 2 hubs
SELECT
    p.parcel_id,
    p.name,
    COUNT(h.hub_id) AS total_hubs
FROM parcels p
JOIN hubs h ON p.parcel_id = h.parcel_id
GROUP BY p.parcel_id, p.name
HAVING COUNT(h.hub_id) > 2;


-- Q5: Find parcels having no hubs
SELECT p.*
FROM parcels p
LEFT JOIN hubs h ON p.parcel_id = h.parcel_id
WHERE h.hub_id IS NULL;


-- Q6: Total amount per label, only above 1000
SELECT
    label,
    SUM(amount) AS total_amount
FROM hubs
GROUP BY label
HAVING SUM(amount) > 1000;


-- Q7: Rank hubs by amount within each parcel
SELECT
    parcel_id,
    hub_id,
    label,
    amount,
    RANK() OVER (
        PARTITION BY parcel_id
        ORDER BY amount DESC
    ) AS amount_rank
FROM hubs;


-- Q8: Latest scan event for every hub using a CTE
WITH ranked_events AS (
    SELECT
        scan_event_id,
        hub_id,
        event_type,
        scanned_at,
        ROW_NUMBER() OVER (
            PARTITION BY hub_id
            ORDER BY scanned_at DESC, scan_event_id DESC
        ) AS row_num
    FROM scan_events
)
SELECT
    h.hub_id,
    h.parcel_id,
    h.label,
    re.event_type AS latest_event,
    re.scanned_at AS latest_scan_time
FROM hubs h
LEFT JOIN ranked_events re
    ON h.hub_id = re.hub_id
    AND re.row_num = 1
ORDER BY h.hub_id;
