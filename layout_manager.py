from dash import dcc, html
import dash_bootstrap_components as dbc
from constant_manager import default_parameters_job_page, default_parameters_phd_page, academic_discipline_options, heading_job_page, heading_phd_page, funding_type_options, hours_type_options
layout_navbar = html.Div(
    [
        dbc.NavbarSimple(
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
    ]
)


layout_homepage = html.Div([
    layout_navbar,
    html.H3('Welcome to home page!')
])

# Define find_jobs page layout
layout_find_jobs = html.Div(children=[
    # Add Navbar
    layout_navbar,
    dbc.Container(children=[
        dcc.Markdown(children=heading_job_page),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Label('Search Keywords'),
                dcc.Input(id='search_keywords',
                          value=default_parameters_job_page['search_keywords'], type='text', style={'padding': '6px'})
            ], width=6, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Academic Discipline'),
                dcc.Dropdown(options=academic_discipline_options,
                             value=default_parameters_job_page['academic_discipline'], id="academic_discipline"),
            ], width=6, style={'padding': '6px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Label('Keywords in Title'),
                dcc.Input(id='ordered_keywords',
                          value=default_parameters_job_page['ordered_keywords'], type='text', style={'padding': '6px'}),
            ], width=6, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Keywords to Exclude'),
                dcc.Input(id='exclude_keywords',
                          value=default_parameters_job_page['exclude_keywords'], type='text', style={'padding': '6px'}),
            ], width=6, style={'padding': '6px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dcc.RangeSlider(
                    min=0,
                    max=2,
                    step=1,
                    value=[0, 1],
                    marks={
                        0: {'label': 'with include keyword'},
                        1: {'label': 'without exclude or include keyword'},
                        2: {'label': 'with exclude keyword'}
                    },
                    id='range_slider'
                ),
            ], width=6, style={'padding': '10px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Button('Find Jobs', id='find_jobs',
                           className="btn btn-primary"),
            ], width=12, style={'padding': '10px'}),
        ]),
        dcc.Loading(
            id="loading",
            children=[
                html.Div(id="results-jobs")
            ],
            type="circle",
        ),
        html.Div(id='trigger_jobs', children=0,
                    style=dict(display='none')),
        html.Div(id='word-cloud-jobs')
    ])
])

# Define find_phds page layout
layout_find_phds = html.Div(children=[
    # Add Navbar
    layout_navbar,
    dbc.Container(children=[
        dcc.Markdown(children=heading_phd_page),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Label('Academic Discipline'),
                dcc.Dropdown(options=academic_discipline_options,
                             value=default_parameters_phd_page['academic_discipline'], id="academic_discipline"),
            ], width=4, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Funding Type'),
                dcc.Dropdown(options=funding_type_options,
                             value=default_parameters_phd_page['funding_type'], id="funding_type"),
            ], width=4, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Hours Type'),
                dcc.Dropdown(options=hours_type_options,
                             value=default_parameters_phd_page['hours_type'], id="hours_type"),
            ], width=4, style={'padding': '6px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Label('Keywords in Title'),
                dcc.Input(id='ordered_keywords',
                          value=default_parameters_phd_page['ordered_keywords'], type='text', style={'padding': '6px'}),
            ], width=6, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Keywords to Exclude'),
                dcc.Input(id='exclude_keywords',
                          value=default_parameters_phd_page['exclude_keywords'], type='text', style={'padding': '6px'}),
            ], width=6, style={'padding': '6px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dcc.RangeSlider(
                    min=0,
                    max=2,
                    step=1,
                    value=[0, 1],
                    marks={
                        0: {'label': 'with include keyword'},
                        1: {'label': 'without exclude or include keyword'},
                        2: {'label': 'with exclude keyword'}
                    },
                    id='range_slider'
                ),
            ], width=6, style={'padding': '10px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Button('Find PhDs', id='find_phds',
                           className="btn btn-primary"),
            ], width=12, style={'padding': '10px'}),
        ]),
        dcc.Loading(
            id="loading",
            children=[
                html.Div(id="results-phds")
            ],
            type="circle",
        ),
        html.Div(id='trigger_phds', children=0,
                    style=dict(display='none')),
        html.Div(id='word-cloud-phds')
    ])
])
