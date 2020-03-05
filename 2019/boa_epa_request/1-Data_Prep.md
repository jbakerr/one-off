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

## BoA EPA Request

For ticket 6876

### Data Sources
- file1 : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QqAWUA0/view

### Changes
- 12-10-2019 : Started project

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

### Load DF from saved CSV



```python
df = pd.read_csv(in_file)
```

### Data Manipulation

```python
df.head()
```

```python
# Because I was too lazy to create the report, dropping duplicated rows

df = df.drop_duplicates()
```

```python

```

```python
# Recode Workshop Departments so that there is a "department" for
# Financial Literacy, Math Intervention, and College Affordability.

workshop_counts = df["Workshop Session: Dosage Type"].value_counts()
```

```python
workshop_counts.to_csv("reports/out_file.csv")
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
df.to_pickle(summary_file)
```
