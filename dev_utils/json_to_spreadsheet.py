import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load JSON data
input_file = './dev_utils/exclusion_test_data.json'
output_file = 'schedule_view.xlsx'

with open(input_file, 'r') as f:
    data = json.load(f)

# Process Doctors
doctors_df = pd.DataFrame(data['doctors'])

# Process Schedules
schedules_df = pd.DataFrame(data['schedules'])

# Process Shifts
shifts_df = pd.DataFrame(data['shifts'])

# Process Admin Users
admin_users_df = pd.DataFrame(data['admin_users'])

# Save data to Excel with separate sheets
with pd.ExcelWriter(output_file) as writer:
    doctors_df.to_excel(writer, sheet_name='Doctors', index=False)
    schedules_df.to_excel(writer, sheet_name='Schedules', index=False)
    shifts_df.to_excel(writer, sheet_name='Shifts', index=False)
    admin_users_df.to_excel(writer, sheet_name='Admin_Users', index=False)

print(f"Spreadsheet saved as {output_file}")

# Visualization - Calendar View
calendar = pd.DataFrame(index=doctors_df['name'], columns=[f'2024-09-{str(i).zfill(2)}' for i in range(1, 31)])

# Fill calendar with shift assignments and days off
for _, doctor in doctors_df.iterrows():
    days_off = doctor['days_off'].split(',')
    for day in days_off:
        if day in calendar.columns:
            calendar.loc[doctor['name'], day] = 'OFF'

for _, shift in shifts_df.iterrows():
    doctor_name = doctors_df.loc[doctors_df['id'] == shift['doctor_id'], 'name'].values[0]
    calendar.loc[doctor_name, shift['date']] = 'X'

calendar = calendar.fillna('')

# Plot calendar view
fig, ax = plt.subplots(figsize=(15, 8))
cax = ax.matshow(np.zeros(calendar.shape), cmap='Greys', alpha=0)

ax.set_xticks(np.arange(len(calendar.columns)))
ax.set_yticks(np.arange(len(calendar.index)))
ax.set_xticklabels(calendar.columns, rotation=90)
ax.set_yticklabels(calendar.index)

for i in range(len(calendar.index)):
    for j in range(len(calendar.columns)):
        text = calendar.iloc[i, j]
        ax.text(j, i, text, ha='center', va='center', color='black')

plt.xlabel('Date')
plt.ylabel('Doctor')
plt.title('Shift Calendar for September 2024')
plt.tight_layout()
plt.savefig('calendar_plot.png')
plt.show()
