from navbar import create_navbar
from dash import dcc, html
import dash_bootstrap_components as dbc
from constants_job import (
    default_parameters,
    heading,
    academic_discipline_options,
)

nav = create_navbar()


def create_page_jobs():

    # Define page layout
    layout = html.Div(children=[
        # Add Navbar
        nav,
        dbc.Container(children=[
            dcc.Markdown(children=heading),
            dbc.Row(children=[
                dbc.Col(children=[
                    html.Label('Search Keywords'),
                    dcc.Input(id='search_keywords',
                              value=default_parameters['search_keywords'], type='text', style={'padding': '6px'})
                ], width=6, style={'padding': '6px'}),
                dbc.Col(children=[
                    html.Label('Academic Discipline'),
                    dcc.Dropdown(options=academic_discipline_options,
                                 value=default_parameters['academic_discipline'], id="academic_discipline"),
                ], width=6, style={'padding': '6px'}),
            ]),
            dbc.Row(children=[
                dbc.Col(children=[
                    html.Label('Keywords in Title'),
                    dcc.Input(id='ordered_keywords',
                              value=default_parameters['ordered_keywords'], type='text', style={'padding': '6px'}),
                ], width=6, style={'padding': '6px'}),
                dbc.Col(children=[
                    html.Label('Keywords to Exclude'),
                    dcc.Input(id='exclude_keywords',
                              value=default_parameters['exclude_keywords'], type='text', style={'padding': '6px'}),
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

    return layout
