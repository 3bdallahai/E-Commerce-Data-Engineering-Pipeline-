UPDATE o
SET o.total_amount = subquery.calculated_total
FROM sales.orders o
JOIN (
    SELECT order_id, SUM(quantity * unit_price) AS calculated_total
    FROM sales.order_items
    GROUP BY order_id
) subquery ON o.order_id = subquery.order_id;