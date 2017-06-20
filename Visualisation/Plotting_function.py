
import plotly
plotly.tools.set_credentials_file(username='zandermoore1994', api_key='dund3fgcUIRA82LX6JxJ')
from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import scipy as sp
import plotly as py
import pandas
plotly.offline.init_notebook_mode()
import plotly.offline as offline
import jinja2

def plot_graphs(data_new):
    CDUstr="CDU/CSU"
    SPDstr="SPD"
    GRÜNEstr="GRÜNE"
    LINKEstr='LINKE'
    AfDstr='AfD'
    parties=[CDUstr,SPDstr,GRÜNEstr,LINKEstr,AfDstr]
    total=np.sum(data_new[parties].iloc[0])
    base_chart = {
        "values": [40, 10, 10, 10, 10, 10, 10],"domain": {"x": [0, .48]},"marker": {"colors": ['rgb(255, 255, 255)','rgb(255, 255, 255)','rgb(255, 255, 255)','rgb(255, 255, 255)','rgb(255, 255, 255)','rgb(255, 255, 255)','rgb(255, 255, 255)'],"line": {"width": 0}},"name": "Predictor","hole": .4,"type": "pie","direction": "clockwise", "rotation": 180,"showlegend": False,"hoverinfo": "none","textinfo": "none","textposition": "outside"}
    meter_chart = {"values": [total, data_new[CDUstr][0], data_new[SPDstr][0], data_new[GRÜNEstr][0],data_new[AfDstr][0],data_new[LINKEstr][0]],
        "labels": [" ", "CDU/CSU", "SPD", "Green", "AFD", "Die Linke"],
        "marker": {'colors': ['rgb(255, 255, 255)','rgb(0,0,0)','rgb(165,0,38)','rgb(154,205,50)','rgb(0,204,255)','rgb(153,102,255)']},
        "domain": {"x": [0, 0.48]},"name": "% Representation","hole": .3,"type": "pie",  "direction": "clockwise", "rotation": 90,
        "showlegend": False,"textinfo": "label", "textposition": "outside","hoverinfo": "none"}

    fig_1 = {"data": [base_chart, meter_chart],}
    #offline.plot(fig_1 , output_type='file', filename='SeatChart',image='png')


    timeline= data_new['Datum'][::-1]
    CDU_data=data_new[CDUstr][::-1]
    SPD_data=data_new[SPDstr][::-1]
    Green_data=data_new[GRÜNEstr][::-1]
    Linke_data=data_new[LINKEstr][::-1]
    AFD_data=data_new[AfDstr][::-1]



    CDU = go.Scatter(
    x=timeline,
    y=CDU_data,
    name = "CDU",
    line = dict(color = 'rgb(0,0,0)'),
    opacity = 0.8)

    SPD = go.Scatter(
        x=timeline,
        y=SPD_data,
        name = "SPD",
        line = dict(color = 'rgb(165,0,38)'),
        opacity = 0.8)

    Gruene = go.Scatter(
        x=timeline,
        y=Green_data,
        name = "Gruene",
        line = dict(color = 'rgb(154,205,50)'),
        opacity = 0.8)

    Linke = go.Scatter(
        x=timeline,
        y=Linke_data,
        name = "Linke",
        line = dict(color = 'rgb(0,204,255)'),
        opacity = 0.8)

    AFD = go.Scatter(
        x=timeline,
        y=AFD_data,
        name = "AfD",
        line = dict(color = 'rgb(153,102,255)'),
        opacity = 0.8)

    data2 = [CDU,SPD,Gruene,Linke,AFD]

    layout2 = dict(
        title='Evolution of Second Vote Prediction',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='timeline'
        )
    )

    fig_2 = dict(data=data2, layout=layout2)

    xx=offline.plot(fig_1 ,show_link=False, output_type='div', filename='SeatChart.html',image='None', image_width=80, image_height=60)
    xxx=offline.plot(fig_2 ,show_link=False, output_type='div', filename='TimeEvolution.html',image='None', image_width=80, image_height=60)

    template= jinja2.Template("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    header, footer {
        padding: 1em;
        color: white;
        background-color: black;
        clear: left;
        text-align: center;
    }
    .flex-container {
        display: -webkit-flex;
        display: flex;
        width: 2500px;
        height: 600px;
        background-color: white;
    }

    .flex-item {
        background-color: white;
        flex-grow: 0.2
        margin-right: 170px;
        border-right: 1px solid gray;


    }

    .select {
         order: <1>;
         padding:3px;
         width: 100px;
        height: 30px;
        margin: 0;
        -webkit-border-radius:4px;
        -moz-border-radius:4px;
        border-radius:4px;
        -webkit-box-shadow: 0 3px 0 #ccc, 0 -1px #fff inset;
        -moz-box-shadow: 0 3px 0 #ccc, 0 -1px #fff inset;
        box-shadow: 0 3px 0 #ccc, 0 -1px #fff inset;
        background: white;
        color:#888;
        border:none;
        outline:none;
        display: inline-block;
        -webkit-appearance:none;
        -moz-appearance:none;
        appearance:none;
        cursor:pointer;
    }

    </style>
    </head>
    <body>
    <header>
       <h1>Foxy Predictor</h1>
    </header>

    <select id="Polling Firms">
       <optgroup label="Polling Firms">
          <option value="Emnid">Emnid</option>
          <option value="Forsa">Forsa</option>
          <option value="Allensbach">Allensbach</option>
       </optgroup>
    </select>

    <select id="Model Class">
       <optgroup label="Model Class">
          <option value="Simple Model">Simple Model</option>
          <option value="Monte Carlo">Monte Carlo</option>
       </optgroup>
    </select>


    <div class="flex-container">
      <div class="flex-item">{{attrs[1]}}</div>
      <div class="flex-item">{{attrs[0]}}</div>
    </div>



    <footer>
       <h1>Copyright @ Foxy Predictor</h1>
    </footer>
    </body>
    </html>


    <ul>
      {% for attr in attrs %}
      <li>{{attr}}</li>
      {% endfor %}
    </ul>
    </html>
    """)

    output= template.render({'attrs': [xx, xxx]})

    Html_file= open("Dashboard.html","w")
    Html_file.write(output)
    Html_file.close()
