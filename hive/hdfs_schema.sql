CREATE EXTERNAL TABLE IF NOT EXISTS truncated_data (
unique_key string,
created_date string,
closed_date string,
agency string,
agency_name string,
complaint_type string,
descriptor string,
location_type string,
city string,
status string,
date_due string,
resolution_desc string,
date_resolution string,
latitude string,
longitude string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
"separatorChar" = ",",
"quoteChar" = '"',
"escapeChar" = '\\' )
STORED AS TEXTFILE
LOCATION '/user/w205/final_data';
