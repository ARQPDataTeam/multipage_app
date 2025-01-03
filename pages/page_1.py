import dash
from dash import Dash, html, dcc, callback 
from dash.exceptions import PreventUpdate
from datetime import datetime as dt
from datetime import timedelta as td
from dash.dependencies import Input, Output

# local modules
from postgres_query import fig_generator
from credentials import sql_engine_string_generator

# register this as a page in the app
dash.register_page(__name__)
# generate the sql connection string
sql_engine_string=sql_engine_string_generator('DATAHUB_PSQL_SERVER','DATAHUB_BORDEN_DBNAME','DATAHUB_PSQL_USER','DATAHUB_PSQL_PASSWORD')

# set datetime parameters
first_date='2024-01-01'
now=dt.today()
start_date=(now-td(days=1)).strftime('%Y-%m-%d')
end_date=now.strftime('%Y-%m-%d')

# set up the app layout
layout = html.Div(children=
                    [
                    html.H1('BORDEN DASHBOARD', style={'textAlign': 'center'}),
                    html.H3('Pick the desired date range.  This will apply to all plots on the page.'),
                    dcc.DatePickerRange(
                        id='date-picker',
                        min_date_allowed=first_date,
                        max_date_allowed=end_date,
                        display_format='YYYY-MM-DD'
                    ),
                    html.H2('Borden CR3000 Temperatures Display'),
                    dcc.Graph(id='plot_1',figure=fig_generator(start_date,end_date,'plot_1',sql_engine_string)),
                    html.Br(),
                    html.H2(children=['Borden CSAT Temperatures Display']),
                    dcc.Graph(id='plot_2',figure=fig_generator(start_date,end_date,'plot_2',sql_engine_string))
                    ] 
                    )

@callback(
    Output('plot_1', 'figure'),
    Output('plot_2', 'figure'),
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'))

def update_output(start_date,end_date):
    if not start_date or not end_date:
        raise PreventUpdate
    else:
        print ('Updating plot')
        plot_1_fig=fig_generator(start_date,end_date,'plot_1',sql_engine_string)
        plot_2_fig=fig_generator(start_date,end_date,'plot_2',sql_engine_string)
    return plot_1_fig,plot_2_fig

# if __name__=='__main__':
#     app.run(debug=True)
