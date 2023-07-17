from scrape_job import Scrape_Job
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import io
import csv
import base64
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from constants_job import (
    default_parameters,
    heading,
    academic_discipline_options,
)

# Create scrape instance
scraper = Scrape_Job()

# Set external stylesheets
external_stylesheets = [dbc.themes.LUMEN]

# Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Define app layout
app.layout = html.Div(children=[
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
                html.Div(id="results")
            ],
            type="circle",
        ),
        html.Div(id='trigger', children=0, style=dict(display='none')),
        html.Div(id='word-cloud')
    ])
])


@app.callback(
    Output("results", "children"),
    [Input("find_jobs", "n_clicks"), Input('trigger', 'children')],
    [State("search_keywords", "value"),
     State("academic_discipline", "value"),
     State("ordered_keywords", "value"),
     State("exclude_keywords", "value"),
     State("range_slider", "value")
     ]
)
def update_resules(n_clicks, trigger, search_keywords, academic_discipline, ordered_keywords, exclude_keywords, range_slider):
    # Don't bother updating if the page just opened or the button is disabled
    if n_clicks is None or n_clicks == 0 or trigger is None:
        raise PreventUpdate

    # Grab input
    ordered_keywords = [x.strip() for x in ordered_keywords.split(",")]
    exclude_keywords = [x.strip() for x in exclude_keywords.split(",")]

    # Scraping parameters
    parameters = {
        'search_keywords': search_keywords,
        'academic_discipline': academic_discipline,
        'ordered_keywords': ordered_keywords,
        'exclude_keywords': exclude_keywords,
    }
    # Scrape based on parameters given
    df = scraper.get_scrape(parameters)

    # Filter data based on output_range value
    if range_slider == [0, 0]:
        df = df[df['rating'] > 0]
    elif range_slider == [0, 1]:
        df = df[df['rating'] >= 0]
    elif range_slider == [1, 1]:
        df = df[df['rating'] == 0]
    elif range_slider == [0, 2]:
        df = df
    elif range_slider == [2, 2]:
        df = df[df['rating'] == -1]

    # Create a buffer to store CSV data
    csv_buffer = io.StringIO()
    # Convert DataFrame to CSV format
    df.to_csv(csv_buffer, index=False, quoting=csv.QUOTE_NONNUMERIC)
    # Get the CSV data as a string
    csv_string = csv_buffer.getvalue()
    # Close the buffer
    csv_buffer.close()

    results_div = html.Div(className="row", children=[
        html.Div(className="table-active", children=[
            dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'id': c, 'name': c} for c in df.columns],
                style_table={'width': '100%', 'overflowX': 'auto'},
                id="data_output",
                style_cell={
                    'textAlign': 'left',
                    'fontSize': '14px',
                    'fontFamily': 'Arial, sans-serif',
                    'padding': '8px',  # Add padding for cell content
                },
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_data_conditional=[
                    {
                        'if': {'column_id': 'title'},
                        'height': 'auto',
                    },
                    {
                        'if': {
                            'filter_query': '{column_id} != "title"'
                        },
                        'whiteSpace': 'nowrap',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': '200px',  # Adjust the maximum width as needed
                    },
                ],
            )
        ])
    ])

    # Div to output to results parent
    output_div = html.Div(className="row", children=[
        html.H3('Results:'),
        results_div,
        dbc.Row(children=[
            html.A(
                html.Button("Download Full Data as CSV File",
                            className="button button-primary"),
                id='download-link',
                href="data:text/csv;charset=utf-8," + csv_string,
                download="job_data.csv"
            )
        ], style={'padding': '10px'}),
        dbc.Row(children=[
            html.A(
                html.Button("Build Word Cloud",
                            className="button button-primary"),
                id='build-word-cloud',
            )
        ], style={'padding': '10px'}),
    ])

    return output_div


@app.callback(
    Output('trigger', 'children'),
    [Input('find_jobs', 'n_clicks')],
    [State('trigger', 'children')]
)
def trigger_function(n_clicks, trigger):
    # Grab the id of the element that triggered the callback
    context = dash.callback_context.triggered[0]['prop_id'].split('.')[0]

    # If the button triggered the function
    if context == 'find_jobs':
        if n_clicks is None:
            return trigger + 1 if trigger else 1
        elif n_clicks > 0:
            return trigger + 1 if trigger else 1
        else:
            return trigger
    else:
        return trigger  # If scrape completes and signals trigger again


@app.callback(
    Output('word-cloud', 'children'),
    [Input('build-word-cloud', 'n_clicks')],
    [State('data_output', 'data')]
)
def build_word_cloud(n_clicks, data):
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    # Extract the titles from the data
    titles = [row['title'] for row in data]
    employer = [row['employer'] for row in data]
    department = [row['department'] for row in data]
    location = [row['location'] for row in data]
    str_word_cloud = titles+employer+department+location

    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400,
                          margin=1).generate(' '.join(str_word_cloud))

    # Convert the word cloud image to a base64-encoded string
    image_data = io.BytesIO()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(image_data, format='png')
    plt.close()
    image_data.seek(0)
    encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

    # Create a div to display the word cloud
    word_cloud_div = html.Div([
        html.H4('Word Cloud'),
        html.Img(src=f"data:image/png;base64,{encoded_image}")
    ])

    return word_cloud_div


if __name__ == "__main__":
    app.run_server(debug=True)
