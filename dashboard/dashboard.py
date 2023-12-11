import streamlit as st

"""
# Proyek Analisis Data: Air Quality
- Nama: Moh. Hasbi Assidiqi
- Email: hasbi@pens.ac..id
- Id Dicoding: mohhasbias
"""

"""
## Menentukan Pertanyaan Bisnis
- Bagaimana Air Quality dari masing-masing area?
- Bagaimana Tren Air Quality dari masing-masing area dari waktu ke waktu?
"""

"""
## Menyiapkan semua library yang dibutuhkan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import datetime
import os
from fnmatch import fnmatch

"""
## Data Wrangling
### Gathering Data
"""

files = os.listdir('../data')
# files

PRSA_CSV_Files = [file for file in files if fnmatch(file, 'PRSA*.csv')]
PRSA_CSV_Files

df = pd.DataFrame()
for file in PRSA_CSV_Files:
    df_temp = pd.read_csv('../data/' + file)
    df = pd.concat([df, df_temp], ignore_index=True)

"""
head
"""
st.write(df.head())

"""
tail
"""
st.write(df.tail())

"""
### Assessing Data
"""

"""
Get data info
"""
import io

buffer = io.StringIO()
df.info(buf=buffer)
s = buffer.getvalue()
st.text(s)

"""
Check for missing values
"""
st.write(df.isna().sum())

"""
Check for duplicates
"""
st.write(df.duplicated().sum())

"""
Show descriptive statistics
"""
st.write(df.describe())

"""
### Cleaning Data
"""

"""
Drop duplicates
"""
df.drop_duplicates(inplace=True)

"""
Get is na for column pm2.5
"""
st.write(df[df["PM2.5"].isna()])

"""
Get count of values for each station
"""
st.write(df["station"].value_counts())

"""
Get count of values of PM2.5
"""
st.write(df["PM2.5"].value_counts())

"""
Get most frequent value of PM2.5
"""
st.write(df["PM2.5"].value_counts().index[0])

"""
Get columns with missing values
"""
columns_with_missing_values = df.columns[df.isna().any()].tolist()
st.write(columns_with_missing_values)

"""
Fill missing values with most frequent value for all columns
"""
"""
before filling missing values
"""
st.write(df.isna().sum())

for column in columns_with_missing_values:
    df[column].fillna(df[column].value_counts().index[0], inplace=True)

"""
after filling missing values
"""
st.write(df.isna().sum())

"""
Add new column date from columns year, month, day, hour
"""
df["date"] = pd.to_datetime(
    df[["year", "month", "day", "hour"]], format="%Y%m%d%H"
)

st.write(df.head())

"""
Add new column weekday from column date
"""
df["weekday"] = df["date"].dt.weekday

st.write(df.head())

"""
## Exploratory Data Analysis (EDA)
"""

"""
### Explore PM2.5 distribution for each station.
PM2.5 adalah partikel kecil yang dapat mencapai paru-paru dan bahkan aliran darah.
PM2.5 adalah indikator yang baik untuk mengukur polusi udara.
Semakin tinggi nilai PM2.5, semakin buruk kualitas udara.
"""

"""
## Visualization & Explanatory Analysis
"""

"""
### Pertanyaan 1:
Bagaimana Air Quality dari masing-masing area?
"""

"""
Get average PM2.5 for each station
"""
df_area = df.groupby("station")["PM2.5"].agg(["mean", "std"]).reset_index()
df_area

"""
Plot bar chart for average PM2.5 for each station
"""

def plot_bar_chart(df, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    # plt.show()
    st.pyplot(plt.gcf())

plot_bar_chart(
    df_area,
    x="station",
    y="mean",
    title="Average PM2.5 for each station",
    xlabel="Station",
    ylabel="Average PM2.5",
)


import plotly.express as px

# visualize PM2.5 over time for each area
df_reset_index = df.reset_index()

fig = px.line(df_reset_index, x="date", y="PM2.5", color="station", title="PM2.5 untuk setiap area", labels={"date": "Tanggal", "PM2.5": "PM2.5"})

# fig.show()
st.plotly_chart(fig)

"""
### Pertanyaan 2:
Bagaimana Tren Air Quality dari masing-masing area dari waktu ke waktu?
"""

"""
Get average PM2.5 for each year
"""
df_year = df.groupby("year")["PM2.5"].agg(["mean", "std"]).reset_index()
df_year

"""
Plot line chart for average PM2.5 for each year
"""
def plot_line_chart(df, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x, y=y, data=df)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    # xticks only on years not fractional years
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # plt.show()
    st.pyplot(plt.gcf())


plot_line_chart(
    df_year,
    x="year",
    y="mean",
    title="Average PM2.5 for each year",
    xlabel="Year",
    ylabel="Average PM2.5",
)

"""
Get average PM2.5 for each month
"""
df_month = df.groupby("month")["PM2.5"].agg(["mean", "std"]).reset_index()
df_month

"""
Plot bar chart for average PM2.5 for each month
"""
plot_bar_chart(
    df_month,
    x="month",
    y="mean",
    title="Average PM2.5 for each month",
    xlabel="Month",
    ylabel="Average PM2.5",
)

"""
Get average PM2.5 for each day
"""
df_day = df.groupby("day")["PM2.5"].agg(["mean", "std"]).reset_index()
df_day

"""
Plot bar chart for average PM2.5 for each day
"""
plot_bar_chart(
    df_day,
    x="day",
    y="mean",
    title="Average PM2.5 for each day",
    xlabel="Day",
    ylabel="Average PM2.5",
)

"""
Get average PM2.5 for each hour
"""
df_hour = df.groupby("hour")["PM2.5"].agg(["mean", "std"]).reset_index()
df_hour

"""
Plot bar chart for average PM2.5 for each hour
"""
plot_bar_chart(
    df_hour,
    x="hour",
    y="mean",
    title="Average PM2.5 for each hour",
    xlabel="Hour",
    ylabel="Average PM2.5",
)

"""
Get average PM2.5 for each weekday
"""
df_weekday = df.groupby("weekday")["PM2.5"].agg(["mean", "std"]).reset_index()
# convert weekday number to weekday name
df_weekday["weekday"] = df_weekday["weekday"].replace(
    {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
)

df_weekday

"""
Plot bar chart for average PM2.5 for each weekday
"""
plot_bar_chart(
    df_weekday,
    x="weekday",
    y="mean",
    title="Average PM2.5 for each weekday",
    xlabel="Weekday",
    ylabel="Average PM2.5",
)

"""
Get average PM2.5 for each wind direction
"""
df_wind_direction = df.groupby("wd")["PM2.5"].agg(["mean", "std"]).reset_index()
df_wind_direction

"""
Plot bar chart for average PM2.5 for each wind direction
"""
plot_bar_chart(
    df_wind_direction,
    x="wd",
    y="mean",
    title="Average PM2.5 for each wind direction",
    xlabel="Wind Direction",
    ylabel="Average PM2.5",
)

"""
## Conclusion
"""

"""
### Pertanyaan 1:
Bagaimana Air Quality dari masing-masing area?
"""

"""
Dari hasil analisis, didapatkan bahwa:
- Air Quality terbaik ada di area Dingling
- Air Quality terburuk ada di area Dongsi
"""

"""
### Pertanyaan 2:
Bagaimana Tren Air Quality dari masing-masing area dari waktu ke waktu?
"""

"""
Dari hasil analisis, didapatkan bahwa:
- Air Quality terbaik ada di kisaran pukul 7 dan 16 di setiap harinya
- Air Quality terbaik ada di kisaran tanggal 12 di setiap bulannya 
- Air Quality terbaik ada di kisaran hari Senin di setiap minggunya

- Air Quality terburuk ada di kisaran pukul 21 - 24/00 di setiap harinya
- Air Quality terburuk ada di kisaran tanggal 15-16 di setiap bulannya 
- Air Quality terburuk ada di kisaran hari Saturday di setiap minggunya
"""