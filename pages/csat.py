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

print ('plotting csat')

# register this as a page in the app
dash.register_page(__name__)

# set the sql engine string
sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_SWAPIT_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
sql_engine=create_engine(sql_engine_string)


# sql query
sql_query="""
SET TIME ZONE 'GMT';
SELECT DISTINCT ON (datetime) * FROM (
	SELECT date_trunc('minute',datetime) AS datetime, ws_u AS u, ws_v AS v, vtempa AS vtemp
	FROM cru__csat_v0
	WHERE ws_u IS NOT NULL
	AND datetime >= '2024-03-01' AND datetime < '2024-03-01 01:00:00'
) AS csat
ORDER BY datetime;
"""

# create the dataframe from the sql query
csat_output_df=pd.read_sql_query(sql_query, con=sql_engine)

# print (csat_output_df)

csat_output_df.set_index('datetime', inplace=True)
csat_output_df.index=pd.to_datetime(csat_output_df.index)
beginning_date=csat_output_df.index[0]
ending_date=csat_output_df.index[-1]
today=dt.today().strftime('%Y-%m-%d')
# print(beginning_date, ending_date)
# use specs parameter in make_subplots function
# to create secondary y-axis


# plot a scatter chart by specifying the x and y values
# Use add_trace function to specify secondary_y axes.
def create_figure(csat_output_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=csat_output_df.index, y=csat_output_df['u'], name="U Wind Speed"),
        secondary_y=False)
    
    # Use add_trace function and specify secondary_y axes = True.
    fig.add_trace(
        go.Scatter(x=csat_output_df.index, y=csat_output_df['v'], name="V Wind Speed"),
        secondary_y=False,)

    fig.add_trace(
        go.Scatter(x=csat_output_df.index, y=csat_output_df['vtemp'], name="Virt Temp"),
        secondary_y=True,)

    # set axis titles
    fig.update_layout(
        template='simple_white',
        title='CRU CSAT Data',
        xaxis_title="Date",
        yaxis_title="Winds (m/s)",
        yaxis2_title="Virt Temp (C)",
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    )   
    )
    return fig

# set up the app layout
layout = html.Div(children=
                    [
                    html.H1(children=['SWAPIT Cruiser CSAT Dashboard']),
                    html.Div(children=['CSAT Met plot display with date picker']),

                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=beginning_date,
                        max_date_allowed=ending_date
                    ),
                    dcc.Graph(id='cru-csat-plot',figure=create_figure(csat_output_df)),
                    
                    ] 
                    )

# @app.callback(
#     Output('graph_2', 'figure'),
#     [Input('date-picker', 'start_date'),
#     Input('date-picker', 'end_date')],
#     [State('submit_button', 'n_clicks')])

@callback(
    Output('cru-csat-plot', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def update_output(start_date, end_date):
    print (start_date, end_date)
    if not start_date or not end_date:
        raise PreventUpdate
    else:
        output_selected_df = csat_output_df.loc[
            (csat_output_df.index >= start_date) & (csat_output_df.index <= end_date), :
        ]
        return create_figure(output_selected_df)


# if __name__=='__main__':
#     app.run(debug=True)
