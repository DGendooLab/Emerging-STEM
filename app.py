from scrape import Scrape
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import io
import csv

default_parameters = {
    'academic_discipline': 'computer-sciences',
    'hours_type': 'full-time',
    'funding_type': 'international-students',
    'ordered_keywords': "Artificial, Machine, Robot, Automation, Simulation",
    'exclude_keywords': "Data",
}

heading = '''
You provide a set of standard input parameters: 
- **Academic Discipline**
- **Hours Type**
- **Funding Type**

In addition to two non-standard parameters: 
- **Keywords in Title**: A list of keywords to search for in a title which, if matched, increase the normalized rating. 
- **Keywords to Exclude**: A list of keywords to search for in a title which renders the rating of that job zero. E.g., if you really hate Data discipline, you would include: "Data"

The web scraper searches through all the PhD listings with those parameters and returns all the listings ordered by the "rating" metric based on the ordered list of keywords.

You can then download the full dataframe as a CSV file for convenience. 

**NOTE: Parsing through all job descriptions can take some time.**
'''

# Create scrape instance
scraper = Scrape()

academic_discipline_options = [
    {"label": "Agriculture, Food & Veterinary",
        "value": "agriculture-food-and-veterinary"},
    {"label": "Architecture, Building & Planning",
        "value": "architecture-building-and-planning"},
    {"label": "Biological Sciences", "value": "biological-sciences"},
    {"label": "Business & Management Studies",
        "value": "business-and-management-studies"},
    {"label": "Computer Sciences", "value": "computer-sciences"},
    {"label": "Creative Arts & Design", "value": "creative-arts-and-design"},
    {"label": "Economics", "value": "economics"},
    {"label": "Education Studies", "value": "education-studies-inc-tefl"},
    {"label": "Engineering & Technology", "value": "engineering-and-technology"},
    {"label": "Health & Medical", "value": "health-and-medical"},
    {"label": "Historical & Philosophical Studies",
        "value": "historical-and-philosophical-studies"},
    {"label": "Information Management & Librarianship",
        "value": "information-management-and-librarianship"},
    {"label": "Languages, Literature & Culture",
        "value": "languages-literature-and-culture"},
    {"label": "Law", "value": "law"},
    {"label": "Mathematics & Statistics", "value": "mathematics-and-statistics"},
    {"label": "Media & Communications", "value": "media-and-communications"},
    {"label": "Physical & Environmental Sciences",
        "value": "physical-and-environmental-sciences"},
    {"label": "Politics & Government", "value": "politics-and-government"},
    {"label": "Psychology", "value": "psychology"},
    {"label": "Social Sciences & Social Care",
        "value": "social-sciences-and-social-care"},
    {"label": "Sport & Leisure", "value": "sport-and-leisure"}
]

funding_type_options = [
    {"label": "EU Students", "value": "eu-students"},
    {"label": "International Students", "value": "international-students"},
    {"label": "Self-funded Students", "value": "self-funded-students"},
    {"label": "UK Students", "value": "uk-students"},
]

hours_type_options = [
    {"label": "Full-time", "value": "full-time"},
    {"label": "Part-time", "value": "part-time"},
]

# Set external stylesheets
external_stylesheets = [dbc.themes.FLATLY]

# Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Define app layout
app.layout = html.Div(children=[
    dbc.Container(children=[
        html.H2(children='EmergingSTEM-PhD'),
        html.H4(children='How to use me:'),
        dcc.Markdown(children=heading),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Label('Academic Discipline'),
                dcc.Dropdown(options=academic_discipline_options,
                             value=default_parameters['academic_discipline'], id="academic_discipline"),
            ], width=4, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Funding Type'),
                dcc.Dropdown(options=funding_type_options,
                             value=default_parameters['funding_type'], id="funding_type"),
            ], width=4, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Hours Type'),
                dcc.Dropdown(options=hours_type_options,
                             value=default_parameters['hours_type'], id="hours_type"),
            ], width=4, style={'padding': '6px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Label('Keywords in Title'),
                dcc.Input(id='ordered_keywords',
                          value=default_parameters['ordered_keywords'], type='text'),
            ], width=4, style={'padding': '6px'}),
            dbc.Col(children=[
                html.Label('Keywords to Exclude'),
                dcc.Input(id='exclude_keywords',
                          value=default_parameters['exclude_keywords'], type='text'),
            ], width=4, style={'padding': '6px'}),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Button('Find PhDs', id='find_phds',
                           className="button button-primary"),
            ], width=12, style={'padding': '10px'}),
        ]),
        dcc.Loading(
            id="loading",
            children=[
                html.Div(id="results")
            ],
            type="circle",
        ),
        html.Div(id='trigger', children=0, style=dict(display='none'))
    ])
])


@app.callback(
    Output("results", "children"),
    [Input("find_phds", "n_clicks"), Input('trigger', 'children')],
    [State("academic_discipline", "value"),
     State("hours_type", "value"),
     State("funding_type", "value"),
     State("ordered_keywords", "value"),
     State("exclude_keywords", "value")]
)
def update_results(n_clicks, trigger, academic_discipline, hours_type, funding_type, ordered_keywords, exclude_keywords):
    # Don't bother updating if the page just opened or the button is disabled
    if n_clicks is None or n_clicks == 0 or trigger is None:
        raise PreventUpdate

    # Grab input
    ordered_keywords = [x.strip() for x in ordered_keywords.split(",")]
    exclude_keywords = [x.strip() for x in exclude_keywords.split(",")]

    # Scraping parameters
    parameters = {
        'academic_discipline': academic_discipline,
        'hours_type': hours_type,
        'funding_type': funding_type,
        'ordered_keywords': ordered_keywords,
        'exclude_keywords': exclude_keywords,
    }

    # Scrape based on parameters given
    df = scraper.get_scrape(parameters)

    # Create a buffer to store CSV data
    csv_buffer = io.StringIO()
    # Convert DataFrame to CSV format
    df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_NONNUMERIC)
    # Get the CSV data as a string
    csv_string = csv_buffer.getvalue()
    # Close the buffer
    csv_buffer.close()

    # Results table div
    results_div = html.Div(className="row", children=[
        html.Div(className="twelve columns", children=[
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                style_table={'overflowX': 'auto'},
                id="data_output",
                style_cell={'textAlign': 'left', 'maxWidth': '200px'},
                style_data_conditional=[
                    {
                        'if': {
                            'column_id': 'title',
                        },
                        'maxWidth': '400px',
                    },
                ]
            )
        ])
    ])

    # Div to output to results parent
    output_div = html.Div(className="row", children=[
        html.H3('Results:'),
        results_div,
        html.Br(),
        html.A(
            html.Button("Download Full Data as CSV File",
                        className="button button-primary"),
            id='download-link',
            href="data:text/csv;charset=utf-8," + csv_string,
            download="phd_data.csv"
        )
    ])

    return output_div


@app.callback(
    Output('trigger', 'children'),
    [Input('find_phds', 'n_clicks')],
    [State('trigger', 'children')]
)
def trigger_function(n_clicks, trigger):
    # Grab the id of the element that triggered the callback
    context = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    # If the button triggered the function
    if context == 'find_phds':
        if n_clicks is None:
            return trigger + 1 if trigger else 1
        elif n_clicks > 0:
            return trigger + 1 if trigger else 1
        else:
            return trigger
    else:
        return trigger  # If scrape completes and signals trigger again


if __name__ == "__main__":
    app.run_server(debug=False)
