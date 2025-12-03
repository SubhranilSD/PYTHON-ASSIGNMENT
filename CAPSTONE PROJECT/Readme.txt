# Capstone Project: Campus Energy Consumption Analysis

## Overview
This Capstone project is an end-to-end data analysis pipeline designed to monitor and analyze energy consumption across different campus buildings. It demonstrates object-oriented programming, data ingestion, aggregation, visualization, and automated reporting.

## Features
- **Object-Oriented Design**: Uses `Building`, `MeterReading`, and `BuildingManager` classes to model the real-world system.
- **Data Ingestion**: Automatically loads CSV data from a `data/` directory. If no data exists, it generates sample data for testing.
- **Data Cleaning**: Handles missing values, normalizes column names, and validates data types.
- **Aggregation**: Calculates daily totals, weekly averages, and building-wise summaries.
- **Visualization**: Generates a comprehensive dashboard (`dashboard.png`) showing:
    - Daily consumption trends.
    - Average weekly consumption by building.
    - Peak-hour consumption scatter plot.
- **Reporting**: Generates an executive summary text file (`summary.txt`) and exports cleaned data.

## Project Structure
- `lab5.py`: The main script containing the entire pipeline.
- `data/`: Directory for input CSV files (one per building).
- `output/`: Directory where results (plots, reports, cleaned data) are saved.

## How to Run
1.  Ensure dependencies are installed:
    ```bash
    pip install pandas numpy matplotlib
    ```
2.  Run the main script:
    ```bash
    python lab5.py
    ```
3.  The script will:
    - Check for data in `data/` (generating samples if empty).
    - Process the data.
    - Save the dashboard and report to the `output/` directory.

