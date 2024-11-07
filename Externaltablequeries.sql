
SELECT TOP 10 * FROM customer;

--query 1
SELECT CustomerID, FirstName, LastName, Title 
FROM customer
WHERE Title = '"Mr."';


--query 2
SELECT COUNT(*) AS NumberOfCustomers
FROM customer
WHERE NameStyle = 'False';


--query 3
SELECT CustomerID, FirstName, LastName, Phone 
FROM customer
WHERE Phone LIKE '"%555-0127"';


--query 4
SELECT CustomerID, FirstName, LastName, ModifiedDate 
FROM customer
WHERE ModifiedDate > '"2006-01-01"';

--query 5
SELECT CustomerID, FirstName, LastName 
FROM customer
ORDER BY LastName ASC;

--query 6
SELECT CustomerID, FirstName, LastName, SalesPerson 
FROM customer
WHERE SalesPerson = '"adventure-works\pamela0"';