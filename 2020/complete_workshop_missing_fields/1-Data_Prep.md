---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.3.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

## Complete Workshop Missing Fields

A short description of the project.

### Data Sources
- Workshops with missing fields: https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M0000077dvzUAA/view
- file2:  Link to SF Report (As Needed)
- file3:  Link to SF Report (As Needed)

### Changes
- 04-24-2020 : Started project

```python
# ALWAYS RUN
# General Setup 

%load_ext dotenv
%dotenv

from salesforce_reporting import Connection, ReportParser
import pandas as pd
from pathlib import Path
from datetime import datetime
import helpers
import os
import numpy as np
from reportforce import Reportforce
import datetime


SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Reportforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)
```

### File Locations

```python
# ALWAYS RUN
today = datetime.today()


in_file1 = Path.cwd() / "data" / "raw" / "workshops.csv"
summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"


in_file2 = Path.cwd() / "data" / "raw" / "sf_output_file2.csv"
summary_file2 = Path.cwd() / "data" / "processed" / "processed_data_file2.pkl"


in_file3 = Path.cwd() / "data" / "raw" / "sf_output_file3.csv"
summary_file3 = Path.cwd() / "data" / "processed" / "processed_data_file3.pkl"


in_file4 = Path.cwd() / "data" / "raw" / "sf_output_file4.csv"
summary_file4 = Path.cwd() / "data" / "processed" / "processed_data_file4.pkl"
```

### Load Report From Salesforce

```python
# # Run if downloading report from salesforce
# # File 1 
# report_id_file1 = "00O1M0000077dvzUAA"
# file_1_id_column = 'Workshop: ID' # adjust as needed
# sf_df = sf.get_report(report_id_file1, id_column=file_1_id_column)



# # File 2 (As needed)
# # report_id_file2 = "SF_REPORT_ID"
# # file_2_id_column = '18 Digit ID' # adjust as needed
# # sf_df_file2 =  sf.get_report(report_id_file2, id_column=file_2_id_column)

# # File 3 (As needed)
# # report_id_file3 = "SF_REPORT_ID"
# # file_3_id_column = '18 Digit ID' # adjust as needed
# # sf_df_file3 =  sf.get_report(report_id_file3, id_column=file_3_id_column)

```

#### Save report as CSV

```python
# Only run if ran above cell
# File 1
# sf_df.to_csv(in_file1, index=False)


# File 2 and 3 (As needed)
# sf_df_file2.to_csv(in_file2, index=False)
# sf_df_file3.to_csv(in_file3, index=False)

```

### Load DF from saved CSV
* Start here if CSV already exist 

```python
# ALWAYS RUN 
# Data Frame for File 1 - if using more than one file, rename df to df_file1
df = pd.read_csv(in_file1)


# Data Frames for File 1 and 2 (As needed)

# df_file2 = pd.read_csv(in_file2)
# df_file3 = pd.read_csv(in_file3)
```

### Data Manipulation

```python
df.columns
```

```python
# Convert missing schedule blocks to block F 
df.loc[pd.isna(df['Schedule Block']),['Schedule Block']] = "F"
```

```python
# Converting all missing weekly / biweekly to weekly
df.loc[pd.isna(df['Weekly / Bi-Weekly']),['Weekly / Bi-Weekly']] = "Weekly"
```

```python
df.loc[pd.isna(df['Workshop Capacity']),['Workshop Capacity']] = 0
```

```python
# Converting missing start / end date to one time date 

df.loc[pd.isna(df['Start Date']),['Start Date']] = df.loc[pd.isna(df['Start Date']),['One Time Date']].values
```

```python
df.loc[pd.isna(df['End Date']),['End Date']] = df.loc[pd.isna(df['End Date']),['One Time Date']].values
```

```python
df['Start Date'] = pd.to_datetime(df['Start Date'])
```

```python
df['Start Date'][0]
```

```python
def determine_day_of_week(date):
    return date.strftime('%A')

# df.loc[pd.isna(df['Day(s) of the Week']),['Day(s) of the Week']] = df.loc[pd.isna(df['Day(s) of the Week']),['Start Date']].values.strftime('%A')

# df.loc[pd.isna(df['Day(s) of the Week']),['Start Date']]
```

```python
df.loc[pd.isna(df['Day(s) of the Week']), ['Day(s) of the Week']] = df.loc[pd.isna(df['Day(s) of the Week']),].apply(lambda x: determine_day_of_week(x['Start Date']), axis=1)
```

```python
dosage_types = {'Student Life': ['SL', 'Student Life'],
               "Math": ['ACT', 'SAT', 'Math', 'Geo', 'Geometry', 'GEO', 'MATH'],
               'Tutoring': ['TUT', 'Tutoring'],
               'College Completion': ['College', 'CC'],
               'NSO': ['NSO', 'New Student Orientation']
               }
```

```python
df['Workshop Display Name'].str.contains('|'.join(['SL', 'Student Life'])).value_counts()
```

```python
import re
```

```python
st = df['Workshop Display Name'][0]
```

```python
st
```

```python
search = ['workshop', "dfa"]
```

```python
bool(re.search(r"|".join(search),st))
```

```python
def check_dosage_type_in_display_name(display_name, dosage_to_check):
    check_strings = dosage_types[dosage_to_check]
#     display_name = np.Se
    
    if bool(re.search(r"|".join(check_strings),display_name)):
        return dosage_to_check
    else:
        return np.nan
```

```python
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']] 
```

```python
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']]  = df.loc[pd.isna(df['Dosage Types']), ].apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "Student Life"), axis=1)
```

```python
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']] = df.loc[pd.isna(df['Dosage Types']), ].apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "Math"), axis=1)
```

```python
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']] = df.loc[pd.isna(df['Dosage Types']), ].apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "Tutoring"), axis=1)
```

```python
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']] = df.loc[pd.isna(df['Dosage Types']), ].apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "College Completion"), axis=1)
```

```python
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']] = df.loc[pd.isna(df['Dosage Types']), ].apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "NSO"), axis=1)
```

```python
df['Dosage Types'].value_counts()
```

```python
df['Dosage Types'].value_counts()
```

```python
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']] = "Other"
```

```python
departments = {'Academic Affairs': ['Math', 'Math Blast', 'Test Prep','Tutoring'],
              'College Completion': ['College Completion', 'Senior Writing Institute (SWI)'],
              'Other': ['Other'],
              'Student Life': ['Student Life']}
```

```python
def determine_department_from_dosage(dosage):
    for department, dosage_types in departments.items():
        if dosage in dosage_types:
            return department
    
    return np.nan
        
```

```python
df.loc[pd.isna(df['Department']), ['Department']] = df.loc[pd.isna(df['Department']), ].apply(
    lambda x: determine_department_from_dosage(x['Dosage Types']), axis=1)
```

```python
df.loc[pd.isna(df['Department']), ['Department']] = "Other"
```

```python
df['Attendance Taker'].value_counts()
```

```python
df['Primary Staff'].value_counts()
```

```python
attendance_takers = {
    "College Track Oakland":"00546000001cdSi",
    "College Track New Orleans": "00546000001b4Tt",
    "College Track East Palo Alto": "00546000001cdSY",
    "College Track Boyle Heights": "00546000001cdS9",
    "College Track Sacramento": "00546000001cdSs",
    "College Track Aurora":"00546000001cdSd",
    "College Track San Francisco": "00546000001cdSx",
    "College Track Watts":"00546000001cdT2",
    "College Track Denver": "00546000001cdST",
    "College Track at The Durant Center":"00546000001cd3r",
    "College Track Arlen": "0051M000009602u"
}
```

```python
def determine_staff(site, attendance_takers):
#     print(site)
#     print(attendance_takers[site])
    
    return attendance_takers[site]
```

```python
df = df.dropna(subset=['Site'])
```

```python
df.loc[pd.isna(df['Primary Staff']),].iloc[40]
```

```python
df.loc[pd.isna(df['Primary Staff']), ['Primary Staff']] = df.loc[pd.isna(
    df['Primary Staff']), ].apply(lambda x: determine_staff(x['Site'], attendance_takers), axis=1)
```

```python
df.loc[pd.isna(df['Attendance Taker']), ['Attendance Taker']] = df.loc[pd.isna(
    df['Attendance Taker']), ].apply(lambda x: determine_staff(x['Site'], attendance_takers), axis=1)
```

```python
df['Start Time']
```

```python
df.loc[pd.isna(df['Start Time']), ['Start Time']] = "9:00 AM"
```

```python
df.loc[pd.isna(df['End Time']), ['End Time']] = "10:00 AM"
```

```python
df = df.drop('test', axis=1)
```

```python
from gspread_pandas import Spread, Client

```

```python
# start_cell = "E" + len

google_sheet = Spread('1DFPUarz1j2-StHWfjnZ_P6uWmBtpoT0TqJw99-i3HGE')


google_sheet.df_to_sheet(df, index=False, sheet='Sheet1', start='A1', replace=False)
```

```python
# File 1
df = helpers.shorten_site_names(df)
df = helpers.clean_column_names(df)

# File 2
# df_file2 = helpers.shorten_site_names(df_file2)
# df_file2 = helpers.clean_column_names(df_file2)
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
# Save File 1 Data Frame (Or master df)
df.to_pickle(summary_file)
```
