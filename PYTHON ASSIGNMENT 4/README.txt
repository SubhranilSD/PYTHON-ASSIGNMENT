Welcome! This little project was all about exploring real weather data using Python. Nothing too fancy — just some basic cleaning, number-crunching, and plotting to understand how the weather behaved over a short period of time.

What Was Done

First, a weather CSV file was downloaded and loaded into a Pandas DataFrame. The data was checked to see what it looked like — things like temperature, humidity, and rainfall.

Cleaning the Data

A few simple cleanup steps were done:

Missing values were removed

The Date column was turned into proper datetime format

Only the useful columns (Date, Temp, Humidity, Rainfall) were kept

Just enough to make the data easy to work with.

Analysis

Using NumPy, some quick stats were calculated — average temperature, highest temp, lowest humidity, rainfall variation, and monthly totals. Then the data was grouped by month and season to spot bigger patterns.

Visuals

A few plots were created to make the trends easier to understand:

Daily temperature line graph

Monthly rainfall bar chart

Humidity vs temperature scatter plot

A combined figure with two plots

All these graphs were saved as PNG images.

Output

Finally, the cleaned dataset was saved as cleaned_weather_data.csv so it can be reused or analysed again later.



Overall, this project was a simple walkthrough of data analysis using Pandas, NumPy, and Matplotlib — perfect practice for handling real-world datasets.