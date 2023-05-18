import pandas as pd
from dash import Dash
from dash import dcc
from dash import html
from take_home_project.create_marker import create_marker


def pH_div(df):
    '''
    Function to return the PH Div component,
    this includes :—
    1. Title + Download Button
    2. Graph
    3. Range Slider
    '''
    numdate = [x for x in range(len(df['time']))]
    # create hourwise labels to diplay on range-slider
    marks = create_marker(df)

    return html.Div( children = [
                                    #Graph Heading and Button
                                    html.Div(
                                            children=[html.H2("pH vs Time",className="graph-heading"), 
                                                        html.Div( children=
                                                                [
                                                                    html.Button("Download CSV", id="btn_csv_pH"),
                                                                    dcc.Download(id="download-dataframe-csv-pH"),
                                                                ],
                                                                className="small-divs-btn"
                                                                )
                                                        ],
                                            className="heading-btn"
                                        ),

                                    #PH Graph
                                    dcc.Graph(
                                        id='PH-graph'
                                    ),

                                    #PH Slider
                                    dcc.RangeSlider(
                                        min=numdate[0], #the first index number
                                        max=numdate[-1], #the last index number
                                        value=[numdate[0],numdate[-1]], #default value of slider
                                        marks = marks,
                                        id = "PH-slider"
                                    )
                                ],
                                className="small-divs-graph"
                    )
