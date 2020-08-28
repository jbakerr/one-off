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

## Tipping Point FY19

Ticket #6755 Data for Tipping Point FY19 Data Request

### Data Sources
- file1 : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007Qn5xUAC/view

### Changes
- 11-08-2019 : Started project

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
summary_file = Path.cwd() / "data" / "processed" / f"summary_{today:%b-%d-%Y}.pkl"
```

### Load Report From Salesforce

```python
report_id = "00O1M000007Qn5xUAC"
sf_df = helpers.load_report(report_id, sf)
```

```python
sf_df.head()
```

#### Save report as CSV

```python
sf_df.to_csv(in_file, index=False)
```

### Load DF from saved CSV

```python
df = pd.read_csv(in_file)
```

### Data Manipulation

```python

```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
df.to_pickle(summary_file)
```

```python

```
