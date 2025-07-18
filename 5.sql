SELECT
    EXTRACT(HOUR FROM CAST(timestamp AS TIMESTAMP)) AS hour,
    COALESCE(SUM(CASE WHEN category = 'Home Goods' THEN amount END), 0) AS 'Home Goods',
    COALESCE(SUM(CASE WHEN category = 'Clothing' THEN amount END), 0) AS 'Clothing',
    COALESCE(SUM(CASE WHEN category = 'Electronics' THEN amount END), 0) AS 'Electronics'
FROM sales
WHERE category IN ('Home Goods', 'Clothing', 'Electronics')
GROUP BY hour
ORDER BY hour;
