from dash import html, register_page  #, callback # If you need callbacks, import it here.


register_page(
    __name__,
    name='Home',
    top_nav=True,
    path='/',
    requests_pathname_prefix="/webapp-SWAPIT/",
    routes_pathname_prefix="/webapp-SWAPIT/"

)


def layout():
    layout = html.Div([
        html.H1(
            [
                "Home Page"
            ]
            ),
        html.Div(html.H4("""Welcome to the Data Team SWAPIT 
                            test data display dashboard home page.  
                            Below are the available data sets 
                            that can be visualized by following
                            the links above."""
                        )
                ),
        html.Div(className='gap',style={'height':'10px'}),
        html.Div([
            html.Div(children="""CRUISER CSAT wind and virtual temperature data""",className="box1",
                        style={
                        'backgroundColor':'aqua',
                        'color':'black',
                        'height':'100px',
                        'margin-left':'10px',
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block'
                        }
                    ),
            html.Img(src='assets/csat.png', alt='CSAT Plot Capture'),
                ]),
        html.Div(className='gap',style={'height':'10px'}),
        html.Div([
            html.Div(children="""CRUISER G2401 (Picarro) trace gas data""",className="box1",
                        style={
                        'backgroundColor':'aqua',
                        'color':'black',
                        'height':'100px',
                        'margin-left':'10px',
                        'width':'45%',
                        'text-align':'center',
                        'display':'inline-block'
                        }
                    ),
            html.Img(src='assets/g2401.png', alt='Picarro Plot Capture'),
                ]),
            ])
    return layout