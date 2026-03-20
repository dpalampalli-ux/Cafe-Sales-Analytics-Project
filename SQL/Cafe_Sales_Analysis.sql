SELECT ROUND(SUM(total_spent), 2) AS total_revenue
FROM cleaned_cafe_sales;

SELECT item,
       ROUND(SUM(total_spent), 2) AS item_revenue
FROM cleaned_cafe_sales
GROUP BY item
ORDER BY item_revenue DESC;

SELECT payment_method,
       ROUND(SUM(total_spent), 2) AS revenue
FROM cleaned_cafe_sales
GROUP BY payment_method
ORDER BY revenue DESC;

SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month,
       ROUND(SUM(total_spent), 2) AS monthly_revenue
FROM cleaned_cafe_sales
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
ORDER BY month;