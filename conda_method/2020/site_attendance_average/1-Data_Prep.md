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

## Site Attendance Average

For ticket 8191

### Data Sources
- file1 : Link to SF Report
- file2:  Link to SF Report (As Needed)
- file3:  Link to SF Report (As Needed)

### Changes
- 06-19-2020 : Started project

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


SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Reportforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)
```

### File Locations

```python
# ALWAYS RUN
today = datetime.today()


in_file1 = Path.cwd() / "data" / "raw" / "site_attendance.csv"
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
# Run if downloading report from salesforce
# File 1 
report_id_file1 = "00O1M0000077bWnUAI"
file_1_id_column = '18 Digit ID' # adjust as needed
sf_df = sf.get_report(report_id_file1, id_column=file_1_id_column)



# File 2 (As needed)
# report_id_file2 = "SF_REPORT_ID"
# file_2_id_column = '18 Digit ID' # adjust as needed
# sf_df_file2 =  sf.get_report(report_id_file2, id_column=file_2_id_column)

# File 3 (As needed)
# report_id_file3 = "SF_REPORT_ID"
# file_3_id_column = '18 Digit ID' # adjust as needed
# sf_df_file3 =  sf.get_report(report_id_file3, id_column=file_3_id_column)

```

#### Save report as CSV

```python
# Only run if ran above cell
# File 1
sf_df.to_csv(in_file2, index=False)


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
df_file2
```

```python
roster = df_file2[df_file2['Contact Record Type'] == "Student: High School"]
```

```python
roster = roster[roster['High School Class'].isin([2023,2022,2020,2021])]
```

```python
roster_count = roster.groupby(['Site']).size()
```

```python
count = pd.DataFrame(df.groupby(['Site', 'Date']).size())
```

```python
count.rename(columns={0:"Avg Attendance"}, inplace=True)
```

```python
roster_count = pd.DataFrame(roster_count).rename(columns={0:"Enrollment"})
```

```python
def create_table(count, roster, count_mod):
    _count = count[count['Avg Attendance'] >= count_mod]
    
    _count = _count.groupby(['Site']).mean()
    
    _count_with_enrollment = _count.merge(roster, left_index=True, right_index=True)
    
    _count_with_enrollment['Percent'] = _count_with_enrollment['Avg Attendance'] / _count_with_enrollment['Enrollment']
    
    return _count_with_enrollment
    
    
    
    
```

```python
writer = pd.ExcelWriter("avg_attendance.xlsx", engine='xlsxwriter')
```

```python


create_table(count, roster_count,0).to_excel(writer, sheet_name='All Days')
```

```python
create_table(count, roster_count,5).to_excel(writer, sheet_name='Days with More than 5 Students')
```

```python
create_table(count, roster_count,10).to_excel(writer, sheet_name='Days with More than 10 Students')
```

```python

writer.save()
```

```python
count_more_5 = 
```

```python
 = count_more_5.
```

```python

```

```python
count_with_enrollent = test.merge(roster_count, left_index=True, right_index=True)
```

```python

```

```python
count_with_enrollent
```

### Data Manipulation

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
