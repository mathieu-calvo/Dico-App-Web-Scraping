# -*- coding: utf-8 -*-
from dash import dcc, html, dash_table, callback_context as ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

from app import app
from ReversoDictionary import ReversoDictionary

# default styles for flag buttons
clicked_style = {'border': 'solid 2px black', 'background-color': 'lightgreen'}
unclicked_style = {'border': 'None', 'background-color': '#f9f9f9'}

# list of countries as accepted by dictionary AND in order displayed through flags
ordered_flags_from = ['francais', 'anglais', 'italien', 'espagnol', 'portugais']
ordered_flags_to = ['francais', 'anglais', 'italien', 'espagnol', 'portugais']

# create dictionary and initiate it
dico = ReversoDictionary()


layout = [
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url("language_icon.png"), className='icon'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("fra_flag.png"),
                        className='flag',
                    )
                ],
                    id='francais_flag_from',
                    style={'border': 'solid 2px black', 'background-color': 'lightgreen'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("eng_flag.png"),
                        className='flag',
                    ),
                ],
                    id='anglais_flag_from',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("ita_flag.png"),
                        className='flag',
                    ),
                ],
                    id='italien_flag_from',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("spa_flag.png"),
                        className='flag',
                    ),
                ],
                    id='espagnol_flag_from',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("por_flag.png"),
                        className='flag',
                    ),
                ],
                    id='portugais_flag_from',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
            ], xs=12, md=4, align='center'),
            dbc.Col([
                html.Img(src=app.get_asset_url("search_icon.png"), className='icon'),
                dcc.Input(id="input_word",
                          type="text",
                          placeholder="Type a word here",
                          debounce=True,
                          className="search_bar")
            ], xs=12, md=4,  align='center'),
            dbc.Col([
                html.Img(src=app.get_asset_url("destination_icon.png"), className='icon'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("fra_flag.png"),
                        className='flag',
                    )
                    ],
                    id='francais_flag_to',
                    style={'border': 'solid 2px black', 'background-color': 'lightgreen'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("eng_flag.png"),
                        className='flag',
                    ),
                    ],
                    id='anglais_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("ita_flag.png"),
                        className='flag',
                    ),
                    ],
                    id='italien_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("spa_flag.png"),
                        className='flag',
                    ),
                    ],
                    id='espagnol_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("por_flag.png"),
                        className='flag',
                    ),
                ],
                    id='portugais_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
            ], xs=12, md=4, align='center'),
        ], justify='center', align='center', style={"margin-top": "20px", "margin-bottom": "20px"}),
        dbc.Row([
            dbc.Col([
                html.Div(
                    [],
                    id='html_output_box0',
                    style={"font-size": "1.2rem", "margin-bottom": "30px"},
                ),
                html.Div(
                    [],
                    id='html_output_box1',
                    style={"font-size": "1.2rem", "margin-bottom": "30px"},
                ),
                dbc.Row([
                    html.A(
                       id="url_source",
                       children="",
                       href="",
                       style={'color': 'blue', "font-size": "0.8rem", "text-decoration": "underline"}
                    ),
                ], style={"margin-left": "10px"}),
            ], xs=12, md=6, className="pretty_container"),
            dbc.Col([
                html.Div([], id='table_output'),
            ], xs=12, md=6, className="pretty_container"),
        ], align='start'),
    ], fluid=True),
]


@app.callback(
    [Output('html_output_box0', 'children'),
     Output('html_output_box1', 'children'),
     Output('url_source', 'children'),
     Output('url_source', 'href'),
     Output('table_output', 'children')],
    [Input('input_word', 'value')] +
    [Input(f'{f}_flag_from', 'style') for f in ordered_flags_from] +
    [Input(f'{f}_flag_to', 'style') for f in ordered_flags_to],
    prevent_initial_call=True,
)
def update_html_output(input_word, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10):
    """ Show definition or translation to user whenever they input a new word or change the type of action """
    if input_word is None:
        raise PreventUpdate

    # first infer languages from style of buttons
    lang1_idx = [b['border'] != "None" for b in [s1, s2, s3, s4, s5]].index(True)
    lang2_idx = [b['border'] != "None" for b in [s6, s7, s8, s9, s10]].index(True)
    lang1 = ordered_flags_from[lang1_idx]
    lang2 = ordered_flags_to[lang2_idx]

    # if source and destination are the same change to definition
    if lang1 == lang2:
        lang2 = 'definition'

    # get the content from dictionary
    word_url, box0_elms_norm, box1_elms_norm, content_df = dico.get_translation_or_definition(input_word, lang1, lang2)

    # table in dash format
    data_table = dash_table.DataTable(
        data=content_df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in content_df.columns],
        style_cell={'textAlign': 'left'},
        style_header={'textAlign': 'center', 'fontWeight': 'bold'},
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
    )
    return [dash_dangerously_set_inner_html.DangerouslySetInnerHTML(box0_elms_norm),
            dash_dangerously_set_inner_html.DangerouslySetInnerHTML(box1_elms_norm),
            word_url,
            word_url,
            [data_table]]


@app.callback(
    [Output(f'{f}_flag_from', 'style') for f in ordered_flags_from] +
    [Output(f'{f}_flag_to', 'style') for f in ordered_flags_to],
    [Input(f'{f}_flag_from', 'n_clicks') for f in ordered_flags_from] +
    [Input(f'{f}_flag_to', 'n_clicks') for f in ordered_flags_to],
    [State(f'{f}_flag_from', 'style') for f in ordered_flags_from] +
    [State(f'{f}_flag_to', 'style') for f in ordered_flags_to],
    prevent_initial_call=True,
)
def update_buttons_style(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10):
    """ Change buttons' style based on flags user clicked on """

    # work out what button is triggering the callback
    trigger = ctx.triggered[0]['prop_id']
    trigger_type = trigger.split('.')[0].split('_')[-1]
    triggering_flag = trigger.split('.')[0].split('_')[0]

    # get current destination and source - infer from style of buttons
    lang1_idx = [b['border'] != "None" for b in [s1, s2, s3, s4, s5]].index(True)
    lang2_idx = [b['border'] != "None" for b in [s6, s7, s8, s9, s10]].index(True)
    from_flag = ordered_flags_from[lang1_idx]
    to_flag = ordered_flags_to[lang2_idx]

    if trigger_type == 'from':

        # style buttons accordingly
        return [clicked_style if f == triggering_flag else unclicked_style for f in ordered_flags_from] + \
               [clicked_style if f == to_flag else unclicked_style for f in ordered_flags_to]

    else:

        # style buttons accordingly
        return [clicked_style if f == from_flag else unclicked_style for f in ordered_flags_from] + \
               [clicked_style if f == triggering_flag else unclicked_style for f in ordered_flags_to]
