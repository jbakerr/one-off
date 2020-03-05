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

## GPA Growth

Used to evaluate GPA growth as requested by Q&L

### Data Sources
- file1 : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QqGyUAK/view?queryScope=userFolders

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
import numpy as np
from collections import Counter


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
report_id = "00O1M000007QqGyUAK"
sf_df = helpers.load_report(report_id, sf)
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
len(df)
```

```python
df.loc[:, "Site"] = df.loc[:, "Site"].str.replace("College Track ", "")
df.loc[:, "Site"] = df.loc[:, "Site"].str.replace("at ", "")
df.loc[:, "Region"] = df.loc[:, "Region"].str.replace("College Track ", "")
df.loc[:, "Region"] = df.loc[:, "Region"].str.replace(" Region", "")
```

```python
# Convert GPA (TERM) and GPA (Running Cumulative) to numeric
df["GPA (Term)"] = pd.to_numeric(df["GPA (Term)"], errors="coerce")
df["GPA (Running Cumulative)"] = pd.to_numeric(
    df["GPA (Running Cumulative)"], errors="coerce"
)
```

```python
# Loking at how many GPA Running Cumulatives are missing, it looks like there are a lot, compared to
# the number for spring 17/18 and spring 18/19. Going to create a new column called "GPA" which is equal to
# Term GPA for the first semester and the cum GPA for the following semesters
len(
    df[
        (df["Global Academic Term"] == "Fall 2017-18 (Semester)")
        & df["GPA (Running Cumulative)"].isna()
    ]
)
```

```python
len(
    df[
        (df["Global Academic Term"] == "Spring 2017-18 (Semester)")
        & df["GPA (Running Cumulative)"].isna()
    ]
)
```

```python
len(
    df[
        (df["Global Academic Term"] == "Spring 2018-19 (Semester)")
        & df["GPA (Running Cumulative)"].isna()
    ]
)
```

```python
def create_gpa_column(row):
    if row["Global Academic Term"] == "Fall 2017-18 (Semester)":
        return row["GPA (Term)"]
    else:
        return row["GPA (Running Cumulative)"]
```

```python
df["GPA"] = df.apply(lambda row: create_gpa_column(row), axis=1)
```

```python
# Remove rows if GPA Term is NaN
df = df.dropna(subset=["GPA"])
```

```python
# pulling out Fall 17-18
df_year_1 = df[(df["Global Academic Term"] == "Fall 2017-18 (Semester)")]

df_year_2 = df[(df["Global Academic Term"] == "Spring 2018-19 (Semester)")]
```

```python
# Sorting data frame by years since hs grad (should be a negative number) with the larger number coming second
df_year_1 = df_year_1.sort_values("Indicator: Years Since HS Grad (AT)")
# Dropping the duplicated values, keeping the first (older) value
df_year_1 = df_year_1.drop_duplicates(subset="18 Digit ID", keep="first")
```

```python
len(df_year_2[df_year_2["Global Academic Term"] == "Spring 2018-19 (Semester)"])
```

```python
# Adding the Spring 18-19 back into the filtered Year 1 Data Frame
df_combined = pd.concat([df_year_1, df_year_2])
```

```python
df_combined = df_combined.sort_values(by=["Full Name"])
```

```python

```

```python
# df_combined.to_csv("test.csv")
```

```python
(df_combined["18 Digit ID"].value_counts() > 1).value_counts()
```

```python
# Keeping students who only have BOTH a Fall 17-18 GPA and a Spring 18-19 GPA

complete_spring = df_combined[
    (df_combined["Global Academic Term"] == "Spring 2018-19 (Semester)")
]

complete_fall = df_combined[
    (df_combined["Global Academic Term"] != "Spring 2018-19 (Semester)")
]

fall_ids = complete_fall["18 Digit ID"]
spring_ids = complete_spring["18 Digit ID"]

valid_ids = fall_ids.append(spring_ids, ignore_index=True)
cnt = Counter(valid_ids)
valid_ids = [k for k, v in cnt.items() if v > 1]


subset_spring = complete_spring[complete_spring["18 Digit ID"].isin(valid_ids)]
subset_fall = complete_fall[complete_fall["18 Digit ID"].isin(valid_ids)]
```


```python
# Joining complete fall with subset spring

complete_df = pd.concat([subset_fall, subset_spring])
```

```python
(complete_df["18 Digit ID"].value_counts() >= 2).value_counts()
```

```python
# Creating new column to indicate if it is year 1 or year 2

complete_df["student_year"] = complete_df["Global Academic Term"].apply(
    lambda x: "Fall 2017-18" if x != "Spring 2018-19 (Semester)" else "Spring 2018-19"
)
```


```python
# creating a new bucket column that is calculated using the data filtered thus far.


def determine_gpa_bucket(gpa):
    gpa_buckets = ["Below 2.5", "2.5 to 2.74", "2.75 to 2.99", "3.0 to 3.49", "3.5+"]

    if gpa < 2.5:
        return gpa_buckets[0]
    elif gpa < 2.75:
        return gpa_buckets[1]
    elif gpa < 3:
        return gpa_buckets[2]
    elif gpa < 3.5:
        return gpa_buckets[3]
    else:
        return gpa_buckets[4]


complete_df["GPA Bucket"] = complete_df.apply(
    lambda row: determine_gpa_bucket(row["GPA"]), axis=1
)
```


### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
complete_df.to_pickle(summary_file)
```

```python
len(complete_df)
```

```python

```
