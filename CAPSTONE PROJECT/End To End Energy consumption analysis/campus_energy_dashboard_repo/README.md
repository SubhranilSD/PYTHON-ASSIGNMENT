# Campus Energy Dashboard 

This repository contains a simplified, easy-to-understand solution for the Campus Energy Dashboard assignment.

## Files
- `simplified_campus_energy.py` - The main, human-friendly script.
- `requirements.txt` - Python packages required.
- `data/` - (not included) Put your CSV meter files here. If empty, the script will generate sample data.
- `output/` - The script writes `cleaned.csv`, `building_totals.csv`, `summary.txt`, and `building_totals.png` here.
- `Lab Assignment` (original brief): `/mnt/data/Lab Assignment 5 (Capstone).docx`  <!-- local path to your uploaded assignment -->

## How to run
1. Create a Python environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows use `venv\Scripts\activate`
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run:
   ```bash
   python simplified_campus_energy.py
   ```
4. Inspect the `output/` folder.

## Notes
- The script is intentionally small and annotated so you can read and understand every step.
- If you have meter CSVs, place them inside `data/` before running. The script expects each CSV to have at least `timestamp` and `kwh` columns; if names differ it will attempt simple guesses.
