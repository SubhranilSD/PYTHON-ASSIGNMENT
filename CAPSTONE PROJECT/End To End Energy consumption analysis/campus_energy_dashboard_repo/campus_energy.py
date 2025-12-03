"""simplified_campus_energy.py

A short, easy-to-read script for the Campus Energy Dashboard assignment.

What it does (simple):
1. Loads CSV files from ./data/ (or generates sample data if none found).
2. Cleans the data and merges into one table.
3. Calculates building-wise totals and saves results.
4. Creates one simple plot and saves it.
5. Writes a short text summary.

Run:
    pip install -r requirements.txt
    python simplified_campus_energy.py

Outputs appear in the output/ folder.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

DATA_DIR = Path("./data")
OUTPUT_DIR = Path("./output")
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_sample_data(data_dir: Path):
    """Create small sample CSVs so the script runs out-of-the-box."""
    data_dir.mkdir(parents=True, exist_ok=True)
    times = pd.date_range(end=pd.Timestamp.now().floor('H'), periods=48, freq='H')
    buildings = ['Library', 'Engineering', 'Admin']
    for b in buildings:
        values = (10 + 5 * np.sin((times.hour/24)*2*np.pi)) + np.random.randn(len(times))
        df = pd.DataFrame({'timestamp': times, 'kwh': np.clip(values, 0.1, None)})
        df.to_csv(data_dir / f"{b}.csv", index=False)

def load_and_clean(data_dir: Path) -> pd.DataFrame:
    """Load all CSVs, ensure columns are correct, and concatenate them."""
    csv_files = sorted(data_dir.glob('*.csv'))
    if not csv_files:
        generate_sample_data(data_dir)
        csv_files = sorted(data_dir.glob('*.csv'))

    df_list = []
    for f in csv_files:
        df = pd.read_csv(f, parse_dates=['timestamp'], infer_datetime_format=True)
        # try to guess 'kwh' and 'timestamp' if names differ - simple approach
        if 'kwh' not in df.columns:
            possible_kwh = [c for c in df.columns if 'energy' in c.lower() or 'consum' in c.lower()]
            if possible_kwh:
                df = df.rename(columns={possible_kwh[0]: 'kwh'})
        if 'timestamp' not in df.columns:
            possible_time = [c for c in df.columns if 'time' in c.lower() or 'date' in c.lower()]
            if possible_time:
                df = df.rename(columns={possible_time[0]: 'timestamp'})
        # drop bad rows
        df = df.dropna(subset=['timestamp', 'kwh'])
        df['building'] = f.stem  # filename as building name
        df['kwh'] = pd.to_numeric(df['kwh'], errors='coerce')
        df = df.dropna(subset=['kwh'])
        df_list.append(df[['timestamp', 'kwh', 'building']])
    combined = pd.concat(df_list, ignore_index=True)
    combined = combined.sort_values(['building', 'timestamp']).reset_index(drop=True)
    return combined

def summarize_and_save(df: pd.DataFrame, out_dir: Path):
    """Create simple aggregations and save CSV + text summary."""
    total_by_building = df.groupby('building')['kwh'].sum().reset_index().rename(columns={'kwh': 'total_kwh'})
    total_by_building.to_csv(out_dir / 'building_totals.csv', index=False)

    summary_lines = []
    summary_lines.append(f"Report generated: {datetime.now().isoformat()}")
    summary_lines.append(f"Total campus kWh: {df['kwh'].sum():.2f}")
    for _, r in total_by_building.sort_values('total_kwh', ascending=False).iterrows():
        summary_lines.append(f" - {r['building']}: {r['total_kwh']:.2f} kWh")

    (out_dir / 'summary.txt').write_text('\n'.join(summary_lines))

def simple_plot(df: pd.DataFrame, out_dir: Path):
    """Create one plot showing total per building as a bar chart."""
    totals = df.groupby('building')['kwh'].sum()
    ax = totals.plot(kind='bar', title='Total kWh by Building', ylabel='kWh')
    fig = ax.get_figure()
    fig.savefig(out_dir / 'building_totals.png', dpi=150)
    fig.clf()

def main():
    data_dir = DATA_DIR
    out_dir = OUTPUT_DIR
    df = load_and_clean(data_dir)
    df.to_csv(out_dir / 'cleaned.csv', index=False)
    summarize_and_save(df, out_dir)
    simple_plot(df, out_dir)
    print('Done. Check the output/ folder for results.')

if __name__ == '__main__':
    main()
