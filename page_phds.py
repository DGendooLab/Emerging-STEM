from navbar import create_navbar
from scrape_phd import Scrape_PhD
import dash
from dash import dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import io
import csv
import base64
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from constants_phd import (
    default_parameters,
    heading,
    academic_discipline_options,
    funding_type_options,
    hours_type_options
)

nav = create_navbar()


def create_page_phds():
    # Create scrape instance
    scraper = Scrape_PhD()

    # Define page layout
    layout = html.Div(children=[
        # Add Navbar
        nav,
        dbc.Container(children=[
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
            html.Div(id='trigger-phds', children=0,
                     style=dict(display='none')),
            html.Div(id='word-cloud')
        ])
    ])

    @callback(
        Output("results-phds", "children"),
        [Input("find_phds", "n_clicks"), Input('trigger_phds', 'children')],
        [State("academic_discipline", "value"),
         State("hours_type", "value"),
         State("funding_type", "value"),
         State("ordered_keywords", "value"),
         State("exclude_keywords", "value"),
         State("range_slider", "value")
         ]
    )
    def update_phds_results(n_clicks, trigger, academic_discipline, hours_type, funding_type, ordered_keywords, exclude_keywords, range_slider):
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
                    download="phd_data.csv"
                )
            ], style={'padding': '10px'}),
            dbc.Row(children=[
                html.A(
                    html.Button("Build Word Cloud",
                                className="button button-primary"),
                    id='build-word-cloud-phds',
                )
            ], style={'padding': '10px'}),
        ])

        return output_div

    @callback(
        Output('trigger_phds', 'children'),
        [Input('find_phds', 'n_clicks')],
        [State('trigger_phds', 'children')]
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

    @callback(
        Output('word-cloud-phds', 'children'),
        [Input('build-word-cloud', 'n_clicks')],
        [State('data_output', 'data')]
    )
    def build_phds_word_cloud(n_clicks, data):
        if n_clicks is None or n_clicks == 0:
            raise PreventUpdate

        # Extract the titles from the data
        titles = [row['title'] for row in data]

        # Generate the word cloud
        wordcloud = WordCloud(width=800, height=400,
                              margin=1).generate(' '.join(titles))

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
    return layout