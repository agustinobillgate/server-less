SELECT 
    DATE(time_start) AS log_date,
    endpoint,
    COUNT(*) AS total_errors
FROM logs_endpoint
WHERE error_message <> ''
GROUP BY DATE(time_start), endpoint
ORDER BY log_date DESC, total_errors DESC LIMIT 50