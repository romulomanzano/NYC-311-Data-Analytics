
# Socrata 311 API

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
