-- SQL Analysis Queries for Supply Chain Analytics
-- Note: Replace 'supply_chain_table' with the actual table name.

-- 1. Total Demand by Product & Category
SELECT 
    "Product ID",
    "Product Name",
    "Category",
    SUM("Demand (Units Sold)") AS Total_Demand
FROM supply_chain_table
GROUP BY 
    "Product ID", 
    "Product Name", 
    "Category"
ORDER BY 
    Total_Demand DESC;

-- 2. Monthly Demand Trends
-- Assuming date formatting for PostgreSQL. Use DATE_FORMAT(Date, '%Y-%m') for MySQL.
SELECT 
    TO_CHAR("Date", 'YYYY-MM') AS Month,
    SUM("Demand (Units Sold)") AS Monthly_Demand
FROM supply_chain_table
GROUP BY 
    TO_CHAR("Date", 'YYYY-MM')
ORDER BY 
    Month ASC;

-- 3. Inventory Levels by Warehouse
SELECT 
    "Warehouse", 
    SUM("Inventory Level") AS Total_Inventory
FROM supply_chain_table
GROUP BY 
    "Warehouse"
ORDER BY 
    Total_Inventory DESC;

-- 4. Stock-Out Frequency
SELECT 
    "Product ID", 
    "Product Name",
    COUNT(*) AS StockOut_Days
FROM supply_chain_table
WHERE 
    "Stock Status" = 'Out of Stock'
GROUP BY 
    "Product ID", 
    "Product Name"
ORDER BY 
    StockOut_Days DESC;

-- 5. Reorder Analysis (below reorder point)
SELECT 
    "Date",
    "Product ID", 
    "Product Name",
    "Warehouse",
    "Inventory Level", 
    "Reorder Point"
FROM supply_chain_table
WHERE 
    "Inventory Level" < "Reorder Point"
ORDER BY 
    "Date" DESC, "Inventory Level" ASC;

-- 6. Supplier Performance (Lead time analysis)
SELECT 
    "Supplier ID",
    AVG("Lead Time (days)") AS Average_Lead_Time,
    MAX("Lead Time (days)") AS Max_Lead_Time,
    MIN("Lead Time (days)") AS Min_Lead_Time
FROM supply_chain_table
GROUP BY 
    "Supplier ID"
ORDER BY 
    Average_Lead_Time ASC;
