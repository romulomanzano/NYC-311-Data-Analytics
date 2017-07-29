# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 17:38:29 2017

@author: romulo
"""
import pandas as pd
from . import etl_settings

def flatten_response_list(data, restrict_columns = False,cols = etl_settings.RESPONSE_COL_REQUIRED):
    frame = pd.DataFrame(data)
    if (restrict_columns):
        return frame[cols]
    return frame

