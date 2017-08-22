# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 14:34:41 2017

"""

from socrata_311 import api

numberOfWeeks = 12

metricsSince12Weeks = api.pull_full_closure_statistics_since_x_weeks(numberOfWeeks ,group_key = ['agency','complaint_type'])
daysToClosureStatsComplaintDOB= api.pull_daily_closure_statistics_since_x_weeks(numberOfWeeks ,group_key = ['agency','complaint_type','borough']
                                                                                     ,restrict_clause = " agency = 'DOB' and borough = 'STATEN ISLAND' ")
closedWithinADayStats = api.pull_closed_within_a_day_stats_since_x_weeks(numberOfWeeks,group_key = ['agency','complaint_type','borough']
                                                                         ,restrict_clause = " agency = 'DOB' ")

#Writing to CSVs to can work on a mockup dashboard:
metricsSince12Weeks.to_csv('aggregated_time_to_closure_metrics.csv')
daysToClosureStatsComplaintDOB.to_csv('days_to_closure_stats_by_complaint_dob_hist_one_borough.csv')
closedWithinADayStats.to_csv('aggregated_closed_within_a_day_stats.csv')


print('Complete')