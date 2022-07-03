import base64

from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from panels import explore, exploit


server = app.server

app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(
                    className="row header",
                    children=[
                        html.Button(id="menu", children=dcc.Markdown("&#8801")),
                        html.Span(
                            className="app-title",
                            children=[
                                dcc.Markdown("**Dictionary App**",
                                             style={'color': 'white', "margin-top": "10px", "width": "auto"}),
                            ],
                        ),
                        html.Img(src=app.get_asset_url("git_logo.png"), className='icon', style={"width": "auto"}),
                        html.A(
                            id="github_link",
                            children="View on Github",
                            href="https://github.com/mathieu-calvo/Dico-App-Web-Scraping/",
                            className='button',
                            style={"width": "auto"},
                        )
                    ],
                    style={'background': '#0C4142', 'color': 'white'},
                ),
            ]),
        ], align='start', justify='center'),
        dbc.Row([
            dbc.Col([
                html.Div(
                    id="tabs",
                    className="row tabs",
                    children=[
                        dcc.Link("Explore", href="/"),
                        dcc.Link("Exploit", href="/"),
                    ],
                    style={"display": "flex", "align-items": "center", "justify-content": "center"},
                ),
                html.Div(
                    id="mobile_tabs",
                    className="row tabs",
                    style={"display": "none", "background-color": "white",
                           "align-items": "center", "justify-content": "center"},
                    children=[
                        dcc.Link("Explore", href="/"),
                        dcc.Link("Exploit", href="/"),
                    ],
                ),
                dcc.Location(id="url", refresh=False),
                html.Div(id="tab_content"),
            ]),
        ]),
    ], fluid=True),
])


@app.callback(
    [
        Output("tab_content", "children"),
        Output("tabs", "children"),
        Output("mobile_tabs", "children"),
    ],
    [Input("url", "pathname")],
)
def display_page(pathname):
    tabs = [
        dcc.Link("Search", href="/dash-dictionary-app/Explore"),
        dcc.Link("Play", href="/dash-dictionary-app/Exploit"),
    ]
    if pathname == "/dash-dictionary-app/Exploit":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 Play**"), href="/dash-dictionary-app/Exploit"
        )
        return exploit.layout, tabs, tabs

    tabs[0] = dcc.Link(
        dcc.Markdown("**&#9632 Search**"),
        href="/dash-dictionary-app/Explore",
    )
    return explore.layout, tabs, tabs


@app.callback(
    Output("mobile_tabs", "style"),
    [Input("menu", "n_clicks")],
    [State("mobile_tabs", "style")],
)
def show_menu(n_clicks, tabs_style):
    if n_clicks:
        if tabs_style["display"] == "none":
            tabs_style["display"] = "flex"
        else:
            tabs_style["display"] = "none"
    return tabs_style


if __name__ == "__main__":
    app.run_server(debug=True)
