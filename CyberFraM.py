#!/usr/bin/env python
# coding: utf-8

# import


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import json
import re
from datetime import date


# database


current = pd.read_excel("framework.xlsx", sheet_name = "current_profile")
target = pd.read_excel("framework.xlsx", sheet_name = "target_profile")
references = pd.read_excel("framework.xlsx", sheet_name = "references")
gantt = pd.read_excel("framework.xlsx", sheet_name = "gantt")


# app


app = dash.Dash(__name__)
app.title = "CyberFraM"
server = app.server


# # elements


intro_text = """
Questa dashboard ipotizza l'applicazione del [**Framework Nazionale per la Cybersecurity e la Data Protection**]
(https://www.cybersecurityframework.it/) ad una organizzazione/impresa di piccole dimensioni.  
La fase preliminare - fittizia in questo caso - consiste nella selezione delle funzioni, categorie e sottocategorie
applicabili al caso concreto. Nel primo *step* si identificano i controlli già applicati ed il relativo livello di
maturità, individuando così il profilo attuale dell'organizzazione (**profilo corrente**). Nel secondo *step* si
individuano i controlli da migliorare (nel livello di maturità) e quelli da implementare *ex novo*, realizzando quello
che è l'obiettivo da raggiungere nell'arco dei prossimi mesi: il **profilo target**.  
Si realizza quindi un gantt chart fissando le date desiderate di completamento delle varie sottocategorie, quantomeno
di quelle con alta priorità.  
La dashboard ha l'obiettivo di monitorare il contenuto dei due profili ed i progressi nell'implementazione.
"""

gauge_trace = go.Indicator(mode = "gauge+number", 
                           value = gantt.Complete.mean(), 
                           gauge = {
                               'axis': {'range': [0, 100], 'tickwidth': 1},
                               'bar': {'color': "orange"},
                               'bgcolor': "white",
                               'borderwidth': 2,
                               'bordercolor': "gray",
                               'steps': [
                                   {'range': [0, 50], 'color': 'lightblue'},
                                   {'range': [50, 90], 'color': 'green'}],
                               'threshold': {
                                   'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75,
                                   'value': 98}
                           })
gauge_data = [gauge_trace]
gauge_layout = go.Layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                         margin = dict(l=40, r=40, t=0, b=0), width = 300, height = 300)
gauge_figure = go.Figure(data = gauge_data, layout = gauge_layout)

radio_options = [
    {"label" : "Funzioni", "value" : "Function"},
    {"label" : "Categorie", "value" : "Category_ID"},
    {"label" : "SottoCategorie", "value" : "Task"}
]

verify = gantt[gantt.Finish <= date.today().strftime("%d/%m/%Y")]
mask = verify.loc[:, "Complete"] == 100
completed = verify[mask].groupby("Priority").count()
mask = verify.loc[:, "Complete"] != 100
incompleted = verify[mask].groupby("Priority").count()
x1 = completed.index
y1 = completed["Complete"].values
completed_graph = go.Bar(x = x1, y = y1, name = "Completate", opacity = 0.7, marker_color='green', 
                         marker_line_color='#002D62', textposition = 'outside', text = y1, hoverinfo = "y")
x2 = incompleted.index
y2 = incompleted["Complete"].values
incompleted_graph = go.Bar(x = x2, y = y2, name = "Incomplete", opacity = 0.7, marker_color='red', 
                           marker_line_color='#002D62', textposition = 'outside', text = y2, hoverinfo = "y")
data = [completed_graph, incompleted_graph]
layout = go.Layout(barmode = "group", paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)',
                   width = 550, height = 380, xaxis = dict(title = "Livello di priorità"),
                   yaxis = dict(title = "SubCategories (count)"), margin = dict(l=40, r=40, t=0, b=0), legend = dict(x = -.1, y = 1.2))
complete_figure = go.Figure(data = data, layout = layout)

gantt_funcs = gantt.Function.unique()
markers = [i for i in range(len(gantt_funcs))]
marks = {m:{"label":gantt_funcs[m],"style":{"color" : "#002D62"}} for m in markers}

message = "Utilizzare i menu a tendina, in alto a destra, per visualizzare le info su Categorie e Subcategorie del Framework."


# layout


# Div 0 - contenitore generale
app.layout = html.Div(className = "main-window", children = [
    
    # Div 1 - titolo
    html.Div(className = "title", children = [
        
        html.H1("CyberSecurity Framework Monitoring")
        
    ]),
    
    # Div 2 - testo di presentazione
    html.Div(className = "intro-text", children = [
        
        dcc.Markdown(children = intro_text)
        
    ]),
    
    # Div 3 - info sugli oggetti del treemap
    html.Div(className = "output-info", children = [
        
        dcc.Markdown(id = "output-info")
        
    ]),
    
    # Div 4 - label Profile
    html.Div(className = "labelProfile", children = [
        
        html.H3("Profile", className = "h3")
        
    ]),
    
    # Div 5 - label Function
    html.Div(className = "labelFunction", children = [
        
        html.H3("Function")
        
    ]),
    
    # Div 6 - menu a tendina profili
    html.Div(className = "menuProfile", children = [
        
        dcc.Dropdown(id = "profile_picker", 
                     options = [{"label":prof,"value":prof} for prof in ["Corrente", "Target"]],
                     value = "Corrente")
        
    ]),
    
    # Div 7 - menu a tendina funzioni
    html.Div(className = "menuFunction", children = [
        
        dcc.Dropdown(id = "func_picker")
        
    ]),
    
    # Div 8 - grafico Treemap del profilo
    html.Div(className = "framework-graph", children = [
        
        dcc.Graph(id = "framework_graph")
        
    ]),
    
    # Div 9 - label Gauge
    html.Div(className = "labelGauge", children = [
        
        html.Pre("Completamento complessivo Medio")
        
    ]),
    
    # Div 10 - grafico gauge del completamento medio complessivo
    html.Div(className = "gauge", children = [
        
        dcc.Graph(id = "gauge-graph", figure = gauge_figure, className = "gauge-graph")
        
    ]),
    
    # Div 11 - label Complete
    html.Div(className = "labelComplete", children = [
        
        html.Pre("SubCatategorie completate")
        
    ]),
    
    # Div 11.2
    html.Div(className = "labelComplete2", children = [
        
        html.Pre("per livello di priorità")
        
    ]),
    
    # Div 12 - grafico a barre del completamento per priorità
    html.Div(className = "complete", children = [
        
        dcc.Graph(id = "complete-graph", figure = complete_figure, className = "complete-graph")
        
    ]),
    
    # Div 13 - slider
    html.Div(className = "slider", children = [
        
        dcc.Slider(id = "func-slider", min = min(markers), max = max(markers), step = None, marks = marks, 
                   value = min(markers))
        
    ]),
    
    # Div 14 - label Gantt
    html.Div(className = "labelGantt", children = [
        
        html.Pre("Selezionare la funzione dalla sovrastante slider")
        
    ]),
    
    # Div 15 - gantt
    html.Div(className = "gantt", children = [
        
        dcc.Graph(id = "gantt-graph", className = "gantt-graph")
        
    ]),
    
    # Div 16 - table
    html.Div(className = "final", children = [
        
        # label Table
    html.Pre("Completamento medio specifico", className = "labelTable"),
    
        # radio buttons
    dcc.RadioItems(id = "radio-buttons", options = radio_options, value = "Function", className = "radioItem"),
    
    html.Div(className = "table-graph", children = [
    
        #tabella
    dash_table.DataTable(id = "table-graph", page_action = 'none', 
                         style_table = {'height' : '300px', 
                                        'overflowY': 'auto'},
                         style_cell={'textAlign': 'center', 'backgroundColor' : '#92A8D1'},
                         style_as_list_view = True,
                         style_header = {'backgroundColor' : 'white', 'fontWeight' : 'bold'},
                         css = [{'selector' : 'table', 'rule' : 'table-layout: fixed'}])  
        
    ]),
    
    html.Pre("Realizzata da Dario Brocato", className = "credits1"),
        
    dcc.Markdown("utilizzando [Plotly](https://plotly.com/) e [Dash](https://plotly.com/dash/).", 
                 className = "credits2"),
        
    dcc.Markdown("Il [framework](https://www.cybersecurityframework.it/) è realizzato dal CIS Sapienza e dal CINI.", 
             className = "credits3")
        
    ])
        
])


# functions


@app.callback(Output('func_picker', 'value'),
              [Input('func_picker', 'options')])
def callback(value):
    return ""

@app.callback(Output('func_picker', 'options'),
              [Input('profile_picker', 'value')])
def func_picker(value):
    if value == "Corrente":
        return [{"label":func,"value":func} for func in current.Function.unique()]
    else:
        return [{"label":func,"value":func} for func in target.Function.unique()]

@app.callback(Output('framework_graph', 'figure'),
              [Input('profile_picker', 'value'), Input('func_picker', 'value')])
def framework_graph(profile, xvalue):
    height = 540
    width = 850
    margins = dict(l=20, r=0, b=0, t=100, pad=4)
    fonts = dict(family = "Courier New, monospace", color = "#002D62")
    mapcolor = ["#92A8D1"]
    opacity = 0.9
    hoverinfo = "label+text"
    textposition = "top center"
    textinfo = "label"
    textfont = dict(family = "Courier New, monospace", color = "white", size = 14)
    
    if profile == "Corrente":
        if xvalue:
            mask = current.loc[:, "Function"] == xvalue
            labels = [cat for cat in current[mask]["Category_ID"].unique()]
            num_labels = len(labels)
            text = ["Category" for cat in labels]
            parents = [xvalue for i in range(num_labels)]
            for cat in labels:
                mask2 = current.loc[:, "Category_ID"] == cat
                subs = [sub for sub in current[mask2]["Subcategory_ID"].unique()]
                for sub in subs:
                    parents.append(cat)
                    labels.append(sub)
                    text.append("SubCategory")
            labels.insert(0, xvalue)
            labels.insert(0, "Cybersecurity Framework")
            parents.insert(0, "Cybersecurity Framework")
            parents.insert(0, "")
            text.insert(0, "Function")
            text.insert(0, "")

            trace = go.Treemap(labels = labels, parents = parents, text = text, opacity = opacity,
                               hoverinfo = hoverinfo, textposition = textposition, textinfo = textinfo,
                               textfont = textfont)
            data = [trace]
            layout = go.Layout(title = "CURRENT PROFILE", height = height, width = width, font = fonts,
                               paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', margin = margins,
                               treemapcolorway = mapcolor)

            return dict(data = data, layout = layout)
        else:
            labels = [func for func in current.Function.unique()]
            num_labels = len(labels)
            labels.insert(0, "Functions")
            labels.insert(0, "Cybersecurity Framework")
            text = ["Function" for i in range(num_labels)]
            parents = ["Functions" for i in range(num_labels)]
            parents.insert(0, "Cybersecurity Framework")
            parents.insert(0, "")
            text.insert(0, "Functions")
            text.insert(0, "")

            trace = go.Treemap(labels = labels, parents = parents, opacity = opacity, hoverinfo = hoverinfo,
                               text = text, textposition = textposition, textinfo = textinfo, textfont = textfont)
            data = [trace]
            layout = go.Layout(title = "CURRENT PROFILE", height = height, width = width, font = fonts,
                               paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', margin = margins,
                               treemapcolorway = mapcolor)

            return dict(data = data, layout = layout)
    else:
        if xvalue:
            mask = target.loc[:, "Function"] == xvalue
            labels = [cat for cat in target[mask]["Category_ID"].unique()]
            num_labels = len(labels)
            text = ["Category" for cat in labels]
            parents = [xvalue for i in range(num_labels)]
            for cat in labels:
                mask2 = target.loc[:, "Category_ID"] == cat
                subs = [sub for sub in target[mask2]["Subcategory_ID"].unique()]
                for sub in subs:
                    parents.append(cat)
                    labels.append(sub)
                    text.append("SubCategory")
            labels.insert(0, xvalue)
            labels.insert(0, "Cybersecurity Framework")
            parents.insert(0, "Cybersecurity Framework")
            parents.insert(0, "")
            text.insert(0, "Function")
            text.insert(0, "")

            trace = go.Treemap(labels = labels, parents = parents, text = text, opacity = opacity,
                               hoverinfo = hoverinfo, textposition = textposition, textinfo = textinfo, 
                               textfont = textfont)
            data = [trace]
            layout = go.Layout(title = "TARGET PROFILE", height = height, width = width, font = fonts,
                               paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', margin = margins,
                               treemapcolorway = mapcolor)

            return dict(data = data, layout = layout)
        else:
            labels = [func for func in target.Function.unique()]
            num_labels = len(labels)
            labels.insert(0, "Functions")
            labels.insert(0, "Cybersecurity Framework")
            text = ["Function" for i in range(num_labels)]
            parents = ["Functions" for i in range(num_labels)]
            parents.insert(0, "Cybersecurity Framework")
            parents.insert(0, "")
            text.insert(0, "Functions")
            text.insert(0, "")

            trace = go.Treemap(labels = labels, parents = parents, opacity = opacity, hoverinfo = hoverinfo,
                               text = text, textposition = textposition, textinfo = textinfo, textfont = textfont)
            data = [trace]
            layout = go.Layout(title = "TARGET PROFILE", height = height, width = width, font = fonts,
                               paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', margin = margins,
                               treemapcolorway = mapcolor)

            return dict(data = data, layout = layout)

@app.callback(Output('output-info', 'children'),
              [Input('profile_picker', 'value'), Input('framework_graph', 'hoverData')])
def output_test(profile, hoverData):
    data = json.dumps(hoverData)
    
    try:
        check = re.search("(?:currentPath[\"']:\s[\"'])(.[^\"']*)", data)
        currentPath = check.group(1)
        check2 = re.search("(?:label[\"']:\s[\"'])(.[^\"']*)", data)
        label = check2.group(1)
    except:
        return message, ""
    
    if profile == "Corrente":
        if currentPath.find("/") == 0:
            return message, ""
        elif currentPath.count("/") == 1 and currentPath[-1] == "/":
            return message, ""
        elif currentPath.count("/") == 2:
            mask = current.loc[:,"Category_ID"] == label
            return current[mask].iloc[0,1]
        elif currentPath.count("/") > 2:
            mask = current.loc[:,"Subcategory_ID"] == label
            mask2 = references.loc[:,"Subcategory"] == label
            return current[mask].iloc[0,2] + "  \n  \nRiferimenti:  \n  \n" + "  \n".join(references[mask2].iloc[:,1].values) + "  \n  \nLivello di maturità: " + current[mask].iloc[0,-1]
    else:
        if currentPath.find("/") == 0:
            return message, ""
        elif currentPath.count("/") == 1 and currentPath[-1] == "/":
            return message, ""
        elif currentPath.count("/") == 2:
            mask = target.loc[:,"Category_ID"] == label
            return target[mask].iloc[0,1]
        elif currentPath.count("/") > 2:
            mask = target.loc[:,"Subcategory_ID"] == label
            mask2 = references.loc[:,"Subcategory"] == label
            return target[mask].iloc[0,2] + "  \n  \nRiferimenti:  \n  \n" + "  \n".join(references[mask2].iloc[:,1].values) + "  \n  \nLivello di maturità: " + target[mask].iloc[0,5]
   
@app.callback([Output('table-graph', 'columns'), Output('table-graph', 'data')],
              [Input('radio-buttons', 'value')])
def table(value):
    if value == "Function" or value == "Category_ID":
        group = gantt.groupby(value).mean()["Complete"].sort_values(ascending = False)
        columns = [{"name" : value, "id" : value}, 
                   {"name" : "Percentuale di completamento media", "id" : "Percentuale di completamento media"}]
        data = [{value:index,"Percentuale di completamento media":str(round(group[index],2)) + " %"} for index in group.index]
        
        return columns, data
    else:
        group = gantt.loc[:, ["Task", "Complete"]].set_index("Task").sort_values("Complete", ascending = False)
        columns = [{"name" : "SubCategory", "id" : "SubCategory"}, 
                   {"name" : "Percentuale di completamento", "id" : "Percentuale di completamento"}]
        data = [{"SubCategory":index,"Percentuale di completamento":str(round(group.loc[index,"Complete"],2)) + " %"} for index in group.index]
        
        return columns, data

@app.callback(Output('gantt-graph', 'figure'),
              [Input('func-slider', 'value')])
def gantt_graph(value):
    mask = gantt.loc[:, "Function"] == marks[value]["label"]
    
    fig = ff.create_gantt(gantt[mask], colors = "Cividis", index_col = 'Complete', show_colorbar = True, 
                          bar_width = 0.2, showgrid_x = True, showgrid_y = True)
    fig.update_layout(paper_bgcolor = 'rgba(0,0,0,0)', plot_bgcolor = 'rgba(0,0,0,0)', xaxis = dict(title = "Timing"),
                      yaxis = dict(title = "SubCategories (Tasks)"), 
                      title = "Gantt (Function: " + marks[value]["label"] + ")")

    return fig


# run


if __name__ == "__main__":
    app.run_server()