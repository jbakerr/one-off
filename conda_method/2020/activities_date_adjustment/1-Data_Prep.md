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

## Activities Date Adjustment

A short description of the project.

### Data Sources
- file1 : Link to SF Report
- file2:  Link to SF Report (As Needed)
- file3:  Link to SF Report (As Needed)

### Changes
- 05-06-2020 : Started project

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
from simple_salesforce import Salesforce


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
today = datetime.today()


in_file1 = Path.cwd() / "data" / "raw" / "activities.csv"
summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"


in_file2 = Path.cwd() / "data" / "raw" / "sf_output_file2.csv"
summary_file2 = Path.cwd() / "data" / "processed" / "processed_data_file2.pkl"


in_file3 = Path.cwd() / "data" / "raw" / "sf_output_file3.csv"
summary_file3 = Path.cwd() / "data" / "processed" / "processed_data_file3.pkl"


in_file4 = Path.cwd() / "data" / "raw" / "sf_output_file4.csv"
summary_file4 = Path.cwd() / "data" / "processed" / "processed_data_file4.pkl"
```

### Load Report From Salesforce


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
def adjust_date(old_date, new_date):
    if pd.isna(old_date):
        return (new_date)
    else:
        return old_date
```

```python
df['Date'] = pd.to_datetime(df['Date'])
```

```python
df[df.Date >= datetime(2020, 3, 1)]
```

```python
df['Date of Contact'] = pd.to_datetime(df['Date of Contact'])
```

```python
df_na_date = df[pd.isna(df['Date'])]
```

```python
df_na_date = df_na_date[~pd.isna(df_na_date['Date of Contact'])]
```

```python
df_na_date.loc[:,'Date'] = df_na_date.apply(
    lambda x: adjust_date(x['Date'], x['Date of Contact']), axis=1)
```

```python
df_na_date['Date'] = df_na_date['Date'].dt.strftime("%Y-%m-%d")
```

```python
df_na_date['Date of Contact'] = df_na_date['Date of Contact'].dt.strftime("%Y-%m-%d")
```

```python
def prep_data_file(date_field, date, record_id):
    data = {"Id": record_id,
           date_field: date}
    return data
```

```python

```

```python
df_na_date
```

```python
data = []
```

```python
data.extend(df_na_date.apply(lambda x: prep_data_file("ActivityDate", x['Date'], x['Activity ID']),axis=1))
```

```python
len(data)
```

```python
def upload_data(df, data, sf_upload):
    #     print(data)
    #     df = df.reset_index(drop=True)
    results = sf_upload.bulk.Task.update(data)

    results_df = pd.DataFrame(results)

    df_with_status = pd.concat([df, results_df], axis=1)

    success_df = df_with_status[df_with_status["success"] == True]

    fail_df = df_with_status[df_with_status["success"] == False]

    return success_df, fail_df, results_df
```

```python
success_df, fail_df, results_df = upload_data(df_na_date, data, sf_upload)
```

```python
fail_df
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
