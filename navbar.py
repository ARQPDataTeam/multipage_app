from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink("Map", active=True, href="/map", target="_blank")
                ),

            dbc.NavItem(
                dbc.NavLink("CSAT Display", active=True, href="/csat", target="_blank")
                ),

            dbc.NavItem(
                dbc.NavLink("CR3000 Display", active=True, href="/cr3000", target="_blank")
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
                    dbc.DropdownMenuItem("CSAT", href='/csat'),
                    dbc.DropdownMenuItem("CR3000", href='/cr3000'),
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