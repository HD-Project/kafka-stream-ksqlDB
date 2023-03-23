--#1 Transformation query to extract id, first name and last name of users:

CREATE STREAM users_stream (id INT, firstName VARCHAR, lastName VARCHAR)
    WITH (kafka_topic='users', value_format='JSON');

CREATE STREAM users_name_stream AS 
    SELECT id, firstName, lastName 
    FROM users_stream
    EMIT CHANGES;
	
--> This query creates a stream named users_stream from the Kafka topic named users, and then creates another stream named users_name_stream which only selects the id, first name and last name of users from the users_stream stream.	
	
--#2 Transformation query to filter users based on gender to only for "male":

CREATE STREAM users_age_stream AS 
    SELECT * 
    FROM users_stream 
    WHERE gender = 'male'
    EMIT CHANGES;
	
--> This query creates another stream named users_age_stream which only selects users whose age is greater than 30.	

--#3 Materialized view query that extracts the id column and adds a new column called generation based on the age of each person:

CREATE MATERIALIZED VIEW people_with_generation AS
SELECT id, 
  CASE 
    WHEN age < 26 THEN 'Gen Z'
    WHEN age BETWEEN 27 AND 42 THEN 'Millennials'
    WHEN age BETWEEN 43 AND 58 THEN 'Gen X'
    WHEN age > 59 THEN 'Boomers'
    ELSE NULL
  END AS generation
FROM people;

--> This will create a materialized view called people_with_generation that contains the id column from the original people table and a new generation column based on the age of each person. The generation column will have one of four possible values: "Gen Z", "Millennials", "Gen X", or "Boomers".