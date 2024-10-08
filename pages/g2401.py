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

from credentials import sql_engine_string_generator

# register this as a page in the app
dash.register_page(__name__,
    requests_pathname_prefix="/webapp-SWAPIT/",
    routes_pathname_prefix="/webapp-SWAPIT/"
)

print ('plotting g2401')

# set some default date limits for the sql query
# default_ending_date=dt.today().strftime('%Y-%m-%d') # for future instruments running currently
default_ending_date_string='2024-03-07' # just for swapit
default_ending_date=dt.strptime(default_ending_date_string, "%Y-%m-%d")
# default_beginning_date=(dt.today()-dt.timedelta(days=7)).strftime('%Y-%m-%d') # for future instruments running currently
default_beginning_date_string='2024-03-06'
default_beginning_date=dt.strptime(default_beginning_date_string, "%Y-%m-%d")

# set the sql engine string
sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_SWAPIT_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')
sql_engine=create_engine(sql_engine_string)


# sql query
sql_query=("""
SET TIME ZONE 'GMT';
SELECT DISTINCT ON (datetime) * FROM (
	SELECT date_trunc('minute',datetime) AS datetime, co_r AS co, co2_r/1e3 AS co2, ch4_r AS ch4
	FROM cru__g2401m_v0
	WHERE co_r IS NOT NULL
	AND datetime >= '{}' AND datetime < '{}'
) AS g2401_
ORDER BY datetime;
""").format(default_beginning_date_string,default_ending_date_string)

# create the dataframe from the sql query
g2401_output_df=pd.read_sql_query(sql_query, con=sql_engine)

# print (g2401_output_df)

g2401_output_df.set_index('datetime', inplace=True)
g2401_output_df.index=pd.to_datetime(g2401_output_df.index)

# print(beginning_date, ending_date)
# use specs parameter in make_subplots function
# to create secondary y-axis


# plot a scatter chart by specifying the x and y values
# Use add_trace function to specify secondary_y axes.
def create_figure(g2401_output_df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=g2401_output_df.index, y=g2401_output_df['co'], name="CO"),
        secondary_y=False)
    
    # Use add_trace function and specify secondary_y axes = True.
    fig.add_trace(
        go.Scatter(x=g2401_output_df.index, y=g2401_output_df['ch4'], name="CH4"),
        secondary_y=True,)

    # set axis titles
    fig.update_layout(
        template='simple_white',
        title='Cruiser G2401 Data',
        xaxis_title="Date",
        yaxis_title="CO",
        yaxis2_title="CH4",
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
                    html.H1(children=['SWAPIT Cruiser G2401 Dashboard']),
                    html.Div(children=['Cruiser G2401 plot display with date picker']),

                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=default_beginning_date,
                        max_date_allowed=default_ending_date
                    ),
                    dcc.Graph(id='cru-g2401-plot',figure=create_figure(g2401_output_df)),
                    
                    ] 
                    )

# @app.callback(
#     Output('graph_2', 'figure'),
#     [Input('date-picker', 'start_date'),
#     Input('date-picker', 'end_date')],
#     [State('submit_button', 'n_clicks')])

@callback(
    Output('cru-g2401-plot', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))

def update_output(start_date, end_date):
    print (start_date, end_date)
    if not start_date or not end_date:
        raise PreventUpdate
    else:
        output_selected_df = g2401_output_df.loc[
            (g2401_output_df.index >= start_date) & (g2401_output_df.index <= end_date), :
        ]
        return create_figure(output_selected_df)


# if __name__=='__main__':
#     app.run(debug=True)
