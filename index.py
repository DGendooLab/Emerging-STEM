from dash import html, dcc
from dash.dependencies import Input, Output
from app import app
import callback_manager  # important, do not delete
from layout_manager import layout_homepage, layout_find_jobs, layout_find_phds

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

app.title = "Career Finder"
app._favicon = "icon.png"


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/jobs':
        return layout_find_jobs
    if pathname == '/phds':
        return layout_find_phds
    else:
        return layout_homepage


if __name__ == '__main__':
    app.run_server(debug=False)
