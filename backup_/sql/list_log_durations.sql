SELECT 
    id, hotel_schema, endpoint,
    time_start,
    time_end,
    EXTRACT(EPOCH FROM (time_end - time_start)) AS duration
FROM logs_endpoint
WHERE endpoint = 'vhpFOC/naStart2'
  AND EXTRACT(EPOCH FROM (time_end - time_start)) > 0
ORDER BY time_start DESC
LIMIT 10