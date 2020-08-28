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

## UW NOLA Fall19

Grant report for Fall 2019 UW LA

### Data Sources
- file1 : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QsnuUAC/view

- workshop report: https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007RFcfUAG/view
### Changes
- 01-07-2020 : Started project

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
from uszipcode import SearchEngine

SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Connection(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)

search = SearchEngine(simple_zipcode=True)
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "raw" / "sf_output.csv"
summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"


in_file2 = Path.cwd() / "data" / "raw" / "sf_output_2.csv"
summary_file2 = Path.cwd() / "data" / "processed" / "processed_data_2.pkl"
```

### Load Report From Salesforce

```python
report_id = "00O1M000007QsnuUAC"
sf_df = helpers.load_report(report_id, sf)
```

```python
report_id_2 = "00O1M000007RFcfUAG"
sf_df_workshops = helpers.load_report(report_id_2, sf)
```

#### Save report as CSV

```python
sf_df.to_csv(in_file, index=False)
```

```python
sf_df_workshops.to_csv(in_file2, index=False)
```

### Load DF from saved CSV
* Start here if CSV already exist

```python
df = pd.read_csv(in_file)
```

```python
df2 = pd.read_csv(in_file2)
```

### Data Manipulation

```python
df.columns
```

```python
df["Parish"] = df.apply(
    lambda x: search.by_zipcode(x["Mailing Zip/Postal Code"]).county, axis=1
)
```


```python
df['Global Academic Term'].value_counts()
```

```python
def determine_gpa_to_use(academic_term, prev_gpa, current_gpa):
    if current_gpa == "-":
        return prev_gpa
    else:
        return current_gpa
```

```python
df['gpa'] = df.apply(lambda x: determine_gpa_to_use(
    x['Global Academic Term'], x['GPA (Prev Term CGPA)'], x['GPA (Running Cumulative)']), axis=1)
```

```python

```

```python
df2_group = df2.groupby(['18 Digit ID','Workshop Display Name']).sum().reset_index()
```

```python
def adjust_workshop_name(workshop_name):
    if workshop_name.split(" ")[0] == "Summer":
        return 'summer_bridge'
    else:
        return workshop_name
```

```python
df2_group['workshop'] = df2_group.apply(lambda x: adjust_workshop_name(x['Workshop Display Name']),axis=1)
```

```python
df2_group['attendance_rate'] = df2_group['Attendance Numerator'] / df2_group['Attendance Denominator']
```

```python
df2_group['above_80'] = df2_group['attendance_rate'] >= .8
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
df.to_pickle(summary_file)
```

```python
df2_group.to_pickle(summary_file2)
```
