from dash import html, dcc
from dash.dependencies import Input, Output
from home import create_page_home
from page_jobs import create_page_jobs
from page_phds import create_page_phds
from app import app
import callbacks

server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/jobs':
        return create_page_jobs()
    if pathname == '/phds':
        return create_page_phds()
    else:
        return create_page_home()


if __name__ == '__main__':
    app.run_server(debug=True)
