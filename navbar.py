from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink("Map", active=True, href="/map", target="_blank")
                ),

            dbc.NavItem(
                dbc.NavLink("Ambient Temperature", active=True, href="/page_1", target="_blank")
                ),

            dbc.NavItem(
                dbc.NavLink("Gases", active=True, href="/page_2", target="_blank")
                ),

            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Map", href='/map'),
                    dbc.DropdownMenuItem("Ambient Temperature", href='/page_1'),
                    dbc.DropdownMenuItem("Gases", href='/page_2'),
                ],
            ),
        ],
        brand='Home',
        brand_href="/",
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar