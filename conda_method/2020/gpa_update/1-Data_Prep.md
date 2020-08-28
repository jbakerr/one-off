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

## gpa_update

a

### Data Sources
- file1 : Link to SF Report
- file2:  Link to SF Report (As Needed)
- file3:  Link to SF Report (As Needed)

### Changes
- 08-03-2020 : Started project

```python
# ALWAYS RUN
# General Setup 

%load_ext dotenv
%dotenv
%load_ext nb_black

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


in_file1 = Path.cwd() / "data" / "raw" / "sf_output_file1.csv"
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
report_id_file1 = "SF_REPORT_ID"
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

# df_file2 = pd.read_csv(in_file2)
# df_file3 = pd.read_csv(in_file3)
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
