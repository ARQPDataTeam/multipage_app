import dash
from dash import Dash, html, dcc, callback 
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime as dt
from datetime import date
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os
from dotenv import load_dotenv 

from pages.credentials import sql_engine_string_generator

# register this as a page in the app
dash.register_page(__name__)

# set the sql engine string
sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_DCP_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
sql_engine=create_engine(sql_engine_string)


# sql query
sql_query="""
select siteid, description, latitude, longitude, groundelevation from stations where projectid = 'SWAPIT' ;
"""
# create the dataframe from the sql query
stations_df=pd.read_sql_query(sql_query, con=sql_engine)

print (stations_df)

