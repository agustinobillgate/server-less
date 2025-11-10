SELECT
    n.nspname AS schema_name,
    pg_size_pretty(SUM(pg_total_relation_size(c.oid))) AS size_pretty,
    SUM(pg_total_relation_size(c.oid)) AS size_bytes
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
  AND c.relkind IN ('r','m','p')  -- tables, matviews, partitioned tables
GROUP BY n.nspname
ORDER BY SUM(pg_total_relation_size(c.oid)) DESC;