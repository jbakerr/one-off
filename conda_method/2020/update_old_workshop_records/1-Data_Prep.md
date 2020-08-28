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

## Update Old Workshop Records

For migrating old workshops into BQ

### Data Sources
- file1 : Link to SF Report
- file2:  Link to SF Report (As Needed)
- file3:  Link to SF Report (As Needed)

### Changes
- 04-30-2020 : Started project

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
from gspread_pandas import Spread, Client



SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Reportforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)
```

### File Locations

```python
# ALWAYS RUN
today = datetime.today()


in_file1 = Path.cwd() / "data" / "raw" / "Workshop_Enrollment.csv"
summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"


in_file2 = Path.cwd() / "data" / "raw" / "Session_Attendance.csv"
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
# report_id_file1 = "SF_REPORT_ID"
# file_1_id_column = '18 Digit ID' # adjust as needed
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
sf_df.to_csv(in_file1, index=False)


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

df_file2 = pd.read_csv(in_file2)
# df_file3 = pd.read_csv(in_file3)
```

```python
google_sheet_key = "1P8qUkFSSQRWZbRFczlzmOeMUe03F6reoQVjf0ond4Lo"

id_matching_sheet = Spread(google_sheet_key)
id_matching_sheet.open_sheet(1)
df_ats = id_matching_sheet.sheet_to_df(index=None)

id_matching_sheet.open_sheet(2)
df_18_id = id_matching_sheet.sheet_to_df(index=None)

```

```python
df_18_id = df_18_id[['18 Digit ID', 'Historical - Contact ID']]
```

```python
df_18_id.rename(columns={'Historical - Contact ID': "STUDENT__C"}, inplace=True)
```

```python
df_18_id
```

```python
df_ats
```

```python
df_withid = df.merge(df_18_id, on='STUDENT__C', how='left')
```

```python
df_withid.head()
```

```python
def create_matching_key_old_data(student_id, semester, year):
    if pd.isna(student_id):
        return np.nan
    
    if semester == "S1":
        new_semster = "Fall"
    elif semester == "S2":
        new_semster = "Spring"
    else:
        new_semster = semester

    new_year = [int(i) for i in year.split('/')]
    new_year[1] -= 2000
    new_year = [str(i) for i in new_year]
    new_year = "-".join(new_year)
    

    return student_id+new_semster + " " + new_year
```

```python
test = df_withid['SCHOOL_YEAR__C'][0]
```

```python
test = [int(i) for i in test.split('/')]
```

```python
test[1] -= 2000

```

```python
[str(i) for i in test]
```

```python
"-".join(test)
```

```python
df_withid['key'] = df_withid.apply(
    lambda x: create_matching_key_old_data(x['18 Digit ID'], x['SEMESTER__C'], x['SCHOOL_YEAR__C']), axis=1)
```

```python
def create_matching_key_new_data(student_id, academic_term_name):
    short_at = academic_term_name.split(" ")
    new_at = " ".join(short_at[:2])
    

    return student_id+new_at
```

```python
df_ats['key'] = df_ats.apply(lambda x: create_matching_key_new_data(
    x['18 Digit ID'], x['Academic Term: Academic Term Name']), axis=1)
```

```python
df_ats = df_ats[['Academic Term: ID', "key"]]
```

```python
df_withid.merge(df_ats, on='key', how='left')
```

```python
df_withid.rename(columns={'18 Digit ID': "New_Instance_Student_ID",
                          'Academic Term: ID': "New_Instance_Academic_Term_D"}, inplace=True)
```

### Data Manipulation

```python
def determine_numerator_denominator(attendance, attend_type):
    attended_values = ["Attended","Make Up"]
    denominator_values = attended_values + ['Absent']
    if attend_type == "num":
        if attendance in attended_values:
            return 1
        else:
            return 0
    else:
        if attendance in denominator_values:
            return 1
        else:
            return 0
```

```python
df_file2['Attendance_Numerator__c'], df_file2['Attendance_Denominator__c'] = 0, 0
```

```python
df_file2['Attendance_Numerator__c'] = df_file2.apply(
    lambda x: determine_numerator_denominator(x['ATTENDANCE__C'], "num"), axis=1)
```

```python
df_file2['Attendance_Denominator__c'] = df_file2.apply(
    lambda x: determine_numerator_denominator(x['ATTENDANCE__C'], "den"), axis=1)
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
df_file2.to_csv("Workshop_Session_Attendance_Modified.csv")
```

```python
df_withid.to_csv("Workshop_Enrollment_Modified.csv")
```

```python

```
