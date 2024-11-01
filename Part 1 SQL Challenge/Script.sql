-- Query 1: Calculate Total Revenue
-- This query calculates the sum of total amount for all trips in January 2024
-- Provides an overall revenue figure for the entire dataset
SELECT SUM(Total_amount) AS total_revenue 
FROM "yellow_tripdata_2024-01";

-- Query 2: Top 3 Locations by Revenue
-- Identifies the top 3 pickup locations with the highest total revenue
-- Groups trips by pickup location ID
-- Sorts locations in descending order of revenue
-- Limits output to top 3 most profitable locations
SELECT PULocationID, SUM(Total_amount) AS revenue 
FROM "yellow_tripdata_2024-01"  
GROUP BY PULocationID 
ORDER BY revenue DESC 
LIMIT 3; 

-- Query 3: Revenue for All Pickup Locations
-- Calculates total revenue for each pickup location
-- Provides a comprehensive view of revenue distribution across all locations
-- I used this due to limiation in memeory then continued in excel
-- SELECT PULocationID, SUM(Total_amount) AS revenue 
-- FROM "yellow_tripdata_2024-01" 
-- GROUP BY PULocationID;


-- Query 4: Locations with More Than 5 Total Passengers
-- Finds pickup locations with more than 5 total passengers
-- Useful for identifying high-traffic pickup points
-- Uses HAVING clause to filter after aggregation
SELECT PULocationID, SUM(Passenger_count) AS total_passengers 
FROM "yellow_tripdata_2024-01" 
GROUP BY PULocationID 
HAVING total_passengers > 5;

