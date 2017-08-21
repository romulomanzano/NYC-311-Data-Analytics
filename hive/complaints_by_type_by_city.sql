CREATE TABLE top_complaints_by_city AS
SELECT
  city,
  complaint_type,
  count(complaint_type) AS number_occurrances
FROM
  truncated_data
GROUP BY city, complaint_type
ORDER BY number_occurrances DESC;
