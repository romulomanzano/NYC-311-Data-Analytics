# NYC 311 Data Quickstart

This README file includes instructions to replicate our process.

The final results are available here:

http://people.ischool.berkeley.edu/~samuel.goodgame/311/

# Part I: Static Data Transformation with Hive

This section covers how to pull a very large .csv file out of the NYC OpenData website, impose schema on it, and manipulate it in Hive.

## Environment Setup and Acquiring the Data

1. Launch and start an AWS EC2 instance with Hadoop, Hive, HDFS, and PostgreSQL. The AMI **ami-be0d5fd4** has everything necessary for the project. Instructions can be found [here](https://github.com/UC-Berkeley-I-School/w205-summer-17-labs-exercises/blob/master/lab_1/Lab1-w205.md) and [here](https://github.com/UC-Berkeley-I-School/w205-summer-17-labs-exercises/blob/master/lab_2/Lab2.md).

2. Create the following open TCP ports on `0.0.0.0/0`  (all ip addresses, in practice you will want to limit this to as neccessary)

- 22 (SSH)
- 7180 (Cloudera Manager)
- 8080 (Webserver)
- 10000 (Hive)
- 50070 (Hadoop)

3. Navigate to the /data directory.

4. Download the data. This data is a slightly modified version of the full dataset that does not include all of the fields (and is therefore more manageable): `$ wget https://data.cityofnewyork.us/api/views/dbhh-68ph/rows.csv?accessType=DOWNLOAD`

5. Strip the headers from your data (necessary for Hive): `$ tail -n +2 311_data.csv > 311_data_no_headers.csv`

6. Change the user to w205 (if you're using the UCB AMI): `$  su - w205`

7. Make a directory in HDFS for your data: `$ hdfs dfs -mkdir /user/w205/final_data`

8. Put your new .csv file into HDFS: `$ hdfs dfs -put 311_data_no_headers.csv /user/w205/final_data`

## Imposing schema

1. Enter Hive: `$ hive`

2. Load the data into HDFS with the found in this repository's /hive directory under *hdfs_schema.sql*.

## Transform the data

Within Hive, run transformations that output aggregations of the total table. There are four Hive SQL scripts located within the /hive directory of this repository; run each of them to produce four separate tables:
- avg_complaint_coords.sql
- complaints_by_type_by_city.sql
- least_common_complaints.sql
- top_topp_complaint_types.sql

While still in the Hive interpreter, enter `$ show tables` to confirm that the tables exist. You can also query the first few line of each table to inspect the data with a query like `$ SELECT * FROM avg_complaint_coords LIMIT 10`.

## Visualize the Data in Tableau

1. Within your EC2 instance, run the following command: `hive --service hiveserver2 --hiveconf hive.server2.thrift.port=10000 &`. This ensures that Tableau will be able to read from your Hive tables.

2. Download Tableau Desktop [here](https://www.tableau.com/products/desktop). You can use a free trial if needed. Tableau also has free options for students.

3. Within Tableau, connect to a new data source. Select *Cloudera Hadoop* as the data source type. Enter your EC2 server connection information for *Server*, "HiveServer2" for *Type*, and use whatever username you used to create the Hive tables.

4. Once the connection is successful, enter **default** for "schema" and select enter. You should see a text field for entering tables; type one of your tables exactly as it exists in hive (e.g., *"avg_complaint_coords"*.)

5. Drag your table into the data window, and begin creating visualizations! You can see examples of the ones we've made on our [website](http://people.ischool.berkeley.edu/~samuel.goodgame/311/).

# Part II: Socrata 311 API

Python libraries to pull incremental 311 data from the Socrata Open Data API


## Background

For the purpose of refreshing our data on a daily basis, we decided to leverage the existing SODA Consumer API to pull the daily updates registered in the NYC 311 data set.

The goal was to be able to abstract some of the logic needed to produce the data needed for our various reports in the form of simple, callable methods as well as passing on some of the data manipulation load into the hosting service (thus saving storage and compute power on our end ) .

Similarly, the abstraction allow us to further refine the logic to transform the data pulled from the api with minimal disruption to the consumption layer of our data (for the purposes of this project Tableau or direct function calls on Python)

## Requirements

At its core, this library depends heavily on the 'sodapy' and 'requests' Python packages.

## Documentation

The [official Socrata API docs](http://dev.socrata.com/) provide thorough documentation of the available methods, however,the set of methods written cater exclusively towards the NYC 311 dataset, which is fully documented [here](https://dev.socrata.com/foundry/data.cityofnewyork.us/fhrw-4uyv).

## Package Structure

- [settings](#settings)
- [etl](#etl)
- [etl_settings](#etl_settings)
- [api](#api)


### settings

Primarily created to host a few constants referenced through the package. Includng:

- APP_TOKEN_311: api token generated when registering an app in socrata. This is a private token currently being shared as part of the project. It will be deactivated/decomissioned after September 15th for obvious reasons!

- APP_NYC_DATASET: this is Socrata's dataset key. Static, no need to change

- APP_NYC_API_DOMAIN: this is Socrata's api domain url. Static, no need to change

### etl

This module hosts a handful of methods used to extend the data pulled from the api with additional attributes needed for 'time to closure' analysis.

### etl_settings

Holds a couple of simple settings needed to standardize the data before exporting (when needed needed)

### api

- pull_data_modified_since:

Can be used to simply pull data modified in Socrata since a given timestamp

- pull_data_created_since

Can be used to simply pull data created in Socrata since a given timestamp

- pull_agg_closure_statistics_created_since:

The main purpose of this method is to return the percentage closure stats for a given group key (list of fields to group by). The scope is all records created since the passed timestamp

- pull_raw_time_to_closure_statistics_created_since_closed_only

Not widely used due to the vasts amounts of data pulled (not restrictive enough).  This method essentially pulls all the raw data (at the service request level) created since a given timestamp and calculates the time to closure metrics.


- pull_agg_time_to_closure_statistics_created_since_closed_only

This method calculates the average time to closure per group key for all complaints received since the desired timestamp

- pull_full_closure_statistics_since_date

This method calculates the average time to closure per group key for all complaints received since the desired timestamp and combines it with the percentage closed ratio metrics

- pull_full_closure_statistics_since_x_weeks

This method calculates the average time to closure per group key for all complaints received since the desired number of weeks (in the past) and combines it with the percentage closed ratio metrics


- pull_daily_closure_statistics_since_x_weeks

This method returns groupings of the passed key (granularity) and number of days to closure, the main idea is to use it to generate histograms and dive into a specific type of complaints

- pull_closed_within_a_day_stats_since_x_weeks

This method returns the ratio of complaints closed within a day


## How to run a test data pull

See 'run_data_socrata_api.py' script for three sample calls to relevant package methods. The examples pull data and calculate relevant metrics for a window of 12 weeks since call time.

## Intended use in future work

This package lays the foundation for future work on generating actionable insights on the 311. The recommended next steps are to leverage these methods to refresh (1) the life-to-date hdfs files used for broader tableau reporting as wel as (2) persisting the aggregated results in a PostgreSql instance so as to maintain a live connection with the reporting layer (Tableau) and be able to take daily snapshots and perform time series analysis on time to closure.
