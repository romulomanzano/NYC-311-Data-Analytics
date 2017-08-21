CREATE TABLE avg_complaint_coords AS
SELECT
  complaint_type,
  avg(cast(latitude AS DOUBLE)) AS avg_lat,
  avg(cast(longitude AS DOUBLE)) AS avg_lon
FROM
  truncated_data
GROUP BY complaint_type;
