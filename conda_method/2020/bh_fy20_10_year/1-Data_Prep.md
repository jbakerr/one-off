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

## BH fy20 10 year

For Will.i.am 

### Data Sources
- Valid ATs : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007RFZqUAO/view
- Service Hours:  https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007RFhGUAW/view
- file3:  Link to SF Report (As Needed)

### Changes
- 07-27-2020 : Started project

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


in_file1 = Path.cwd() / "data" / "raw" / "academic_terms.csv"
summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"


in_file2 = Path.cwd() / "data" / "raw" / "service_hours.csv"
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
# report_id_file1 = "00O1M000007RFZqUAO"
# file_1_id_column = 'Academic Term: ID' # adjust as needed
# sf_df = sf.get_report(report_id_file1, id_column=file_1_id_column)



# File 2 (As needed)
# report_id_file2 = "00O1M000007RFhGUAW"
# file_2_id_column = 'Student Life Activity: ID' # adjust as needed
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

df_file2 = pd.read_csv(in_file2)
# df_file3 = pd.read_csv(in_file3)
```

### Data Manipulation

```python
# File 1
# df = helpers.shorten_site_names(df)
# df = helpers.clean_column_names(df)

# File 2
# df_file2 = helpers.shorten_site_names(df_file2)
# df_file2 = helpers.clean_column_names(df_file2)
```

```python
df.columns
```

```python
df_file2
```

```python
len(df)
```

```python
df_merge = df.merge(df_file2[["Academic Term", "Hours of Service Completed"]],
         left_on='Academic Term: Academic Term Name', right_on='Academic Term', how="right", indicator=True)
```

```python
len(df_merge)
```

```python
df_group = df_merge.groupby(['18 Digit ID', "Global Academic Year","Global Academic Term", "CT Status (AT)"]).sum().reset_index()
```

```python
test = df_group.groupby(['18 Digit ID', "Global Academic Year"]).filter(lambda x: (x['CT Status (AT)'] != "Did Not Finish CT HS Program").any())
```

```python
# df_group.groupby(['18 Digit ID', "Global Academic Year"])['CT Status (AT)'].transform(lambda x: x.isin("Current CT HS Program")).min()

# len(x[x.C == 'T']) == len(x)
```

```python
df_group[df_group['CT Status (AT)'] == "Did Not Finish CT HS Program"]
```

```python
valid_ats = df_group[df_group.groupby(['18 Digit ID', "Global Academic Year"])['CT Status (AT)'].transform(lambda x: x.isin(["Current CT HS Student"]).min())]
```

```python
year_sum = valid_ats.groupby(["Global Academic Year"]).sum().reset_index()
```

```python
year_sum['cum_sum'] = year_sum['Hours of Service Completed'].cumsum()
```

```python
year_sum[['Global Academic Year', "Hours of Service Completed", "cum_sum"]].to_csv("hours.csv")
```

```python
year_sum['Hours of Service Completed'].sum()
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
# Save File 1 Data Frame (Or master df)
df.to_pickle(summary_file)
```
