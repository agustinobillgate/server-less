

SELECT pid, usename, datname, client_addr, application_name, state, query_start, state_change
FROM pg_stat_activity
ORDER BY query_start DESC;






