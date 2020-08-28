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

## Incoming Cohort GPA

Looking at the distrobutions of incoming cohort's gpa for the past 4 academic years (class of 2019-2022).

### Data Sources
- file1 : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QnSmUAK/view

### Changes
- 11-13-2019 : Started project

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

# sf = Connection(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "raw" / "raw_data.csv"
summary_file = Path.cwd() / "data" / "processed" / f"summary_{today:%b-%d-%Y}.pkl"
```

### Load DF from saved CSV

```python
df = pd.read_csv(in_file)
```

### Data Manipulation

```python
# Remove rows if GPA Term is NaN
df = df.dropna(subset=["GPA (Term)"])
```

```python
# count of unique students (to compare to later)
# Doing this after the last cell because last cell might have removed some unique students (if they had no GPA data)
orig_unique_students = len(df["18 Digit ID"].unique())
```

```python
# Ensuring that the data frame only has students with just one, or at most 2 semesters.
df.groupby(df["18 Digit ID"], as_index=False).size().value_counts()
```

```python
# Sorting data frame by years since hs grad (should be a negative number) with the larger number coming second
df = df.sort_values("Indicator: Years Since HS Grad (AT)")
# Dropping the duplicated values, keeping the first (older) value
df = df.drop_duplicates(subset="18 Digit ID", keep="first")
```

```python
# ensuring that there is only a single record for each student
df.groupby(df["18 Digit ID"], as_index=False).size().value_counts()
```

```python
# Ensuring the count of students in the new data frame equals the original unique count
len(df) == orig_unique_students
```

```python
# Removing "College Track" and "Region" from Region and Site column values

df.loc[:, "Site"] = df.loc[:, "Site"].str.replace("College Track ", "")
df.loc[:, "Site"] = df.loc[:, "Site"].str.replace("at ", "")
df.loc[:, "Region"] = df.loc[:, "Region"].str.replace("College Track ", "")
df.loc[:, "Region"] = df.loc[:, "Region"].str.replace(" Region", "")

# df.Region = df.loc[:,'Region'].map(lambda x: x.lstrip('College Track '))
# df.loc[:,'Region'] = df.loc[:,'Region'].map(lambda x: x.rstrip(' Region'))
# data['result'] = data['result'].map(lambda x: x.lstrip('+-').rstrip('aAbBcC'))
```


```python
# Setting the 18 digit id as the index
df.set_index("18 Digit ID", inplace=True)
```

```python
df.Site.unique()
```

```python
df.Region.unique()
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
df.to_pickle(summary_file)
```

```python
df.head()
```

```python

```
