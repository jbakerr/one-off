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
from simple_salesforce import Salesforce
from gspread_pandas import Spread, Client




SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Reportforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)

sf_upload = Salesforce(username=SF_USERNAME, password=SF_PASS,
                 security_token=SF_TOKEN)
```

### File Locations

```python
# ALWAYS RUN
# today = datetime.today()


in_file1 = Path.cwd() / "data" / "raw" / "workshops_2.csv"
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
google_sheet = Spread('1DFPUarz1j2-StHWfjnZ_P6uWmBtpoT0TqJw99-i3HGE')

```

#### Missing Schedule Blocks

```python
# Missing Schedule Blocks
missing_schedule_blocks = df.loc[pd.isna(df['Schedule Block']),:]

missing_schedule_blocks.loc[:,'Schedule Block'] = "F"
```

```python
missing_block_data = []

missing_schedule_blocks.apply(lambda x: missing_block_data.append({"Id": x['Workshop: ID'], "Schedule_Block__c": x['Schedule Block']}),axis=1)
```

```python
missing_block_upload_results = sf_upload.bulk.Class__c.update(missing_block_data)

```

```python
missing_schedule_blocks = missing_schedule_blocks.join(pd.DataFrame(missing_block_upload_results))
```

```python
google_sheet.df_to_sheet(missing_schedule_blocks, index=False, sheet="Missing Schedule Blocks", start='A1', replace=False, headers=True)
```

#### Missing Weekly

```python
# Converting all missing weekly / biweekly to weekly
df.loc[pd.isna(df['Weekly / Bi-Weekly']),['Weekly / Bi-Weekly']] = "Weekly"
```

```python
missing_weekly = df.loc[pd.isna(df['Weekly / Bi-Weekly']),:]

missing_weekly.loc[:,"Weekly / Bi-Weekly"] = "Weekly"
```

```python
missing_weekly_data = []

missing_weekly.apply(lambda x: missing_weekly_data.append({"Id": x['Workshop: ID'], "Recurrance__c":1}),axis=1)
```

```python
missing_weekly_upload_results = sf_upload.bulk.Class__c.update(missing_weekly_data)

```

```python
missing_weekly = missing_weekly.join(pd.DataFrame(missing_weekly_upload_results))
```

```python
google_sheet.df_to_sheet(missing_weekly, index=False, sheet="Missing Weekly", start='A1', replace=False, headers=True)
```

#### Workshop Capacity

```python
missing_workshop_capacity = df.loc[pd.isna(df['Workshop Capacity']),:]
```

```python
missing_workshop_capacity.loc[:,'Workshop Capacity'] = 0
```

```python
def update_data(sf_field, google_sheet, df, sheet_title, df_field):
    _data = []
    
    df.apply(lambda x: _data.append({"Id": x["Workshop: ID"], sf_field:x[df_field]}),axis=1)
    
    _upload_results = sf_upload.bulk.Class__c.update(_data)
    df = df.join(pd.DataFrame(_upload_results))
    
    google_sheet.df_to_sheet(df, index=False, sheet=sheet_title, start='A1', replace=True, headers=True)
    
    return df, _upload_results

```

```python
    missing_workshop_capacity_upload, missing_workshop_capacity_upload_results = update_data(
    "Workshop_Capacity__c", google_sheet, missing_workshop_capacity, "Missing Capacity", "Workshop Capacity")
```

```python
_results = pd.DataFrame(missing_workshop_capacity_upload_results)
```

```python
_results.success.value_counts(dropna=False)
```

<!-- #region heading_collapsed=true -->
#### Missing Start Date
<!-- #endregion -->

```python hidden=true
# Converting missing start / end date to one time date 

missing_start_end_date = df.loc[pd.isna(df['Start Date']),:]

# df.loc[pd.isna(df['Start Date']),['Start Date']] = df.loc[pd.isna(df['Start Date']),['One Time Date']].values
```

```python hidden=true
missing_start_end_date.loc[:,'Start Date'] = df.loc[pd.isna(df['Start Date']),['One Time Date']].values
```

```python hidden=true
missing_start_end_date.loc[:,'End Date'] = df.loc[pd.isna(df['Start Date']),['One Time Date']].values
```

```python hidden=true
missing_start_end_date.loc[:,'Start Date'] = pd.to_datetime(
    missing_start_end_date['Start Date']).dt.strftime("%Y-%m-%d")
```

```python hidden=true
missing_start_end_date.loc[:,'End Date'] =pd.to_datetime(
    missing_start_end_date['End Date']).dt.strftime("%Y-%m-%d")
```

```python hidden=true
missing_start_end_date = missing_start_end_date.dropna(subset=['Start Date', "End Date"])
```

```python hidden=true
missing_start_end_date_data = []

missing_start_end_date.apply(lambda x: missing_start_end_date_data.append({"Id":x['Workshop: ID'], "Start_Date__c":x['Start Date'], "End_Date__c":x["End Date"]}),axis=1)
```

```python hidden=true
missing_start_end_date_data.pop()
```

```python hidden=true
missing_start_end_date_data
```

```python hidden=true
missing_date_upload_results = sf_upload.bulk.Class__c.update(missing_start_end_date_data)
```

```python hidden=true
missing_start_end_date= missing_start_end_date.join(pd.DataFrame(missing_date_upload_results))
```

```python hidden=true
missing_start_end_date= missing_start_end_date.join(pd.DataFrame(missing_date_upload_results))
```

```python hidden=true
google_sheet.df_to_sheet(missing_start_end_date, index=False, sheet="Missing Start/End Dates", start='A1', replace=True, headers=True)

```

```python hidden=true
missing_start_end_date
```

```python hidden=true
df_missing_start_date = update_data("Start_Date__c", google_sheet, df, "Missing Start Date", "Start Date")
```

```python hidden=true
df.loc[pd.isna(df['End Date']),['End Date']] = df.loc[pd.isna(df['End Date']),['One Time Date']].values
```

```python hidden=true

```

```python hidden=true
df['Start Date'][0]
```

<!-- #region heading_collapsed=true -->
#### Missing Day of the Week
<!-- #endregion -->

```python hidden=true
df.loc[:,'Start Date'] = pd.to_datetime(df['Start Date'])
```

```python hidden=true
def determine_day_of_week(date):
    return date.strftime('%A')

# df.loc[pd.isna(df['Day(s) of the Week']),['Day(s) of the Week']] = df.loc[pd.isna(df['Day(s) of the Week']),['Start Date']].values.strftime('%A')

# df.loc[pd.isna(df['Day(s) of the Week']),['Start Date']]
```

```python hidden=true
missing_day_of_week = df.loc[pd.isna(df['Day(s) of the Week']), :]
```

```python hidden=true
missing_day_of_week.loc[:,'Day(s) of the Week'] = missing_day_of_week.apply(lambda x: determine_day_of_week(x['Start Date']), axis=1)
```

```python hidden=true
missing_day_of_week = update_data("Recurring_Days__c", google_sheet,missing_day_of_week, "Missing Day of Week", "Day(s) of the Week")
```

<!-- #region heading_collapsed=true -->
#### Missing Dosage Types
<!-- #endregion -->

```python hidden=true
dosage_types = {'Student Life': ['SL', 'Student Life'],
               "Math": ['ACT', 'SAT', 'Math', 'Geo', 'Geometry', 'GEO', 'MATH'],
               'Tutoring': ['TUT', 'Tutoring'],
               'College Completion': ['College', 'CC'],
               'NSO': ['NSO', 'New Student Orientation']
               }
```

```python hidden=true
df['Workshop Display Name'].str.contains('|'.join(['SL', 'Student Life'])).value_counts()
```

```python hidden=true
import re
```

```python hidden=true
st = df['Workshop Display Name'][0]
```

```python hidden=true
st
```

```python hidden=true
search = ['workshop', "dfa"]
```

```python hidden=true
bool(re.search(r"|".join(search),st))
```

```python hidden=true
def check_dosage_type_in_display_name(display_name, dosage_to_check, current_dosage):
    if pd.isna(current_dosage):
        check_strings = dosage_types[dosage_to_check]

    
        if bool(re.search(r"|".join(check_strings),display_name)):
            return dosage_to_check
        else:
            return np.nan
    else:
        return current_dosage
```

```python hidden=true
missing_dosage_type = df.loc[pd.isna(df['Dosage Types']),:] 
```

```python hidden=true

```

```python hidden=true
missing_dosage_type.loc[:,"Dosage Types"]  = missing_dosage_type.apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "Student Life", x['Dosage Types']), axis=1)
```

```python hidden=true
missing_dosage_type.loc[:,"Dosage Types"]  = missing_dosage_type.apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "Math",x['Dosage Types']), axis=1)
```

```python hidden=true
missing_dosage_type.loc[:,"Dosage Types"]  = missing_dosage_type.apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "Tutoring", x['Dosage Types']), axis=1)
```

```python hidden=true
missing_dosage_type.loc[:,"Dosage Types"]  = missing_dosage_type.apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "College Completion", x['Dosage Types']), axis=1)
```

```python hidden=true
missing_dosage_type.loc[:,"Dosage Types"]  = missing_dosage_type.apply(
    lambda x: check_dosage_type_in_display_name(x['Workshop Display Name'], "NSO", x['Dosage Types']), axis=1)
```

```python hidden=true
missing_dosage_type['Dosage Types'].value_counts(dropna=False)
```

```python hidden=true
missing_dosage_type.loc[pd.isna(missing_dosage_type['Dosage Types']), ['Dosage Types']] = "Other"
```

```python hidden=true
missing_dosage_type, missing_dosage_upload_results = update_data("Dosage_Types__c", google_sheet,missing_dosage_type, "Missing Dosage", 'Dosage Types' )
```

```python hidden=true
_results = pd.DataFrame(missing_dosage_upload_results)
```

```python hidden=true
_results.success.value_counts()
```

```python hidden=true
missing_dosage_type['success'].value_counts()
```

```python hidden=true
df.loc[pd.isna(df['Dosage Types']), ['Dosage Types']] = "Other"
```

#### Missing Department

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
missing_department = df.loc[pd.isna(df['Department']),:]
```

```python
missing_department['Department'] = missing_department.apply(
    lambda x: determine_department_from_dosage(x['Dosage Types']), axis=1)
```

```python
missing_department['Department'].value_counts(dropna=False)
```

```python
missing_department.loc[pd.isna(missing_department['Department']), ['Department']] = "Other"
```

```python
missing_department_upload, missing_department_upload_results = update_data(
    "Department__c", google_sheet, missing_department, "Missing Department", "Department")
```

#### Attendance Taker

```python
df['Attendance Taker'].value_counts(dropna=False)
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
missing_attendance_taker = df.loc[pd.isna(df['Attendance Taker']), :]
```

```python
missing_attendance_taker.loc[:, "Attendance Taker"] = missing_attendance_taker.apply(lambda x: determine_staff(x['Site'], attendance_takers), axis=1)
```

```python
missing_attendance_taker_upload, missing_attendance_taker_upload_results = update_data(
    "Attendance_Taker__c", google_sheet, missing_attendance_taker, "Missing Attendance Taker", "Attendance Taker")
```

#### Missing Primary Staff

```python
missing_primary_staff = df.loc[pd.isna(df['Primary Staff']), :]
```

```python
missing_primary_staff['Primary Staff'] = missing_primary_staff.apply(
    lambda x: determine_staff(x['Site'], attendance_takers), axis=1)
```

```python
missing_primary_staff_upload, missing_primary_staff_upload_results = update_data(
    "Primary_Staff__c", google_sheet, missing_primary_staff, "Missing Primary Staff", "Primary Staff")
```

#### Missing Start Time

```python
df['Start Time']
```

```python
missing_start_time = df.loc[pd.isna(df['Start Time']), :]
```

```python
"a3246000000yYdK" in missing_start_time['Workshop: ID']
```

```python
missing_start_time['Start Time'] = "09:00:00.000Z"
```

```python
missing_start_time['End Time'] = "10:00:00.000Z"
```

```python
missing_start_time_data = []
```

```python
missing_start_time.apply(lambda x: missing_start_time_data.append(
    {"Id": x['Workshop: ID'], "Start_Time__c": x['Start Time'], "End_Time__c": x['End Time']}),axis=1)
```

```python
missing_time_upload_results = sf_upload.bulk.Class__c.update(missing_start_time_data)

```

```python
missing_time_upload_results
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
