# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 21:52:56 2017

@author: romulo
"""
from sodapy import Socrata
from . import settings
import pandas as pd

# =============================================================================
#   receives a date object or timestamp in isoformat
#   an existing connection is optional, can create a new one
#   beware of the restrictive optional parameters (timeout, data limit)
# =============================================================================
def pull_data_modified_since(since,client=None,timeout = 120,data_limit = 10000):
    if (client == None):
        client = Socrata(settings.APP_NYC_API_DOMAIN ,settings.APP_TOKEN_311,timeout=timeout)
    data = client.get(settings.APP_NYC_DATASET,limit = data_limit,where = "resolution_action_updated_date >= '"+str(since)+"'")
    return data

# =============================================================================
#   receives a date object or timestamp in isoformat
#   an existing connection is optional, can create a new one
#   beware of the restrictive optional parameters (timeout, data limit)
# =============================================================================
def pull_data_created_since(since,client=None,timeout = 120,data_limit = 10000):
    if (client == None):
        client = Socrata(settings.APP_NYC_API_DOMAIN ,settings.APP_TOKEN_311,timeout=timeout)
    data = client.get(settings.APP_NYC_DATASET,limit = data_limit,where = "created_date>= '"+str(since)+"'")
    return data


# =============================================================================
#   receives a date object or timestamp in isoformat
#   an existing connection is optional, can create a new one
#   beware of the restrictive optional parameters (timeout, data limit)
# =============================================================================
def pull_agg_closure_statistics_created_since(since,client=None,timeout = 120):
    if (client == None):
        client = Socrata(settings.APP_NYC_API_DOMAIN ,settings.APP_TOKEN_311,timeout=timeout)
    data = client.get(settings.APP_NYC_DATASET,query = "select agency, " \
                                                       "count(*) as total, " \
                                                       "sum(case(status='Closed',1,true,0)) as closed " \
                                                       "where created_date>= '"+str(since)+"' "
                                                        "group by agency""")

    dataFrame= pd.DataFrame.from_dict(data)
    dataFrame['perc_closed'] = (dataFrame['closed'].astype('float') / dataFrame['total'].astype('float'))

    return dataFrame