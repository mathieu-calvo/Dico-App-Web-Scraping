
import dash_core_components as dcc
import dash_html_components as html
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
                        dcc.Markdown("**Dictionary App**"),
                        html.Span(
                            id="subtitle",
                            children=dcc.Markdown("&nbsp using Dash and Heroku"),
                            style={"font-size": "1.8rem", "margin-top": "15px"},
                        ),
                    ],
                ),
                html.Img(src=app.get_asset_url("logo.png")),
                html.A(
                    id="learn_more",
                    children=html.Button("Learn More"),
                    href="https://plot.ly/dash/",
                ),
            ],
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
    className="row",
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
        dcc.Link("Explore", href="/dash-dictionary-app/Explore"),
        dcc.Link("Exploit", href="/dash-dictionary-app/Exploit"),
    ]
    if pathname == "/dash-dictionary-app/Explore":
        tabs[0] = dcc.Link(
            dcc.Markdown("**&#9632 Explore**"),
            href="/dash-dictionary-app/Explore",
        )
        return explore.layout, tabs, tabs
    tabs[1] = dcc.Link(
        dcc.Markdown("**&#9632 Exploit**"), href="/dash-dictionary-app/Exploit"
    )
    return exploit.layout, tabs, tabs


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
