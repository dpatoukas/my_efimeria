import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Validate file existence
if not os.path.exists('days_off.json'):
    raise FileNotFoundError("Missing file: 'days_off.json'. Ensure it is in the same directory as this script.")

if not os.path.exists('shifts.json'):
    raise FileNotFoundError("Missing file: 'shifts.json'. Ensure it is in the same directory as this script.")

# Load the data
with open('days_off.json', 'r') as f:
    days_off = json.load(f)

with open('shifts.json', 'r') as f:
    shifts = json.load(f)

# Ensure consistency in doctor IDs by converting them to strings
days_off = {str(k): v for k, v in days_off.items()}
for shift in shifts:
    shift['doctor_id'] = str(shift['doctor_id'])

# Extract unique dates
all_dates = sorted(set([shift['date'] for shift in shifts] + [date for d in days_off.values() for date in d['day_off_requested']] + [date for d in days_off.values() for date in d['day_available']]))

# Initialize DataFrame
doctor_ids = sorted(set(days_off.keys()).union(set(shift['doctor_id'] for shift in shifts)))
df = pd.DataFrame(index=doctor_ids, columns=all_dates, data='')

# Populate days off and available days
for doctor_id, data in days_off.items():
    for day in data['day_off_requested']:
        if day in df.columns:
            df.loc[doctor_id, day] = 'OFF'
    for day in data['day_available']:
        if day in df.columns:
            df.loc[doctor_id, day] = 'AVAILABLE'

# Populate shifts and check for conflicts
for shift in shifts:
    doctor_id = shift['doctor_id']
    date = shift['date']
    if date in df.columns:
        if df.loc[doctor_id, date] == 'OFF':
            df.loc[doctor_id, date] = 'CONFLICT'
        else:
            df.loc[doctor_id, date] = 'SHIFT'

# Fill empty cells with white (no activity)
df = df.fillna('')

# Highlight conflicts in red
cmap = ListedColormap(['white', 'green', 'blue', 'orange', 'red'])
colors = {'': 0, 'SHIFT': 1, 'AVAILABLE': 2, 'OFF': 3, 'CONFLICT': 4}

visual = df.applymap(lambda x: colors[x])

plt.figure(figsize=(20, 10))
plt.imshow(visual, cmap=cmap, aspect='auto')
plt.colorbar(ticks=[0, 1, 2, 3, 4], label='Status')
plt.clim(-0.5, 4.5)
plt.xticks(range(len(df.columns)), df.columns, rotation=90)
plt.yticks(range(len(df.index)), df.index)
plt.title('Doctor Shifts and Days Off Visualization')
plt.xlabel('Dates')
plt.ylabel('Doctor IDs')

# Legend for colors
plt.figtext(0.5, -0.1, "Legend: White - No Activity, Green - Shift, Blue - Available, Orange - Day Off, Red - Conflict", wrap=True, horizontalalignment='center', fontsize=12)

plt.show()
