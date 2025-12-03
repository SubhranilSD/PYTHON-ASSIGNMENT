# Python Lab 4: Pandas Weather Analysis

## Overview
This project involves analyzing a real-world weather dataset using Python's data science stack: Pandas, NumPy, and Matplotlib. The goal is to clean raw data, perform statistical analysis, and visualize weather trends.

## Features
- **Data Loading**: Loads weather data from a CSV file.
- **Data Cleaning**: Handles missing values and converts date columns to the correct format.
- **Statistical Analysis**: Calculates daily, monthly, and seasonal statistics (mean temperature, max temperature, total rainfall, etc.).
- **Visualization**: Generates various plots to visualize trends:
    - Daily Temperature Trend (Line Chart)
    - Monthly Rainfall (Bar Chart)
    - Humidity vs. Temperature (Scatter Plot)
    - Combined Dashboard
- **Export**: Saves the cleaned dataset and generated plots.

## Files
- `lab4.py`: The main analysis script.
- `weather_dataset.csv`: The input raw dataset.
- `cleaned_weather_data.csv`: The processed output dataset.
- `*.png`: Generated plots (e.g., `daily_temp_trend.png`, `monthly_rainfall.png`).

## How to Run
1.  Ensure you have the required libraries installed:
    ```bash
    pip install pandas numpy matplotlib
    ```
2.  Run the script:
    ```bash
    python lab4.py
    ```
3.  Check the output directory for the generated PNG plots and the cleaned CSV file.
