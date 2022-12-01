"""
Functions to create the plots used in plot_bids.py
"""

from datetime import datetime, date, timedelta 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from query_supabase import *


def get_duid_station_options(start_time: str, regions: list, duration: str):
    """
    Gets the duids and corresponding station names of all units that are 
    based within the given regions and have made bids during the specified 
    timeframe, as well as station names of all stations that include such units. 

    Arguments:
        start_time: Initial datetime in the format "YYYY/MM/DD HH:MM:SS"
        regions: List of specified regions
        duration: Duration of time period. Either "Daily" or "Weekly" 
    Returns:
        Dataframe - column "DUID" contains unit duids, column "STATION NAME" 
            contains name of station that each unit belongs to
    """
    start_time_obj = datetime.strptime(start_time, "%Y/%m/%d %H:%M:%S")
    if duration == 'Daily':
        end_time = (start_time_obj + timedelta(days=1)).strftime("%Y/%m/%d %H:%M:%S")
        return stations_and_duids_in_regions_and_time_window(regions, start_time, end_time)
    if duration == 'Weekly':
        end_time = (start_time_obj + timedelta(days=7)).strftime("%Y/%m/%d %H:%M:%S")
        return stations_and_duids_in_regions_and_time_window(regions, start_time, end_time)


def plot_duid_bids(start_time: str, end_time: str, resolution: str, duids: list):
    """
    Plots a stacked bar chart showing the bid volumes for each unit specified in 
    the 'duids' list. 

    x-axis: Bid volume. Stacked bars sorted by bid price in ascending order. 
    y-axis: Datetime. Bids will be displayed at 5 min intervals if time period 
        is 1 day or hourly intervals if time period is 1 week. 
    Colour: Bid price for each volume bid. 

    Arguments:
        start_time: Initial datetime in the format "YYYY/MM/DD HH:MM:SS"
        end_time: Ending datetime, formatted identical to start_time
        resolution: Either 'hourly' or '5-min
        duids: list of unit duids
    Returns: 
        Plotly express figure (stacked bar chart)
    """
    stacked_bids = duid_bids(duids, start_time, end_time, resolution)
    stacked_bids = stacked_bids.groupby(["INTERVAL_DATETIME", "BIDPRICE"], as_index=False).agg({"BIDVOLUME": "sum"})

    stacked_bids.sort_values(by=["BIDPRICE"], inplace=True)
    fig = px.bar(
        stacked_bids, 
        barmode="stack",
        x='INTERVAL_DATETIME', 
        y='BIDVOLUME', 
        color='BIDPRICE',
        labels={
            "BIDPRICE": "Bid Price", 
            'BIDVOLUME': "Bid Volume",
        },
        hover_data={
            'INTERVAL_DATETIME': True, 
            'BIDPRICE': ':.0f', 
            'BIDVOLUME': ':.0f',
        }, 
        custom_data=['BIDPRICE'],
    )

    fig.update_yaxes(title="Volume (MW)")
    fig.update_traces(hovertemplate="%{x}<br>Bid Price: $%{customdata[0]:.0f}<br>Bid Volume: %{y:.0f} MW")
    fig.update_layout(height=400)
    if resolution == "hourly":
        fig.update_xaxes(title=f"Time (Bid stack sampled on the hour)")
    else:
        fig.update_xaxes(title=f"Time (Bid stack sampled at 5 min intervals)")

    return fig


def plot_aggregate_bids(start_time:str, end_time:str, resolution:str, regions:list, show_demand: bool):
    """
    Plots a stacked bar chart showing the aggregate bids for the specified 
    regions grouped into a set of predefined bins. If show_demand is True, total 
    electricity demand for all specified regions is plotted on top of the 
    aggregated bids. Relies on query_supabase.aggregate_bids.

    x-axis: Bid volume. Stacked bars sorted from lowest price bin to highest. 
    y-axis: Datetime. Bids will be displayed at 5 min intervals if time period 
        is 1 day or hourly intervals if time period is 1 week. 
    Colour: Price bin that each bid's price falls into. 

    Arguments:
        start_time: Initial datetime in the format "YYYY/MM/DD HH:MM:SS"
        end_time: Ending datetime, formatted identical to start_time
        resolution: Either 'hourly' or '5-min
        regions: list of specified regions
        show_demand: True if electricity demand is to be plotted over figure, 
            otherwise False
    Returns: 
        Plotly express figure (stacked bar chart)
    """
    stacked_bids = aggregate_bids(regions, start_time, end_time, resolution)
    stacked_bids = stacked_bids.groupby(["INTERVAL_DATETIME", "BIN_NAME"], as_index=False).agg({"BIDVOLUME": "sum"})
    bid_order = [ 
        "[-1000, -100)", "[-100, 0)", "[0, 50)", "[50, 100)", "[100, 200)", 
        "[200, 300)", "[300, 500)", "[500, 1000)", "[1000, 5000)", 
        "[5000, 10000)", "[10000, 15500)", 
    ]
    color_map = {}
    color_sequence = [
        "lightsalmon", "yellow", "red", 'orange', '#00cc96', 
        '#636efa', 'purple', 'cyan', 'fuchsia', 'palegreen', 'lightblue'
    ]
    for i in range(len(bid_order)):
        color_map[bid_order[i]] = color_sequence[i]

    fig = px.bar(
        stacked_bids, 
        x='INTERVAL_DATETIME', 
        y='BIDVOLUME', 
        category_orders={"BIN_NAME": bid_order},
        color='BIN_NAME',
        color_discrete_map=color_map,
        labels={"BIN_NAME": "Price Bin"},
    )

    # Update graph axes and hover text
    fig.update_yaxes(title="Volume (MW)")
    fig.update_traces(hovertemplate="%{x}<br>Bid Volume: %{y:.0f} MW<extra></extra>")
    fig.update_layout(height=400)
    if resolution == "hourly":
        fig.update_xaxes(title=f"Time (Bid stack sampled on the hour)")
    else:
        fig.update_xaxes(title=f"Time (Bid stack sampled at 5 min intervals)")

    if show_demand:
        fig = add_demand_trace(fig, start_time, end_time, regions)

    return fig


def add_demand_trace(fig, start_time: str, end_time: str, regions: list):
    """
    Adds the line plot showing electricity demand to an existing figure. Plots 
    total demand over the given time period for the specified regions. 

    x-axis: Volume of electricity demand (MW). 
    y-axis: Datetime. Bids will be displayed at 5 min intervals if time period 
        is 1 day or hourly intervals if time period is 1 week. 
    
    Arguments:
        fig: plotly express figure
        start_time: Initial datetime in the format "YYYY/MM/DD HH:MM:SS"
        end_time: Ending datetime, formatted identical to start_time
        regions: list of specified regions
    Returns:
        Updated plotly express figure consisting of the electricity demand curve 
        plotted on top of the original figure 
    """
    demand = region_data(start_time, end_time)
    demand.loc[:,"REGIONID"] = demand["REGIONID"].str[:-1]
    demand = demand[demand["REGIONID"].isin(regions)]
    demand = demand.groupby(["SETTLEMENTDATE"], as_index=False).agg({"TOTALDEMAND": "sum"})
    fig.add_trace(go.Scatter(x=demand['SETTLEMENTDATE'], y=demand['TOTALDEMAND'],
                                marker=dict(color='blue', size=4), name='Demand'))
    fig.update_traces(
        hovertemplate="%{x}<br>Demand: %{y:.0f} MW<extra></extra>",
        selector={"name": "Demand"}
    )
    return fig


def plot_bids(start_time:str, end_time:str, resolution:str, regions:list, duids: list, show_demand: bool, show_price: bool):
    """
    Plots volume bids over time based on the given parameters. See 
    plot_duid_bids, plot_aggregate_bids and add_price_subplot for more info. 

    Arguments: 
        start_time: Initial datetime in the format "YYYY/MM/DD HH:MM:SS"
        end_time: Ending datetime, formatted identical to start_time
        resolution: Either '5-min' or 'hourly'
        regions: list of specified regions
        duids: list of specified unit duids. If this empty, only the specified 
            duid bids will be plotted, otherwise aggregate bids for the given 
            timeframe and regions will be plotted
        show_demand: True if electricity demand is to be plotted over figure, 
            otherwise False
        show_price: Bool. If True, the figure returned will consist of 2 
            subplots, 1 showing bids and 1 showing average electricity prices
            over the same timeframe. If False, only bids will be plotted. 
    Returns:
            Plotly express figure if show_price is False. Plotly go subplot if 
            show_price is True. 
    """
    if (duids):
        fig = plot_duid_bids(start_time, end_time, resolution, duids)
    else: 
        fig = plot_aggregate_bids(start_time, end_time, resolution, regions, show_demand)
    
    if show_price:
        return add_price_subplot(fig, start_time, end_time, regions, resolution)
    return fig



def add_price_subplot(fig, start_time: str, end_time: str, regions: list, resolution: str):
    """
    Takes a plotly express figure plotting bids and puts it into a plotly go 
    subplot consisting of the original figure on top with the average 
    electricity price plotted below. The figures share their x-axis (datetime). 
    The data from the original figure is removed and appended to a plotly go 
    figure so it will be compatible with the subplot (plotly express does not 
    support subplots). Electricity price is first plotted as a plotly express 
    figure, the data is removed and appended to the subplot. 
    See plot_price for more info. 

    Arguments:
        fig: plotly express figure
        start_time: Initial datetime in the format "YYYY/MM/DD HH:MM:SS"
        end_time: Ending datetime, formatted identical to start_time
        regions: list of specified regions
        resolution: Either '5-min' or 'hourly'
    Returns:
        plotly go subplot containing original bid plot on top and electricity 
        price below
    """
    #TODO fix overlap in legend entry when plotting with duid bids
    price_graph = plot_price(start_time, end_time, regions, resolution)

    plot = make_subplots(
        rows=2,
        cols=1, 
        shared_xaxes=True,
        row_heights=[0.66, 0.34],
        vertical_spacing=0.03,
    )

    bid_traces = []
    for i in range(len(fig["data"])):
        bid_traces.append(fig["data"][i])
    price_trace = price_graph["data"][0]
    for trace in bid_traces:
        plot.append_trace(trace, row=1, col=1)
    price_trace["showlegend"] = True
    price_trace["name"] = "Electricity Price"
    plot.add_trace(price_trace, row=2, col=1)

    plot.update_layout(
        {"barmode": "stack", "height": 600},
        coloraxis_colorscale="Plasma",
    )
    plot.update_yaxes(
        title_text="Volume (MW)", 
        row=1, 
        col=1
    )
    plot.update_yaxes(
        title_text="Average electricity<br>price ($/MWh)",
        range=[0, 199],
        row=2, 
        col=1
    )
    if resolution == "hourly":
        plot.update_xaxes(title_text="Time (Bid stack sampled on the hour)", row=2, col=1)
    else:
        plot.update_xaxes(title_text="Time (Bid stack sampled at 5 min intervals)", row=2, col=1)
    
    return plot

def plot_price(start_time, end_time, regions, resolution):
    """
    TODO
    """
    prices = get_aggregated_vwap(regions, start_time, end_time)
    prices = prices.sort_values(by="SETTLEMENTDATE")
    if resolution == "hourly":
        prices = prices[prices["SETTLEMENTDATE"].str.contains(":00:00")]

    price_graph = px.line(
        prices, 
        x = "SETTLEMENTDATE", 
        y = "PRICE", 
        labels={
            "SETTLEMENTDATE": "Time", 
            "PRICE": "Average electricity price ($/MWh)",
        }, 
        color_discrete_sequence=["red"], 
    )
    price_graph.update_traces(hovertemplate="%{x}<br>Price: $%{y:.2f}/MWh<extra></extra>")
    return price_graph



    