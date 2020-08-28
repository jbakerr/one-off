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

## Avg. PS Dropout Rate

used to determine the average dropout rate from the past three years

### Data Sources
- file1 :  https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007Qtg6UAC/edit

### Changes
- 01-13-2020 : Started project
- 

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

SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Connection(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "raw" / "sf_output.csv"
summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"
```

### Load Report From Salesforce

```python
report_id = "00O1M000007Qtg6UAC"
sf_df = helpers.load_report(report_id, sf)
```

```python
len(sf_df)
```

#### Save report as CSV

```python
sf_df.to_csv(in_file, index=False)
```

### Load DF from saved CSV
* Start here if CSV already exist

```python
df = pd.read_csv(in_file)
```

### Data Manipulation

```python
df.head()
```

```python
# Stripping everything past Fall and Spring in Global Academic Term

df["Global Academic Term"] = df["Global Academic Term"].str.split(" ").str[0]
```


```python
# Removing students that don't occur at least twice
df = df.groupby("18 Digit ID").filter(lambda x: len(x) > 1)
```

```python
# Removing any Fall Year 1 Data

df = df[~((df["Global Academic Term"] == "Fall") & (df["Grade (AT)"] == "Year 1"))]
```


```python
df = df[df["CT Status (AT)"] != "Did Not Finish CT HS Program"]
df = df[df["CT Status (AT)"] != "Prior to joining CT HS Program"]
```

```python
def create_year_grouping(term, year):
    if term == "Spring" and year == "AY 2015-16":
        return "Group 1 "
    elif term == "Fall" and year == "AY 2016-17":
        return "Group 1"
    elif term == "Spring" and year == "AY 2016-17":
        return "Group 2"
    elif term == "Fall" and year == "AY 2017-18":
        return "Group 2"
    elif term == "Spring" and year == "AY 2017-18":
        return "Group 3"
    elif term == "Fall" and year == "AY 2018-19":
        return "Group 3"
    else:
        return "Ignore"


df["group"] = df.apply(
    lambda x: create_year_grouping(
        x["Global Academic Term"], x["Global Academic Year"]
    ),
    axis=1,
)
```


```python
# drop ignore students

df = df[df["group"] != "Ignore"]
```


```python
# creating new column to determine modified status


def create_modified_status(enrollment, ct_status):
    if enrollment == "Not Enrolled":
        return "Inactive"
    elif ct_status == "Inactive: Post-Secondary":
        return "Inactive"
    else:
        return "Active"
```

```python
df["mod_status"] = df.apply(
    lambda x: create_modified_status(x["Enrollment Status"], x["CT Status (AT)"]),
    axis=1,
)
```

```python
# Removing students who were inactive or unenrolled in spring
df = df[~((df["Global Academic Term"] == "Spring") & (df["mod_status"] == "Inactive"))]
```


```python
len(df)
```

```python
# Remove students who don't appear at least two times in a single group

df = df.groupby(["group", "18 Digit ID"]).filter(lambda x: len(x) > 1)
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
df.to_pickle(summary_file)
```
