---
jupyter:
  jupytext:
    formats: ipynb,md
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

## Mail Merge

A project started to create a mail merge template for Aurora

### Data Sources
- General data (df) : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QpT8UAK/view
    - Contains majority of needed data
- Test (test_df): https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QpnDUAS/view
    - Contains all the required test data
- Scholarship Applications (scholarships_df): https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QpnNUAS/view
    - Contains all the scholarship application information

### Changes
- 12-06-2019 : Started project

```python
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

SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Connection(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)
```

### File Locations

```python
today = datetime.today()
df_in_file = Path.cwd() / "data" / "raw" / "general_data.csv"
test_in_file = Path.cwd() / "data" / "raw" / "test_data.csv"
scholarship_in_file = Path.cwd() / "data" / "raw" / "scholarship_data.csv"

summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"
```

### Load Report From Salesforce

```python
general_report_id = "00O1M000007QpT8UAK"
test_report_id = "00O1M000007QpnDUAS"
scholarship_report_id = "00O1M000007QpnNUAS"

df_in = helpers.load_report(general_report_id, sf)
test_df_in = helpers.load_report(test_report_id, sf)
scholarship_df_in = helpers.load_report(scholarship_report_id, sf)
```

#### Save report as CSV

```python
df_in.to_csv(df_in_file, index=False)
test_df_in.to_csv(test_in_file, index=False)
scholarship_df_in.to_csv(scholarship_in_file, index=False)
```

### Load DF from saved CSV

```python
df = pd.read_csv(df_in_file)
test_df = pd.read_csv(test_in_file)
scholarship_df = pd.read_csv(scholarship_in_file)
```

### Data Manipulation

```python
# For AUR, subsetting all data frames to only include their data.
# For future reports, don't run this cell or change the filter value
df = df[df["Site"] == "College Track Aurora"]
test_df = test_df[test_df["Site"] == "College Track Aurora"]
scholarship_df = scholarship_df[scholarship_df["Site"] == "College Track Aurora"]
```


```python
# Creating a pivot table summing the number of scholarships a student applied to

scholarship_count = scholarship_df.pivot_table(
    index="18 Digit ID",
    columns=["Scholarship Application: Record Type"],
    values="Scholarship Application: ID",
    aggfunc="count",
    margins=True,
    fill_value=0,
)
```

```python
scholarship_count = scholarship_count.drop(index="All", axis=0)
```

```python
scholarship_count = scholarship_count.rename(columns={"All": "Total Scholarships"})
```

```python
# Creating a table which pulls the most recent diagnostics test data avaliable for each student

test_df["Test Date"] = pd.to_datetime(test_df["Test Date"])
```

```python
test_df
```

```python
most_recent_test = test_df.sort_values("Test Date").drop_duplicates(
    "18 Digit ID", keep="last"
)
```

```python
most_recent_test = most_recent_test.rename(columns={"SAT Total Score": "PSAT"})
```

```python
most_recent_test = most_recent_test["PSAT"]
```

```python
# Setting the index for all data frames for merging

most_recent_test = most_recent_test.set_index("18 Digit ID")

df = df.set_index("18 Digit ID")

scholarship_df = scholarship_df.set_index("18 Digit ID")
```

```python
master_df = df.merge(scholarship_count, on="18 Digit ID", how="left")
```

```python
master_df = master_df.merge(most_recent_test, on="18 Digit ID", how="left")
```

```python
master_df
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
master_df.to_csv("reports/aur_mail_merge.csv")
```

```python

```
