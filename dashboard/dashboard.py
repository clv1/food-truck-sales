"""Generates Streamlit Dashboard"""
# pylint: disable=import-error, unused-import

import streamlit as st
import pandas as pd
import altair as alt

from dotenv import load_dotenv
from database_functions import get_db_connection, load_transaction_data

SORT_ORDER = "x"

load_dotenv()

conn = get_db_connection()
transactions_df = load_transaction_data(conn)
# transactions_df = pd.read_csv(
#     """/Users/kevinchirayil/Documents/Coursework/Week-9/
#       Coursework-Data-Engineering-Week-3/pipeline/
#       historical_truck_data/combined_historical_truck_data.csv""",
#       parse_dates=['time_stamp'])

st.dataframe(transactions_df)

st.title('Food Truck Dashboard')
st.write("A Streamlit dashboard for evaluating transaction data from T3's fleet of food trucks.")


# Hiram has two priorities: Cut costs, Raise profits.
# Information and metrics that would be useful for him are:

# -- TOTAL REVENUE: (bar chart) revenue by truck each in total
# -----> see where profits are coming from
# -- TRANSACTION VOLUME: (pie chart) transactions by truck per day (we have this?)
# -----> see which truck is most popular
# -- AVERAGE PURCHASE price: (bar chart) average purchase price by truck

# -- BONUS
# ---- REVENUE OVER TIME: (Line Chart or Area Chart)
# ---- CASH PROPORTION (pie chart) proportion of payments from cash
# -----> identify optimal money laundering vehicle (Hiram is secretly mafia)


# --- TOTAL REVENUE ---
st.subheader('Total Revenue by Truck')

# Group by truck_id and calculate total revenue
total_revenue_by_truck = transactions_df.groupby(
    'truck_id')['total'].sum().reset_index(name='total_revenue')

# Altair bar chart
chart = alt.Chart(total_revenue_by_truck).mark_bar().encode(
    x=alt.X("truck_id:N", title="Truck ID").sort(
        SORT_ORDER),  # Add title for x-axis
    y=alt.Y("total_revenue:Q", title="Total Revenue"))  # Add title for y-axis

# Display the chart
st.altair_chart(chart, use_container_width=True)


# --- TRANSACTION VOLUME ---
st.subheader('Number of Transactions by Truck')

# Group by truck_id and calculate the number of transactions
transactions_by_truck = transactions_df.groupby(
    'truck_id').size().reset_index(name='transaction_count')

# Altair pie chart
chart = alt.Chart(transactions_by_truck).mark_arc().encode(
    color="truck_id:N",
    theta="transaction_count",)
st.altair_chart(chart, use_container_width=True)


# --- AVERAGE PURCHASE ---
st.subheader('Average Purchase Value by Truck')

# Group by truck_id and calculate the average purchase price
average_price_by_truck = transactions_df.groupby(
    'truck_id')['total'].mean().reset_index(name='avg_purchase_value')

# Altair bar chart
chart = alt.Chart(average_price_by_truck).mark_bar().encode(
    x=alt.X("truck_id:N").sort(SORT_ORDER),
    y="avg_purchase_value")
st.altair_chart(chart, use_container_width=True)


# --- REVENUE OVER TIME ---
st.subheader('Revenue Over Time by Truck')

# multiselect for filtering by day
selected_days = st.multiselect(
    'Select Days', transactions_df['time_stamp'].dt.date.unique())
# Filter for selected days
filtered_df = transactions_df[transactions_df['time_stamp'].dt.date.isin(
    selected_days)]
# Group by truck_id and time_stamp, calculate total revenue
total_revenue_over_time = filtered_df.groupby(['truck_id', 'time_stamp'])[
    'total'].sum().reset_index()

# # Group by truck_id and time_stamp, calculate total revenue
# total_revenue_over_time = transactions_df.groupby(['truck_id', 'time_stamp'])[
#     'total'].sum().reset_index()

# Altair line chart
chart = alt.Chart(total_revenue_over_time).mark_line().encode(
    x='time_stamp:T',
    y='total',
    color='truck_id:N')
st.altair_chart(chart, use_container_width=True)
