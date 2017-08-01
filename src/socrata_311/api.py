# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 21:52:56 2017

@author: romulo
"""
from sodapy import Socrata
from . import settings

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
