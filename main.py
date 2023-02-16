#Import lyb
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
#import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Revenue Collection Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

#@st.cache
def get_data_from_excel():
    df = pd.read_excel(
            io=r"C:\Users\Alfred\Documents\trv demo report.xlsx",
            engine="openpyxl",
            sheet_name=0,
            #skiprows=0,
            usecols="A:S",
            nrows=1000
            )
    # Add hour column to df
    #df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df
df = get_data_from_excel()

#print(df.head())
#st.dataframe(df)


# Side bar
st.sidebar.header("Please Filter here: ")
zone = st.sidebar.multiselect(
    "Select the zone",
    options=df["ZONE"].unique(),
    default=df["ZONE"].unique()
)

market = st.sidebar.multiselect(
    "Select the Market",
    options=df["MARKET"].unique(),
    default=df["MARKET"].unique()
)

produce = st.sidebar.multiselect(
    "Select the Produce",
    options=df["PRODUCE"].unique(),
    default=df["PRODUCE"].unique()
)

df_selection = df.query(
    "ZONE == @zone & MARKET == @market & PRODUCE == @produce"
)

# Main page
st.title(":bar_chart: Revenue Dashboard")
st.markdown("##")

# Top KPI
total_sales = df_selection["TOTAL AMOUNT PIAD IN"].sum()
average_rating = round(df_selection["TOTAL QUANTITY SEEN"].mean(), 1)
star_rating = ":star:" #* int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["TOTAL AMOUNT PIAD IN"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Revenue:")
    st.subheader(f"N {total_sales:,}")

with middle_column:
    st.subheader("Average Rating")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Revenue Per Transaction")
    st.subheader(f"N{average_sale_by_transaction:,}")

st.markdown("---")

# sales_by_product_line = (
# df_selection.groupby(by=["PRODUCE"][["TOTAL AMOUNT PIAD IN"]]).sort_values(by=["Total"]))

sales_by_product_line = (df.groupby("ZONE")["TOTAL AMOUNT PIAD IN"].sum().sort_values().round())
fig_product_sales = px.bar(
    sales_by_product_line,
    x="TOTAL AMOUNT PIAD IN",
    #y=sales_by_product_line.unique(),
    #orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=(["#0083B8"] * len(sales_by_product_line)),
    template=("plotly_white"))


st.plotly_chart(fig_product_sales)

mean_price_per_zone = df.groupby("ZONE")["TOTAL AMOUNT PIAD IN"].sum().sort_values().round()
chart = mean_price_per_zone.plot.bar(title="Mean Price per market", x="Region", y="Mean Price")
print(chart)


#df1 = pd.read_excel(r"C:\Users\Alfred\Documents\monthly_collections.xlsx")
#print(df1)
#st.line_chart(data=df1[:], x=None, y=None, width=0, height=0, use_container_width=True)

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)


# Hide streamlit styles
hide_st_style = """
            <style>
            #MainMenu {visibility:hidden;}
            footer {visibility:hidden;}
            header {visibility:hidden;}
            </style>
"""
