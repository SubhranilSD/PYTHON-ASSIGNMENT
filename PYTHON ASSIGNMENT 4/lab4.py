import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# TASK 1: LOAD & INSPECT DATA
# ---------------------------------------------------------

# Load real dataset (you should place your CSV in the same folder)
df = pd.read_csv('weather_dataset.csv')

print("\n--- HEAD ---")
print(df.head())

print("\n--- INFO ---")
print(df.info())

print("\n--- DESCRIBE ---")
print(df.describe())


# ---------------------------------------------------------
# TASK 2: DATA CLEANING & PROCESSING
# ---------------------------------------------------------

# Handle missing values (drop all NaNs)
df = df.dropna()

# Convert date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

# Filter relevant columns
weather = df[['Date', 'Temp', 'Humidity', 'Rainfall']]
print("\n--- CLEANED DATA ---")
print(weather.head())


# ---------------------------------------------------------
# TASK 3: STATISTICAL ANALYSIS (USING NUMPY)
# ---------------------------------------------------------

# Daily statistics
mean_temp = np.mean(weather['Temp'])
max_temp = np.max(weather['Temp'])
min_humidity = np.min(weather['Humidity'])
std_rainfall = np.std(weather['Rainfall'])

print("\n--- DAILY STATISTICS ---")
print("Mean Temp:", mean_temp)
print("Max Temp:", max_temp)
print("Min Humidity:", min_humidity)
print("Std Rainfall:", std_rainfall)

# Monthly statistics
weather['Month'] = weather['Date'].dt.month
monthly_mean_temp = weather.groupby('Month')['Temp'].mean()
monthly_total_rain = weather.groupby('Month')['Rainfall'].sum()

# Yearly statistics (if multiple years present)
weather['Year'] = weather['Date'].dt.year
yearly_max_temp = weather.groupby('Year')['Temp'].max()


# ---------------------------------------------------------
# TASK 4: VISUALIZATION
# ---------------------------------------------------------

# A. Line chart for daily temperature trend
plt.figure(figsize=(10,4))
plt.plot(weather['Date'], weather['Temp'])
plt.title('Daily Temperature Trend')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.savefig('daily_temp_trend.png')
plt.show()

# B. Bar chart for monthly rainfall totals
plt.figure(figsize=(8,4))
monthly_total_rain.plot(kind='bar')
plt.title('Monthly Rainfall')
plt.xlabel('Month')
plt.ylabel('Rainfall (mm)')
plt.savefig('monthly_rainfall.png')
plt.show()

# C. Scatter plot (Humidity vs Temperature)
plt.figure(figsize=(6,4))
plt.scatter(weather['Temp'], weather['Humidity'])
plt.title('Humidity vs Temperature')
plt.xlabel('Temperature (°C)')
plt.ylabel('Humidity (%)')
plt.savefig('humidity_vs_temp.png')
plt.show()

# D. Combined plot in a single figure (Line + Scatter)
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.plot(weather['Date'], weather['Temp'])
plt.title('Daily Temperature Trend')

plt.subplot(1,2,2)
plt.scatter(weather['Temp'], weather['Humidity'])
plt.title('Humidity vs Temperature')

plt.tight_layout()
plt.savefig('combined_plot.png')
plt.show()


# ---------------------------------------------------------
# TASK 5: GROUPING & AGGREGATION
# ---------------------------------------------------------

# Group by season
def get_season(month):
    if month in [12,1,2]:
        return "Winter"
    elif month in [3,4,5]:
        return "Summer"
    elif month in [6,7,8]:
        return "Monsoon"
    else:
        return "Post-Monsoon"

weather['Season'] = weather['Month'].apply(get_season)

seasonal_stats = weather.groupby('Season')[['Temp','Rainfall','Humidity']].mean()

print("\n SEASONAL STATISTICS ")
print(seasonal_stats)

#EXPORT DATA

weather.to_csv("cleaned_weather_data.csv", index=False)
print("\nCleaned data exported as cleaned_weather_data.csv")
print("All plots saved as PNG images.")
