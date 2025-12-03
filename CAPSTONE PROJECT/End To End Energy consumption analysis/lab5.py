import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

DATA_DIR = Path("./data")
OUTPUT_DIR = Path("./output")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Task 3: Object-Oriented Modeling ---

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh

class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, timestamp, kwh):
        self.meter_readings.append(MeterReading(timestamp, kwh))

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)
    
    def get_dataframe(self):
        data = [{'timestamp': r.timestamp, 'kwh': r.kwh, 'building': self.name} for r in self.meter_readings]
        return pd.DataFrame(data)

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def get_or_create_building(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def add_reading_to_building(self, building_name, timestamp, kwh):
        building = self.get_or_create_building(building_name)
        building.add_reading(timestamp, kwh)
    
    def get_all_readings_df(self):
        dfs = [b.get_dataframe() for b in self.buildings.values() if b.meter_readings]
        if not dfs:
            return pd.DataFrame(columns=['timestamp', 'kwh', 'building'])
        combined = pd.concat(dfs, ignore_index=True)
        combined['timestamp'] = pd.to_datetime(combined['timestamp'])
        return combined.sort_values(['building', 'timestamp']).reset_index(drop=True)

# --- Task 1: Data Ingestion and Validation ---

def generate_sample_data(data_dir: Path):
    """Create small sample CSVs so the script runs out-of-the-box."""
    data_dir.mkdir(parents=True, exist_ok=True)
    times = pd.date_range(end=pd.Timestamp.now().floor('H'), periods=168, freq='H') # 1 week of data
    buildings = ['Library', 'Engineering', 'Admin']
    for b in buildings:
        # Create some realistic-ish patterns
        base_load = 10
        daily_pattern = 5 * np.sin((times.hour/24)*2*np.pi - np.pi/2) # Peak at noon
        random_noise = np.random.randn(len(times)) * 2
        values = base_load + daily_pattern + random_noise
        
        df = pd.DataFrame({'timestamp': times, 'kwh': np.clip(values, 0.1, None)})
        df.to_csv(data_dir / f"{b}.csv", index=False)
    print("Sample data generated.")

def load_data(data_dir: Path, manager: BuildingManager):
    csv_files = sorted(data_dir.glob('*.csv'))
    if not csv_files:
        print("No CSV files found. Generating sample data...")
        generate_sample_data(data_dir)
        csv_files = sorted(data_dir.glob('*.csv'))

    for f in csv_files:
        try:
            # Handle bad lines and missing values
            df = pd.read_csv(f, on_bad_lines='skip') 
            
            # Normalize column names
            df.columns = [c.lower() for c in df.columns]
            
            # Identify timestamp and kwh columns
            timestamp_col = next((c for c in df.columns if 'time' in c or 'date' in c), None)
            kwh_col = next((c for c in df.columns if 'kwh' in c or 'energy' in c or 'consum' in c), None)
            
            if not timestamp_col or not kwh_col:
                print(f"Skipping {f.name}: Could not identify timestamp or kwh columns.")
                continue

            df = df.dropna(subset=[timestamp_col, kwh_col])
            
            building_name = f.stem
            
            for _, row in df.iterrows():
                try:
                    ts = pd.to_datetime(row[timestamp_col])
                    kwh = float(row[kwh_col])
                    manager.add_reading_to_building(building_name, ts, kwh)
                except ValueError:
                    continue # Skip rows with invalid data types

        except Exception as e:
            print(f"Error reading {f.name}: {e}")

# --- Task 2: Core Aggregation Logic ---

def calculate_daily_totals(df):
    return df.set_index('timestamp').groupby('building').resample('D')['kwh'].sum().reset_index()

def calculate_weekly_aggregates(df):
    return df.set_index('timestamp').groupby('building').resample('W')['kwh'].mean().reset_index()

def building_wise_summary(df):
    return df.groupby('building')['kwh'].agg(['mean', 'min', 'max', 'sum']).reset_index()

# --- Task 4: Visual Output with Matplotlib ---

def generate_dashboard(df, daily_totals, weekly_avg, out_dir: Path):
    fig, axes = plt.subplots(3, 1, figsize=(12, 18))
    fig.suptitle('Campus Energy Consumption Dashboard', fontsize=16)

    # 1. Trend Line – daily consumption over time for all buildings
    for building in df['building'].unique():
        subset = daily_totals[daily_totals['building'] == building]
        axes[0].plot(subset['timestamp'], subset['kwh'], label=building, marker='o')
    axes[0].set_title('Daily Energy Consumption Trend')
    axes[0].set_ylabel('Total kWh')
    axes[0].set_xlabel('Date')
    axes[0].legend()
    axes[0].grid(True)

    # 2. Bar Chart – compare average weekly usage across buildings
    # We'll take the mean of the weekly means for a simple bar chart per building
    avg_weekly = weekly_avg.groupby('building')['kwh'].mean()
    avg_weekly.plot(kind='bar', ax=axes[1], color='skyblue', edgecolor='black')
    axes[1].set_title('Average Weekly Consumption by Building')
    axes[1].set_ylabel('Average kWh')
    axes[1].set_xlabel('Building')
    axes[1].grid(axis='y')

    # 3. Scatter Plot – peak-hour consumption vs. time/building
    # Let's plot raw readings to show distribution/peaks
    for building in df['building'].unique():
        subset = df[df['building'] == building]
        axes[2].scatter(subset['timestamp'], subset['kwh'], label=building, alpha=0.5, s=10)
    axes[2].set_title('Hourly Consumption Scatter Plot (Peak Analysis)')
    axes[2].set_ylabel('kWh')
    axes[2].set_xlabel('Time')
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(out_dir / 'dashboard.png')
    plt.close()

# --- Task 5: Persistence and Executive Summary ---

def generate_report(df, building_summary, out_dir: Path):
    total_consumption = df['kwh'].sum()
    highest_consumer = building_summary.loc[building_summary['sum'].idxmax()]
    
    # Find peak load time (global)
    peak_row = df.loc[df['kwh'].idxmax()]
    
    summary_text = f"""
EXECUTIVE SUMMARY REPORT
========================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. Total Campus Consumption: {total_consumption:.2f} kWh

2. Highest Consuming Building:
   - Name: {highest_consumer['building']}
   - Total Usage: {highest_consumer['sum']:.2f} kWh
   - Average Usage: {highest_consumer['mean']:.2f} kWh

3. Peak Load Event:
   - Time: {peak_row['timestamp']}
   - Building: {peak_row['building']}
   - Consumption: {peak_row['kwh']:.2f} kWh

4. Building Summary Data:
{building_summary.to_string(index=False)}
"""
    
    print(summary_text)
    (out_dir / 'summary.txt').write_text(summary_text)
    
    df.to_csv(out_dir / 'cleaned_energy_data.csv', index=False)
    building_summary.to_csv(out_dir / 'building_summary.csv', index=False)

def main():
    print("Starting Energy Analysis Pipeline...")
    
    manager = BuildingManager()
    load_data(DATA_DIR, manager)
    
    df_combined = manager.get_all_readings_df()
    
    if df_combined.empty:
        print("No data available to process.")
        return

    # Aggregations
    daily_totals = calculate_daily_totals(df_combined)
    weekly_avg = calculate_weekly_aggregates(df_combined)
    summary_stats = building_wise_summary(df_combined)
    
    # Visualization
    generate_dashboard(df_combined, daily_totals, weekly_avg, OUTPUT_DIR)
    
    # Reporting
    generate_report(df_combined, summary_stats, OUTPUT_DIR)
    
    print("Analysis complete. Check 'output' directory.")

if __name__ == '__main__':
    main()
