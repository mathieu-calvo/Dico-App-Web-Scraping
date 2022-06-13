import base64

import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output, State

from app import app
from panels import explore, exploit


server = app.server

app.layout = html.Div(
    [
        html.Div(
            className="row header",
            children=[
                html.Button(id="menu", children=dcc.Markdown("&#8801")),
                html.Span(
                    className="app-title",
                    children=[
                        dcc.Markdown("**Dictionary App**", style={'color': 'white', "margin-top": "10px"}),
                    ],
                ),
                html.Img(src=app.get_asset_url("git_logo.png")),
                html.A(
                    id="github_link",
                    children="View on Github",
                    href="https://github.com/mathieu-calvo/Dico-App-Web-Scraping/",
                    style={'color': 'white', 'border': 'solid 1px white', "margin-left": "8px"}
                )
            ],
            style={'background': '#0C4142', 'color': 'white'},
        ),
        html.Div(
            id="tabs",
            className="row tabs",
            children=[
                dcc.Link("Explore", href="/"),
                dcc.Link("Exploit", href="/"),
            ],
        ),
        html.Div(
            id="mobile_tabs",
            className="row tabs",
            style={"display": "none"},
            children=[
                dcc.Link("Explore", href="/"),
                dcc.Link("Exploit", href="/"),
            ],
        ),
        dcc.Location(id="url", refresh=False),
        html.Div(id="tab_content"),
        html.Link(
            href="https://use.fontawesome.com/releases/v5.2.0/css/all.css",
            rel="stylesheet",
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"
        ),
        html.Link(
            href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"
        ),
    ],
    style={"margin": "0%"},
)

# Update the index


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
        dcc.Link("Search", href="/dash-dictionary-app/Explore", style={"font-size": "2rem"}),
        dcc.Link("Play", href="/dash-dictionary-app/Exploit", style={"font-size": "2rem"}),
    ]
    if pathname == "/dash-dictionary-app/Exploit":
        tabs[1] = dcc.Link(
            dcc.Markdown("**&#9632 Play**", style={"font-size": "2rem"}), href="/dash-dictionary-app/Exploit"
        )
        return exploit.layout, tabs, tabs

    tabs[0] = dcc.Link(
        dcc.Markdown("**&#9632 Search**", style={"font-size": "2rem"}),
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
