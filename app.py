import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_labs as dl
from navbar import create_navbar

# Toggle the themes at [dbc.themes.LUX]
# The full list of available themes is:
# BOOTSTRAP, CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN,
# LUX, MATERIA, MINTY, PULSE, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR,
# SPACELAB, SUPERHERO, UNITED, YETI, ZEPHYR.
# To see all themes in action visit:
# https://dash-bootstrap-components.opensource.faculty.ai/docs/themes/explorer/

# To use Font Awesome Icons
FA621 = "./all.css"
APP_TITLE = "Multipage Dash App"
# (__name__, )
url_prefix = "/app/SWAPIT/"
app = dash.Dash(
    __name__,
    plugins=[dl.plugins.pages],
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.LUX,  # Dash Themes CSS
        FA621,  # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
    use_pages=True,  # New in Dash 2.7 - Allows us to register pages
    # requests_pathname_prefix="/app/SWAPIT/",
    # routes_pathname_prefix="/app/SWAPIT/",
    url_base_pathname=url_prefix
)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink("Map", active=True, href="/app/SWAPIT/pages/map", target="_blank")
            ),

        dbc.NavItem(
            dbc.NavLink("Ambient Temperature", active=True, href="/app/SWAPIT/pages/page_1", target="_blank")
            ),

        dbc.NavItem(
            dbc.NavLink("Gases", active=True, href="/app/SWAPIT/pages/page_2", target="_blank")
            ),

        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(page["name"], href=url_prefix+page["path"])
                for page in dash.page_registry.values()
                if page["module"] != "pages.not_found_404"
            ],
            nav=True,
            in_navbar=True,
            label="Menu",
            align_end=True,
            ),
        ),
    brand='Home',
    brand_href="/app/SWAPIT/",
    # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
    color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
    dark=True,  # Change this to change color of text within the navbar (False for dark text)
    ]
)


app.layout = dcc.Loading(  # <- Wrap App with Loading Component
    id='loading_page_content',
    children=[
        html.Div(
            [
                navbar,dl.plugins.page_container
            ]
        )
    ],
    color='primary',  # <- Color of the loading spinner
    fullscreen=True  # <- Loading Spinner should take up full screen
)

server = app.server


if __name__ == '__main__':
    # app.run_server(debug=False, host='0.0.0.0', port=8080)
    app.run(debug=False, host='0.0.0.0', port=8080)
