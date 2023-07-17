import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Find Jobs", href='/jobs'),
                    dbc.DropdownMenuItem("Find PhDs", href='/phds'),
                ],
            ),
        ],
        brand="Home",
        brand_href="/",
        sticky="top",
        # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        color="dark",
        # Change this to change color of text within the navbar (False for dark text)
        dark=True,
    )

    return navbar
