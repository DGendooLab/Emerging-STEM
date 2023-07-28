from dash import dcc, html
import dash_bootstrap_components as dbc
from constant_manager import default_parameters_job_page, default_parameters_phd_page, academic_discipline_options, heading_job_page, heading_phd_page, funding_type_options, hours_type_options
from app import app  # Import the app instance from app.py

layout_navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", active=True, href="/")),
        dbc.NavItem(dbc.NavLink("Find PhDs", href="/phds")),
        dbc.NavItem(dbc.NavLink("Find Jobs", href="/jobs")),
    ],
)

wordcloud_image_url = app.get_asset_url("word_cloud_homepage.png")

# Text for the two features
feature1_text = "Helping you efficiently find PhD studentship opportunities in the UK."
feature2_text = "Helping you efficiently find academic job opportunities in the UK."

# Expanded Introductory text
intro_text = """
Welcome to Career Finder, a web application lead by [Dr Gendoo Deena](https://www.birmingham.ac.uk/staff/profiles/cancer-genomic/gendoo-deena.aspx), and developed by the intern team at DGengoo Lab. Career Finder is designed to be your one-stop destination for academic and research opportunities in the UK. Whether you are a student looking for Ph.D. studentships or a professional seeking academic jobs, Career Finder has got you covered.

Explore the word cloud generated from the latest academic listings and gain insights into the trending research areas and disciplines. Our application empowers you with an efficient and intuitive interface, making your search process seamless.

So, what are you waiting for? Start your journey towards a successful academic career with Career Finder!
"""
# Define custom CSS styles
custom_styles = {
    'wordcloud_img': {
        'display': 'block',
        'margin': 'auto',
        'max-height': '400px',
        'border-radius': '8px'
    },
    'feature_card_title': {
        'color': '#007BFF',  # Blue color for feature card titles
        'font-weight': 'bold'
    },
    'intro_text': {
        'font-size': '18px',
        'line-height': '1.6',
        'margin-bottom': '30px'
    },
    'feature_gap': {
        'margin-top': '20px'
    }
}
# Define the layout of the homepage with Bootstrap components and custom styling
layout_homepage = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Welcome to Career Finder",
                className="display-4 text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Img(src=wordcloud_image_url, className="img-fluid",
                     style=custom_styles['wordcloud_img']),
        ], width={"size": 8, "offset": 2})
    ], className="my-4"),
    dbc.Row([
        dbc.Col([
            html.H3("Features", className="text-center"),
            dbc.CardGroup([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(html.A("Find PhD Studentships", href="/phds", className="card-link text-dark",
                                style=custom_styles['feature_card_title']), className="card-title"),
                        html.P(feature1_text, className="card-text")
                    ])
                ]),
                dbc.Card([
                    dbc.CardBody([
                        html.H4(html.A("Find Academic Jobs", href="/jobs", className="card-link text-dark",
                                style=custom_styles['feature_card_title']), className="card-title"),
                        html.P(feature2_text, className="card-text")
                    ])
                ])
            ])
        ], width={"size": 8, "offset": 2})
    ], className="my-4"),
    dbc.Row([
        dbc.Col([
            html.H3("Introduction", className="text-center"),
            dcc.Markdown(intro_text, className="lead",
                         style=custom_styles['intro_text'])
        ], width={"size": 8, "offset": 2})
    ], className="my-4"),
], fluid=True)

# Define find_jobs page layout
layout_find_jobs = html.Div([
    # Add Navbar
    layout_navbar,
    dbc.Container([
        html.H1("Find Job Opportunities", style={
                'text-align': 'center', 'margin-top': '20px'}),
        dcc.Markdown(heading_job_page, style={'text-align': 'center'}),
        dbc.Row([
            dbc.Col([
                html.Label('Search Keywords', style={'font-weight': 'bold'}),
                dcc.Input(
                    id='search_keywords',
                    value=default_parameters_job_page['search_keywords'],
                    type='text',
                    style={'padding': '12px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                )
            ], width=6, style={'padding': '6px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Academic Discipline',
                           style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    options=academic_discipline_options,
                    value=default_parameters_job_page['academic_discipline'],
                    id="academic_discipline",
                    style={'width': '100%', 'margin-bottom': '10px'}
                ),
            ], width=4, style={'padding': '6px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Keywords in Title', style={'font-weight': 'bold'}),
                dcc.Input(
                    id='ordered_keywords',
                    value=default_parameters_job_page['ordered_keywords'],
                    type='text',
                    style={'padding': '12px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                ),
            ], width=6, style={'padding': '10px'}),]),
        dbc.Row([
            dbc.Col([
                dcc.Checklist(
                    options=[
                        {'label': 'With include keyword', 'value': 'include'},
                    ],
                    id='tick_boxes',
                    labelStyle={'display': 'block', 'margin-left': '10px'}
                ),
            ], width=6, style={'padding': '10px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Button('Find Jobs', id='find_jobs',
                            className="btn btn-primary", style={'width': '100%'}),
            ], width=12, style={'padding': '10px'}),
        ]),
        dcc.Loading(
            id="loading",
            children=[
                html.Div(id="results-jobs")
            ],
            type="circle",
        ),
        html.Div(id='trigger_jobs', children=0, style=dict(display='none')),
        html.Div(id='word-cloud-jobs')
    ], style={'max-width': '800px', 'margin': '0 auto'})
], style={'background-color': '#f9f9f9', 'padding': '20px'})


# Define the layout for finding PhDs
layout_find_phds = html.Div([
    # Add Navbar
    layout_navbar,
    dbc.Container([
        html.H1("Find PhD Opportunities", style={
                'text-align': 'center', 'margin-top': '20px'}),
        dcc.Markdown(heading_phd_page, style={'text-align': 'center'}),
        dbc.Row([
            dbc.Col([
                html.Label('Search Keywords', style={'font-weight': 'bold'}),
                dcc.Input(
                    id='search_keywords',
                    value=default_parameters_phd_page['search_keywords'],
                    type='text',
                    style={'padding': '12px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                )
            ], width=6, style={'padding': '6px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Academic Discipline', style={
                           'font-weight': 'bold'}),
                dcc.Dropdown(
                    options=academic_discipline_options,
                    value=default_parameters_phd_page['academic_discipline'],
                    id="academic_discipline",
                    style={'width': '100%', 'margin-bottom': '10px'}
                ),
            ], width=4, style={'padding': '6px'}),
            dbc.Col([
                html.Label('Funding Type', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    options=funding_type_options,
                    value=default_parameters_phd_page['funding_type'],
                    id="funding_type",
                    style={'width': '100%', 'margin-bottom': '10px'}
                ),
            ], width=4, style={'padding': '6px'}),
            dbc.Col([
                html.Label('Hours Type', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    options=hours_type_options,
                    value=default_parameters_phd_page['hours_type'],
                    id="hours_type",
                    style={'width': '100%', 'margin-bottom': '10px'}
                ),
            ], width=4, style={'padding': '6px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Label('Keywords in Title', style={'font-weight': 'bold'}),
                dcc.Input(
                    id='ordered_keywords',
                    value=default_parameters_phd_page['ordered_keywords'],
                    type='text',
                    style={'padding': '12px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                ),
            ], width=6, style={'padding': '10px'}),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Checklist(
                    options=[
                        {'label': 'With include keyword', 'value': 'include'},
                    ],
                    id='tick_boxes',
                    labelStyle={'display': 'block', 'margin-left': '10px'}
                ),
            ], width=6, style={'padding': '10px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Button('Find PhDs', id='find_phds',
                            className="btn btn-primary", style={'width': '100%'})
            ], width=12, style={'padding': '10px'}),
        ]),
        dcc.Loading(
            id="loading",
            children=[
                html.Div(id="results-phds")
            ],
            type="circle",
        ),
        html.Div(id='trigger_phds', children=0, style=dict(display='none')),
        html.Div(id='word-cloud-phds')
    ], style={'max-width': '800px', 'margin': '0 auto'})
], style={'background-color': '#f9f9f9', 'padding': '20px'})
