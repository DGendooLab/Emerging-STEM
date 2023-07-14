from scrape import *
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
default_parameters = {
    'academic_discipline': 'computer-science',
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

in addition to two non-standard paramaters: 
- **Keywords in Title**: A list of keywords to search for in a title which, if matched for, increase the normalised rating. 
- **Keywords to Exclude**: A list of keywords to search for in a title which renders the rating of that job zero. E.g. if you really hate Data discipline, you would include: "Data"

The web scraper searches through all the PhD listings with those paramaters and returns all the listings ordered by the "rating" metric based on the ordered list of keywords.

You can then download the full dataframe as an excel sheet for convenience. 

**NOTE: Parsing through all job descriptions can take sometime. **

'''

# create scrape instance
scraper = scrape()

# better stylesheet
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Create app
app = dash.Dash(external_stylesheets=external_stylesheets)

# assign server instance
server = app.server
# Create layout
app.layout = html.Div(children=[
    dcc.Markdown(heading),
    dbc.Progress(id="progress", value=0, striped=True, animated=True),
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.Label('Academic Discipline'),
                dcc.Input(id='academic_discipline',
                          value=default_parameters['academic_discipline'], type='text')
            ], className="four columns"),
            html.Div(children=[
                html.Label('Funding Type'),
                dcc.Input(id='funding_type',
                          value=default_parameters['funding_type'], type='text')
            ], className="four columns"),
            html.Div(children=[
                html.Label('Hours Type'),
                dcc.Input(id='hours_type',
                          value=default_parameters['hours_type'], type='text')
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
        dcc.Interval(id="interval", interval=1000, n_intervals=0),
        html.Div(id='trigger', children=0, style=dict(display='none'))
    ])
])

######################################################################################################################
# Callback Functions #
######################################################################################################################


if __name__ == "__main__":
    app.run_server(debug=True)
