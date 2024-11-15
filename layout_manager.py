from dash import dcc, html
import dash_bootstrap_components as dbc
from constant_manager import default_parameters_job_page, default_parameters_phd_page, academic_discipline_options, heading_job_page, heading_phd_page, funding_type_options, hours_type_options, feature1_text, feature2_text, intro_text, dev_team_text, recommended_keywords
from app import app  # Import the app instance from app.py

layout_navbar = html.Div(
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Home", active=True, href="/")),
            dbc.NavItem(dbc.NavLink("Find PhDs", href="/phds")),
            dbc.NavItem(dbc.NavLink("Find Jobs", href="/jobs")),
        ],
        style={
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'top',
            'gap': '2px',
            'fontSize': '18px',
            'color': '#333',
            'background-color': '#f8f9fa',
            'padding': '6px',
            'border': '1px solid #ddd',
            'border-radius': '10px',
            'box-shadow': '0 2px 5px rgba(0, 0, 0, 0.1)',
        },
    ),
    style={
        'width': '60%',
        'margin': '0 auto',
    },
)

wordcloud_image_url = app.get_asset_url("word_cloud_homepage.png")

# Define custom CSS styles
custom_styles = {
    'wordcloud_img': {
        'display': 'block',
        'margin': 'auto',
        'max-height': '400px',
        'border-radius': '8px'
    },
    'feature_card_title': {
        'color': '#007BFF',
    },
    'feature_gap': {
        'margin-top': '20px'
    }
}

# Define the layout of the homepage with Bootstrap components and custom styling
layout_homepage = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to Career Finder",
                            className="display-4 text-center mb-4"), width=12)
        ]),
        dbc.Row([
            dbc.Col([
                html.Img(src=wordcloud_image_url, className="img-fluid",
                         style=custom_styles['wordcloud_img']),
            ], width={"size": 8, "offset": 2})
        ], className="my-2"),
        dbc.Row([
            dbc.Col([
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
                html.H2("About Career Finder",
                        className="text-center mb-3",
                        style={'font-size': '24px', 'color': '#333'}),
                dcc.Markdown(
                    intro_text, className="lead",
                    style={'font-size': '20px', 'margin': '20px 0'}
                )
            ], width={"size": 8, "offset": 2})
        ], className="my-4"),
        dbc.Row([
            dbc.Col([
                html.H2("Meet Our Team",
                        className="text-center mb-3",
                        style={'font-size': '24px', 'color': '#333'}),
                dcc.Markdown(
                    dev_team_text, className="lead",
                    style={'font-size': '20px', 'margin': '20px 0'}
                )
            ], width={"size": 8, "offset": 2})
        ], className="my-4"),
    ])
], style={'background-color': '#f9f9f9', 'padding': '20px'})

# Define find_jobs page layout
layout_find_jobs = html.Div([
    # Add Navbar
    layout_navbar,
    dbc.Container([
        html.H2("Find Job Opportunities", style={
                'text-align': 'center', 'margin-top': '20px'}),
        dcc.Markdown(heading_job_page, style={'text-align': 'left'}),
        dbc.Row([
            dbc.Col([
                html.Label('Search Keywords', style={'font-weight': 'bold'}),
                dcc.Input(
                    id='search_keywords',
                    value=default_parameters_job_page['search_keywords'],
                    type='text',
                    style={'padding': '12px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                ),
                html.Div([
                    html.Div([
                        html.Div("Recommended Search Keywords",
                                 className="toggle-keywords"),
                        dbc.Button(
                            "Toggle Keywords",
                            id="toggle-keywords-button-job",
                            className="toggle-keywords-button",
                            color="link",
                        ),
                    ], style={'display': 'flex', 'align-items': 'center'}),
                    html.Div(
                        id="recommended_keywords_container_job",
                        children=[
                            dbc.Badge(keyword, pill=True,
                                      className='recommended-badge', style={'margin-right': '5px'})
                            for keyword in recommended_keywords
                        ],
                        style={"display": "none"},  # Initially hide the badges
                    ),
                ]),
            ], width=6, style={'padding': '6px'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'top'}),
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
            dbc.Col([
                html.Label('Keywords in Title', style={'font-weight': 'bold'}),
                dcc.Input(
                    id='ordered_keywords',
                    value=default_parameters_job_page['ordered_keywords'],
                    type='text',
                    style={'padding': '6px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                ),
            ], width=6, style={'padding': '6px'}),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Checklist(
                    options=[
                        {'label': 'Include all results', 'value': 'include'},
                    ],
                    id='tick_boxes',
                    labelStyle={'display': 'block', 'margin-left': '10px'},
                    inputStyle={'margin-right': '10px'}
                ),
            ], width=6, style={'padding': '10px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Button(
                [
                    html.I(className="fa fa-search", style={"margin-right": "10px"}),  # Cloud icon
                    "Find Jobs"
                ], id='find_jobs',
                            className="btn btn-primary", style={'width': '100%'})
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
        html.H2("Find PhD Opportunities", style={
                'text-align': 'center', 'margin-top': '20px'}),
        dcc.Markdown(heading_phd_page, style={'text-align': 'left'}),
        dbc.Row([
            dbc.Col([
                html.Label('Search Keywords', style={'font-weight': 'bold'}),
                dcc.Input(
                    id='search_keywords',
                    value=default_parameters_phd_page['search_keywords'],
                    type='text',
                    style={'padding': '12px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                ),
                html.Div([
                    html.Div([
                        html.Div("Recommended Search Keywords",
                                 className="toggle-keywords"),
                        dbc.Button(
                            "Toggle Keywords",
                            id="toggle-keywords-button-phd",
                            className="toggle-keywords-button",
                            color="link",
                        ),
                    ], style={'display': 'flex', 'align-items': 'center'}),
                    html.Div(
                        id="recommended_keywords_container_phd",
                        children=[
                            dbc.Badge(keyword, pill=True,
                                      className='recommended-badge', style={'margin-right': '5px'})
                            for keyword in recommended_keywords
                        ],
                        style={"display": "none"}, 
                    ),
                ]),
            ], width=6, style={'padding': '6px'}),
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'top'}),
        dbc.Row([
            dbc.Col([
                html.Label('Academic Discipline',
                           style={'font-weight': 'bold'}),
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
                    style={'padding': '6px', 'width': '100%',
                           'text-align': 'center', 'border': '1px solid #ccc', 'border-radius': '5px'}
                ),
            ], width=6, style={'padding': '6px'}),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Checklist(
                    options=[
                        {'label': 'Include all results', 'value': 'include'},
                    ],
                    id='tick_boxes',
                    labelStyle={'display': 'block', 'margin-left': '10px'},
                    inputStyle={'margin-right': '10px'}

                ),
            ], width=6, style={'padding': '10px'}),
        ]),
        dbc.Row([
            dbc.Col([
                html.Button(    
                [
                    html.I(className="fa fa-search", style={"margin-right": "10px"}),  # Cloud icon
                    "Find PhDs"
                ], id='find_phds',
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
