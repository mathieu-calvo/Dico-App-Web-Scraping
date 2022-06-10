# -*- coding: utf-8 -*-
import pandas as pd
from dash import html, dash_table, callback_context as ctx
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_dangerously_set_inner_html

from app import app
from ReversoDictionary import ReversoDictionary

# default styles for flag buttons
clicked_style = {'border': 'solid 2px black', 'background-color': 'lightgreen'}
unclicked_style = {'border': 'None', 'background-color': '#f9f9f9'}

# create dictionary and initiate it
dico = ReversoDictionary()
dico.set_up_translation_type('fr', 'def')


layout = [
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(src=app.get_asset_url("language_icon.png"),
                         style={'height': '10%', 'width': '5%', "margin-right": "10px"}),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("fra_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    )
                ],
                    id='francais_flag_from',
                    style={'border': 'solid 2px black', 'background-color': 'lightgreen'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("eng_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    ),
                ],
                    id='anglais_flag_from',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("ita_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    ),
                ],
                    id='italien_flag_from',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("spa_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    ),
                ],
                    id='espagnol_flag_from',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
            ]),
            dbc.Col([
                html.Img(src=app.get_asset_url("search_icon.png"),
                         style={'height': '4%', 'width': '4%', "margin-right": "10px"}),
                dcc.Input(id="input_word",
                          type="text",
                          placeholder="Type a word here",
                          debounce=True,
                          style={"font-size": "1.4rem"})
            ]),
            dbc.Col([
                html.Img(src=app.get_asset_url("destination_icon.png"),
                         style={'height': '10%', 'width': '5%', "margin-right": "10px"}),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("definition_icon.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    )
                    ],
                    id='definition_flag_to',
                    style={'border': 'solid 2px black', 'background-color': 'lightgreen'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("fra_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    )
                    ],
                    id='francais_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("eng_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    ),
                    ],
                    id='anglais_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("ita_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    ),
                    ],
                    id='italien_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton'),
                html.Button([
                    html.Img(
                        src=app.get_asset_url("spa_flag.png"),
                        style={'height': '50px', "margin-right": "10px"},
                    ),
                    ],
                    id='espagnol_flag_to',
                    style={'border': 'None', 'background-color': '#f9f9f9'},
                    className='equalButton')
            ]),
        ], justify='center', align='center', style={"margin-top": "20px", "margin-bottom": "20px"}),
        dbc.Row([
            dbc.Col([
                html.Div(
                    [],
                    id='html_output',
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
            ], width=6, className="pretty_container"),
            dbc.Col([
                html.Div([], id='table_output'),
            ], width=6, className="pretty_container"),
        ], align='start'),
    ], fluid=True),
]


@app.callback(
    [Output('html_output', 'children'),
     Output('url_source', 'children'),
     Output('url_source', 'href'),
     Output('table_output', 'children')],
    [Input('input_word', 'value')] +
    [Input(f'{f}_flag_from', 'style') for f in ['francais', 'anglais', 'italien', 'espagnol']] +
    [Input(f'{f}_flag_to', 'style') for f in ['definition', 'francais', 'anglais', 'italien', 'espagnol']],
    prevent_initial_call=True,
)
def update_html_output(input_word, s1, s2, s3, s4, s5, s6, s7, s8, s9):
    """ Show definition or translation to user whenever they input a new word or change the type of action """
    # first the content from dictionary
    word_url, html_display, html_elems, content_df, elems_norm = dico.translate_or_define(input_word, target=False)
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
    return [dash_dangerously_set_inner_html.DangerouslySetInnerHTML(elems_norm), word_url, word_url, [data_table]]


@app.callback(
    [Output(f'{f}_flag_from', 'style') for f in ['francais', 'anglais', 'italien', 'espagnol']] +
    [Output(f'{f}_flag_to', 'style') for f in ['definition', 'francais', 'anglais', 'italien', 'espagnol']],
    [Input(f'{f}_flag_from', 'n_clicks') for f in ['francais', 'anglais', 'italien', 'espagnol']] +
    [Input(f'{f}_flag_to', 'n_clicks') for f in ['definition', 'francais', 'anglais', 'italien', 'espagnol']],
    prevent_initial_call=True,
)
def update_dico_type(n1, n2, n3, n4, n5, n6, n7, n8, n9):
    """ Change type of dictionary based on flags user clicked on, change style of flags accordingly """

    # work out what button is triggering the callback
    trigger = ctx.triggered[0]['prop_id']
    trigger_type = trigger.split('.')[0].split('_')[-1]
    triggering_flag = trigger.split('.')[0].split('_')[0]

    if trigger_type == 'from':

        # get current destination
        to_flag = dico.lang2

        # print(f"TYPE 1: from {triggering_flag} to {to_flag}")

        # change the dictionary accordingly
        dico.set_up_translation_type(triggering_flag, to_flag)

        # style buttons accordingly
        return [clicked_style if f == triggering_flag else unclicked_style
                for f in ['francais', 'anglais', 'italien', 'espagnol']] + \
               [clicked_style if f == to_flag else unclicked_style
                for f in ['definition', 'francais', 'anglais', 'italien', 'espagnol']]

    else:

        # get current source
        from_flag = dico.lang1

        # print(f"TYPE 2: from {from_flag} to {triggering_flag}")

        # change the dictionary accordingly
        dico.set_up_translation_type(from_flag, triggering_flag)

        # style buttons accordingly
        return [clicked_style if f == from_flag else unclicked_style
                for f in ['francais', 'anglais', 'italien', 'espagnol']] + \
               [clicked_style if f == triggering_flag else unclicked_style
                for f in ['definition', 'francais', 'anglais', 'italien', 'espagnol']]
