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

## SAC Literacy Map

A report that counts all the hours students attended at selected workshops in AY 2Y18-19

### Data Sources
- file1 : Description of where this file came from

### Changes
- 12-02-2019 : Started project

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

report_id = "00O1M000007QpDAUA0"
```


```python
%load_ext autoreload
%autoreload 2
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "raw" / "sf_output.csv"
summary_file = Path.cwd() / "data" / "processed" / f"summary_{today:%b-%d-%Y}.pkl"
```

### Load Report

```python
df = pd.read_csv(in_file)
```

### Data Manipulation

```python
# finding areas where Forumula doesn't match workshop session workshop duration

df["calc_duration"] = df.apply(
    lambda x: x["Workshop Session: Workshop Duration"] / 60, axis=1
)
```


```python
# The number of "True" is the number of records that have a greater than half hour descrepancy
(abs(df["calc_duration"] - df["Formula - Total Session Hours"]) > 0.5).value_counts()
```

```python
# Drop in session aren't being calculated correctly in the "Formaul = Total Sessions Hours"
# this checks the values and makes sure they are right

# this subset is for drop in sessions that lasted longer than 3 hours.
# Upon evaluation it looks like it was a field trip, thus is correct
df[(df.Attendance == "Drop-in") & (df.calc_duration > 3)]

# setting Formula value to calc value (for verification)
df.loc[df.Attendance == "Drop-in", "Formula - Total Session Hours"] = df.calc_duration
```

```python
# Still some records that need to be cleaned up
(abs(df["calc_duration"] - df["Formula - Total Session Hours"]) > 0.5).value_counts()
```

```python
# it looks like all of these records are correct in the Formula field,
# so I'm going to set the calc field equal to that
df[abs(df["calc_duration"] - df["Formula - Total Session Hours"]) > 0.5][
    "Formula - Total Session Hours"
].describe()

df.loc[
    abs(df["calc_duration"] - df["Formula - Total Session Hours"]) > 0.5,
    "calc_duration",
] = df["Formula - Total Session Hours"]
```

```python
# Making sure all Trues have been accounted for
(abs(df["calc_duration"] - df["Formula - Total Session Hours"]) > 0.5).value_counts()
```

```python
# Setting up a new column to break out the students into the gruops required for the report
# All Drop in students coded as "Other"
# All Tutoring sessions coded as "Other"
# All Student Life session coded as "Other"
# All makeup sessions (that aren't tutoring) coded as "Small Group"
# All remaining sessions coded as "Small Group"

df["report_group"] = ""

df.loc[df.Attendance == "Drop-in", "report_group"] = "Other"
df.loc[df["Workshop Dosage Type"] == "Tutoring", "report_group"] = "Other"
df.loc[df["Workshop Department"] == "Student Life", "report_group"] = "Other"
df.loc[
    (df.Attendance == "Make Up") & (df.report_group != "Other"), "report_group"
] = "Small Group"
df.loc[
    (df.Attendance == "Attended") & (df.report_group != "Other"), "report_group"
] = "Small Group"
df.loc[
    (df.Attendance == "Tardy") & (df.report_group != "Other"), "report_group"
] = "Small Group"
```


```python
df.report_group.value_counts()
```

```python
df.head()
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
df.to_pickle(summary_file)
```

```python

```
