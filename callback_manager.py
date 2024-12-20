import dash
from dash import html, dash_table, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import io
import csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
from scrape_job import Scrape_Job
from scrape_phd import Scrape_PhD


@callback(
    Output("results-phds", "children"),
    [Input("find_phds", "n_clicks"), Input('trigger_phds', 'children')],
    [State("search_keywords", "value"),
        State("academic_discipline", "value"),
        State("hours_type", "value"),
        State("funding_type", "value"),
        State("ordered_keywords", "value"),
        State("tick_boxes", "value")
     ]
)
def update_phds_results(n_clicks, trigger, search_keywords, academic_discipline, hours_type, funding_type, ordered_keywords, tick_boxes):
    # Don't bother updating if the page just opened or the button is disabled
    if n_clicks is None or n_clicks == 0 or trigger is None:
        raise PreventUpdate

    # Grab input
    ordered_keywords = [x.strip() for x in ordered_keywords.split(",")]

    # Scraping parameters
    parameters = {
        'search_keywords': search_keywords,
        'academic_discipline': academic_discipline,
        'hours_type': hours_type,
        'funding_type': funding_type,
        'ordered_keywords': ordered_keywords,
    }
 # Create scrape instance
    scraper_phds = Scrape_PhD()
    # Scrape based on parameters given
    df = scraper_phds.get_scrape(parameters)

    # Filter data based on output_range value
    if tick_boxes == ['include']:
        df = df[df['rating'] > 0]
    else:
        df = df

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
                # columns=[{'id': c, 'name': c} for c in df.columns],
                columns=[
                    {'id': c, 'name': ' '.join(word.capitalize() for word in c.split('_'))} if c != 'url' else
                    {'id': 'url', 'name': 'URL', 'presentation': 'markdown'}  # Render URL as clickable links
                    for c in df.columns
                ],
                style_table={'width': '100%', 'overflowX': 'auto'},
                id="data_output",
                # Bold column headers
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#f1f1f1',  # Optional: light background for headers
                    'border': '1px solid #ddd',
                    'textAlign': 'center',  # Center-align header text
                },
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
                    # Alternating row colors
                    {
                        'if': {'row_index': 'odd'},  # Grey background for odd rows
                        'backgroundColor': '#f9f9f9',
                    },
                    {
                        'if': {'row_index': 'even'},  # White background for even rows
                        'backgroundColor': '#ffffff',
                    },
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
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'}
                        for column, value in row.items()
                    } for row in df.to_dict('records')
                ],
                tooltip_duration=None
            )
        ])
    ])

    # Div to output to results parent
    output_div = html.Div(className="row", children=[
        html.H3('Results'),
        results_div,
        dbc.Row(children=[
            html.A(
                html.Button(
                [
                    html.I(className="fa fa-download", style={"margin-right": "10px"}),  # Font Awesome download icon
                    "Download Results"
                ],
                className="btn btn-success", style={'width': '30%'}),
                id='download-link',
                href="data:text/csv;charset=utf-8," + csv_string,
                download="phd_data.csv"
            )
        ], style={'padding': '10px'}),
        dbc.Row(children=[
            html.A(
                html.Button(
                [
                    html.I(className="fa fa-cloud", style={"margin-right": "10px"}),  # Cloud icon
                    "Build Word Cloud"
                ],
                className="btn btn-primary", style={'width': '30%'}, disabled=True),
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
    [Input('build-word-cloud-phds', 'n_clicks')],
    [State('data_output', 'data')]
)
def build_phds_word_cloud(n_clicks, data):
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    # Extract the titles from the data
    titles = [row['title'] for row in data]

    # Generate the word cloud
    wordcloud = WordCloud(background_color='white', width=800, height=400,
                          margin=1).generate(' '.join(titles))

    # Convert the word cloud image to a base64-encoded string
    image_data = io.BytesIO()
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(image_data, format='png')
    plt.close()
    image_data.seek(0)
    encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

    # Create a div to display the word cloud
    word_cloud_div = html.Div([
        html.Img(src=f"data:image/png;base64,{encoded_image}")
    ])

    return word_cloud_div


@callback(
    Output("results-jobs", "children"),
    [Input("find_jobs", "n_clicks"), Input('trigger_jobs', 'children')],
    [State("search_keywords", "value"),
        State("academic_discipline", "value"),
        State("ordered_keywords", "value"),
        State("tick_boxes", "value")
     ]
)
# Don't bother updating if the page just opened or the button is disabled
def update_jobs_results(n_clicks, trigger, search_keywords, academic_discipline, ordered_keywords, tick_boxes):
    if n_clicks is None or n_clicks == 0 or trigger is None:
        raise PreventUpdate

    # Grab input
    ordered_keywords = [x.strip() for x in ordered_keywords.split(",")]

    # Scraping parameters
    parameters = {
        'search_keywords': search_keywords,
        'academic_discipline': academic_discipline,
        'ordered_keywords': ordered_keywords,
    }
    # Create scrape instance
    scraper_job = Scrape_Job()
    # Scrape based on parameters given
    df = scraper_job.get_scrape(parameters)

    # Filter data based on output_range value
    if tick_boxes == ['include']:
        df = df[df['rating'] > 0]
    else:
        df = df

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
                # columns=[{'id': c, 'name': c} for c in df.columns],
                columns=[
                    {'id': c, 'name': ' '.join(word.capitalize() for word in c.split('_'))} if c != 'url' else
                    {'id': 'url', 'name': 'URL', 'presentation': 'markdown'}  # Render URL as clickable links
                    for c in df.columns
                ],
                style_table={'width': '100%', 'overflowX': 'auto'},
                id="data_output",
                # Bold column headers
                style_header={
                    'fontWeight': 'bold',
                    'backgroundColor': '#f1f1f1',  # Optional: light background for headers
                    'border': '1px solid #ddd',
                    'textAlign': 'center',  # Center-align header text
                },
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
                    # Alternating row colors
                    {
                        'if': {'row_index': 'odd'},  # Grey background for odd rows
                        'backgroundColor': '#f9f9f9',
                    },
                    {
                        'if': {'row_index': 'even'},  # White background for even rows
                        'backgroundColor': '#ffffff',
                    },
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
                tooltip_data=[
                    {
                        column: {'value': str(value), 'type': 'markdown'} if column != 'url' else
                        {'value': value, 'type': 'text'}  # Tooltip for URL column shows raw URL
                        for column, value in row.items()
                    } for row in df.to_dict('records')
                ],
                tooltip_duration=None
            )
        ])
    ])

    # Div to output to results parent
    output_div = html.Div(className="row", children=[
        html.H3('Results'),
        results_div,
        dbc.Row(children=[
            html.A(
                html.Button(
                [
                    html.I(className="fa fa-download", style={"margin-right": "10px"}),  # Font Awesome download icon
                    "Download Results"
                ],
                className="btn btn-success", style={'width': '30%'}),
                id='download-link',
                href="data:text/csv;charset=utf-8," + csv_string,
                download="job_data.csv"
            )
        ], style={'padding': '10px'}),
        dbc.Row(children=[
            dbc.Col(
                html.Button(
                [
                    html.I(className="fa fa-cloud", style={"margin-right": "10px"}),  # Cloud icon
                    "Build Word Cloud"
                ],
                className="btn btn-primary", style={'width': '30%'}, disabled=True),
                id='build-word-cloud-jobs',
                
            )
        ], style={'padding': '10px'}), 
    ])
    return output_div


@callback(
    Output('trigger_jobs', 'children'),
    [Input('find_jobs', 'n_clicks')],
    [State('trigger_jobs', 'children')]
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


@callback(
    Output('word-cloud-jobs', 'children'),
    [Input('build-word-cloud-jobs', 'n_clicks')],
    [State('data_output', 'data')]
)
def build_jobs_word_cloud(n_clicks, data):
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    # Extract the titles from the data
    titles = [row['title'] for row in data]
    employer = [row['employer'] for row in data]
    department = [row['department'] for row in data]
    location = [row['location'] for row in data]
    str_word_cloud = titles + employer + department + location
    print(str_word_cloud)
    # Generate the word cloud
    wordcloud = WordCloud(background_color='white', width=800, height=400,
                          margin=1).generate(' '.join(str_word_cloud))

    # Convert the word cloud image to a base64-encoded string
    image_data = io.BytesIO()
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(image_data, format='png')
    plt.close()
    image_data.seek(0)
    encoded_image = base64.b64encode(image_data.getvalue()).decode('utf-8')

    # Create a div to display the word cloud
    return html.Div([
        html.Img(src=f"data:image/png;base64,{encoded_image}")
    ])


@callback(
    Output("recommended_keywords_container_job", "style"),
    [Input("toggle-keywords-button-job", "n_clicks")],
    [State("recommended_keywords_container_job", "style")]
)
def toggle_keywords_collapse_job(n, current_style):
    if n:
        display = current_style.get("display", "")
        return {"display": "block" if display == "none" else "none"}
    return current_style


@callback(
    Output("recommended_keywords_container_phd", "style"),
    [Input("toggle-keywords-button-phd", "n_clicks")],
    [State("recommended_keywords_container_phd", "style")]
)
def toggle_keywords_collapse_phd(n, current_style):
    if n:
        display = current_style.get("display", "")
        return {"display": "block" if display == "none" else "none"}
    return current_style
