# kafka-stream-ksqlDB


A. Kafka producer to push the data to a Kafka topic gradually from  "https://dummyjson.com/users'
-->attach on "kafka_producer.py" file

B. Transformation queries and materialized views

#1 Transformation query to extract id, first name and last name of users:

![image](https://user-images.githubusercontent.com/25885092/227249105-d4679452-93d4-4761-abe8-46ff5b45247c.png)

CREATE STREAM users_stream (id INT, firstName VARCHAR, lastName VARCHAR)
    WITH (kafka_topic='users', value_format='JSON');

CREATE STREAM users_name_stream AS 
    SELECT id, firstName, lastName 
    FROM users_stream
    EMIT CHANGES;
	
--> This query creates a stream named users_stream from the Kafka topic named users, and then creates another stream named users_name_stream which only selects the id, first name and last name of users from the users_stream stream.	
	
#2 Transformation query to filter users based on gender to only for "male":

![image](https://user-images.githubusercontent.com/25885092/227249228-a43f61eb-e83d-419f-a12a-8c653f019fd0.png)

CREATE STREAM users_age_stream AS 
    SELECT * 
    FROM users_stream 
    WHERE gender = 'male'
    EMIT CHANGES;
	
--> This query creates another stream named users_age_stream which only selects users whose age is greater than 30.	

#3 Materialized view query that extracts the id column and adds a new column called generation based on the age of each person:

![image](https://user-images.githubusercontent.com/25885092/227249330-74405c66-004d-4ac9-a223-7813619c5411.png)

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

C. consumer to pull the transformed data from a Kafka topic 'users'
-->attach on "kafka_consumer.py" file
