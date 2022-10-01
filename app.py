import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import os
from datetime import datetime, date, time, timedelta


DATASET = "file://" + os.getcwd() + "/air_quality.csv"
DATE_COLUMN = "TIME"
VALUES = ["PM25", "PM10", "AQI25", "AQI10"]
COLORS = ["red", "purple", "blue", "navyblue"]
ELEMENTS = 5000


@st.cache(show_spinner = False)
def load_data(filename = DATASET, nrows = None):
    # read csv file and fix names of dataframe columns
    data = pd.read_csv(filename, nrows = nrows)
    uppercase = lambda x: str(x).upper()
    data.rename(uppercase, axis = "columns", inplace = True)
    data.columns = ["TIME", "PM25", "PM10", "AQI25", "AQI10"]
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN], infer_datetime_format = True, utc = False)
    return data


#--- title/subtitle/info area ---
st.write("""
    #### A very basic dashboard app
    Hello happy testers!
    """)
#----------------------------------------------------


#--- this is the top container in the main window ---
top_container = st.expander("Info window", expanded = False)

# let the reader know the data is loading.
message = "Loading data..."
info_msg = top_container.info(message)

# Load full dataset into the dataframe and define a few variables
df = load_data()

nrows = df.shape[0]
ncols = df.shape[1]
start_date = df["TIME"].iloc[0].timetuple()[:3]
end_date   = df["TIME"].iloc[-1].timetuple()[:3]


# notify that the data was successfully loaded.
message += "done!"
info_msg.info(message)

message = f"Number of rows/columns: {df.shape}"
success_msg = top_container.success(message)

#st.write(df.head())
top_container.dataframe(df, height = 200)
#----------------------------------------------------


#--- this is the sidebar ---
option = st.sidebar.selectbox(
    'Choose what to plot:',
     VALUES
     )

st.sidebar.text(f"You selected: {option}")


dates_to_plot = st.sidebar.slider(
    label = "Select starting/ending dates (format: YYYY-MM-DD)",
    min_value = datetime(*start_date),
    max_value = datetime(*end_date),
    step = timedelta(weeks = 1),
    # value = (datetime(*start_date), datetime(*end_date)),
    value = (datetime(*end_date) - timedelta(weeks = 26), datetime(*end_date)),
    format = "YYYY-MM-DD"
    )

#--- THIS CODE NEEDS FURTHER FIXING ---
# min_points_to_plot = st.sidebar.slider(
#     label = "Select minimum number of points to plot",
#     min_value = 500,
#     max_value = 10000,
#     step = 500
#     )

# if st.sidebar.button("Reset dates", key = None, help = "Reset startind/ending dates"):
#     start_date = df["TIME"].iloc[0].timetuple()[:3]
#     end_date   = df["TIME"].iloc[-1].timetuple()[:3]


# # st.sidebar.bar_chart(df[option])
# start = st.sidebar.date_input("Start date", datetime(*start_date))
# end   = st.sidebar.date_input('End date',   datetime(*end_date))

#----------------------------------------------------


#--- this is the mid container in the main window ---
mid_container = st.expander(
    "Last measured data: " + str(datetime(*end_date)),
    expanded = True
    )


cols = mid_container.columns(4)
for i in range(4):
    cols[i].metric(
        label = VALUES[i],
        value = df[VALUES[i]].iloc[-1],
        delta = f"{df[VALUES[i]].iloc[-2]  - df[VALUES[i]].iloc[-1]:.2f}"
        )

#----------------------------------------------------


#--- TODO ---
#--- this is the bottom container in the main window ---

bottom_container = st.expander("Plot window", expanded = True)

df_plot = df[(df["TIME"] >= dates_to_plot[0]) & (df["TIME"] <= dates_to_plot[1])]

# # check if selection is less than minimum number of points
# if df_plot.shape[0] < min_points_to_plot:
#     # if true select again portion of dataframe to plot
#     # first setting the upper time limit
#     df_plot = df.loc[df["TIME"] <= dates_to_plot[1]]
#     print(f"df_plot < min_points_to_plot: {df_plot.shape[0]}")
#
#     # and then checking if selected dataframe is longer than minimum number of points
#     if df_plot.shape[0] >= min_points_to_plot:
#         # if true set lower time limit
#         # print(df.iloc[-min_points_to_plot][0])
#         # print(df.iloc[-1][0])
#         df_plot = df_plot.loc[
#             # (df["TIME"] >= df.iloc[-min_points_to_plot][0]) &
#             # (df["TIME"] <= df.iloc[-1][0])
#             df_plot["TIME"] >= df_plot.iloc[-min_points_to_plot][0]
#         ]
#         print(f"df_plot after last check: {df_plot.shape[0]}")
#     # otherwise, selected dataframe is shorter than minimum number of points
#     else:
#         # then start again from lower limit and go upwards for min_points_to_plot
#         df_plot = df.loc[df["TIME"] >= dates_to_plot[0]]
#         df_plot = df_plot.loc[
#             df_plot["TIME"] < df_plot.iloc[min_points_to_plot][0]
#             ]
#
#         print(f"df_plot after last check: {df_plot.shape[0]}")


chart = alt.Chart(df_plot).mark_line().encode(
    x = alt.X("TIME", axis = alt.Axis(labelAngle = 0, format="%d %b %Y")),
    y = alt.Y(option, axis = alt.Axis(labels = True))
    )


bottom_container.altair_chart(chart, use_container_width = True)
#----------------------------------------------------


#--- deletd/unused stuff ---

#----------------------------------------------------
# cols[0].metric(label = 'PM25',  value = df['PM25'].iloc[-1],  delta = f"{df['PM25'].iloc[-2]  - df['PM25'].iloc[-1]:.2f}")
# cols[1].metric(label = 'PM10',  value = df['PM10'].iloc[-1],  delta = f"{df['PM10'].iloc[-2]  - df['PM10'].iloc[-1]:.2f}")
# cols[2].metric(label = 'AQI25', value = df['AQI25'].iloc[-1], delta = f"{df['AQI25'].iloc[-2] - df['AQI25'].iloc[-1]:.2f}")
# cols[3].metric(label = 'AQI10', value = df['AQI10'].iloc[-1], delta = f"{df['AQI10'].iloc[-2] - df['AQI10'].iloc[-1]:.2f}")
#----------------------------------------------------


#----------------------------------------------------
# import matplotlib.pyplot as plt
# import plotly.figure_factory as ff

# plt.rc('font', size = 8)
# plt.xticks(rotation = 90)
#
# fig, ax = plt.subplots()
#
# ax.plot(df_plot["TIME"], df_plot[option], linewidth = "0.5")
# ax.grid(axis = "y")
# ax.set_xlabel("TIME")
# ax.set_ylabel(option)
#
# bottom_container.pyplot(fig)

# st.plotly_chart(fig, use_container_width = True)
#----------------------------------------------------

