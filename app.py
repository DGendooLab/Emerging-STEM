from scrape import Scrape
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

default_parameters = {
    'academic_discipline': 'computer-sciences',
    'hours_type': 'full-time',
    'funding_type': 'international-students',
    'ordered_keywords': "Artificial, Machine, Robot, Automation, Simulation",
    'exclude_keywords': "Data",
}

heading = '''
## EmergingSTEM-PhD
### How to use me:

You provide a set of standard input parameters: 
- **academic_discipline**
- **hours_type**
- **funding_type**

in addition to two non-standard parameters: 
- **Keywords in Title**: A list of keywords to search for in a title which, if matched, increase the normalized rating. 
- **Keywords to Exclude**: A list of keywords to search for in a title which renders the rating of that job zero. E.g., if you really hate Data discipline, you would include: "Data"

The web scraper searches through all the PhD listings with those parameters and returns all the listings ordered by the "rating" metric based on the ordered list of keywords.

You can then download the full dataframe as an excel sheet for convenience. 

**NOTE: Parsing through all job descriptions can take some time.**

'''

# Creating app instance and designing layout #

# Create scrape instance
scraper = Scrape()

# Define dropdown options
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
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define app layout
app.layout = html.Div(children=[
    dcc.Markdown(heading),
    dbc.Progress(id="progress", value=0, max=100, striped=True, animated=True),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Label('Academic Discipline'),
                dcc.Input(id='academic_discipline',
                          value=default_parameters['academic_discipline'], type='text')
            ], className="four columns"),
            html.Div(children=[
                html.Label('Funding Type'),
                dcc.Dropdown(options=funding_type_options,
                             value=default_parameters['funding_type'], id="funding_type"),
            ], className="four columns"),
            html.Div(children=[
                html.Label('Hours Type'),
                dcc.Dropdown(options=hours_type_options,
                             value=default_parameters['hours_type'], id="hours_type"),
            ], className="four columns"),
        ], className="row", style={'padding': 10}),
        html.Div(children=[
            html.Div(children=[
                html.Label('Keywords in Title'),
                dcc.Input(id='ordered_keywords',
                          value=default_parameters['ordered_keywords'], type='text')
            ], className="four columns"),
            html.Div(children=[
                html.Label('Keywords to Exclude'),
                dcc.Input(id='exclude_keywords',
                          value=default_parameters['exclude_keywords'], type='text')
            ], className="four columns"),
        ], className="row", style={'padding': 10}),
        html.Div(children=[
            html.Div(children=[
                html.Button('Find PhDs', id='find_phds',
                            className="button button-primary")
            ], className="twelve columns"),
        ], className="row", style={'padding': 10}),
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

# Callback to update results table upon button click, if button isn't disabled


@app.callback(
    Output("results", "children"),
    [Input("find_phds", "n_clicks")],
    [State("academic_discipline", "value"),
     State("hours_type", "value"),
     State("funding_type", "value"),
     State("ordered_keywords", "value"),
     State("exclude_keywords", "value")]
)
def update_results(n_clicks, academic_discipline, hours_type, funding_type, ordered_keywords, exclude_keywords):
    # Don't bother updating if the page just opened or the button is disabled
    if n_clicks is None or n_clicks == 0:
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

    # Column for data-table
    columns = [{"name": i, "id": i} for i in df.columns]

    # Convert data to list of dictionaries
    data = df.to_dict(orient='records')

    # Results table div
    results_div = html.Div(className="row", children=[
        html.Div(className="twelve columns", children=[
            dash_table.DataTable(
                id="data_output",
                style_as_list_view=True,
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                },
                style_cell={
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                    'minWidth': '0px',
                    'maxWidth': '180px'
                },
                data=data,
                columns=columns
            )
        ])
    ])

    # Div to output to results parent
    output_div = html.Div(className="row", children=[
        dcc.Markdown('''
        
        ### Results: 
                        
        '''),
        results_div,
        html.Br(),
        html.A(
            html.Button("Download Full Data as CSV File",
                        className="button button-primary"),
            id='download-link',
            href="/",
            download="phd_data.csv"
        )
    ])

    return output_div

# Callback which checks if button has been triggered already or not. Disables it if so.


@app.callback(
    Output('find_phds', 'disabled'),
    [Input('find_phds', 'n_clicks'),
     Input('trigger', 'children')]
)
def trigger_function(n_clicks, trigger):
    # Grab the id of the element that triggered the callback
    context = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    # If the button triggered the function
    if context == 'find_phds':
        if n_clicks is None:
            return False
        elif n_clicks > 0:
            return True
        else:
            return False
    else:
        return False  # If scrape completes and signals trigger again


if __name__ == "__main__":
    app.run_server(debug=True)
