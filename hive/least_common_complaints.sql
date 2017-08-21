CREATE TABLE least_common_complaints AS
SELECT
  complaint_type,
  count(complaint_type) AS number_occurrances,
  avg(cast(latitude AS DOUBLE)) AS avg_lat,
  avg(cast(longitude AS DOUBLE)) AS avg_lon
FROM
  truncated_data
GROUP BY complaint_type
ORDER BY number_occurrances ASC
LIMIT 150;
