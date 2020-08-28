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

## BH Long to Wide ACT

Boyle Heights requested a wide version of all ACT test data

### Data Sources
- file1 : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007QmXqUAK/view

### Changes
- 11-05-2019 : Started project

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
sf = Connection(
    username="brenneckar@collegetrack.org", password=SF_PASS, security_token=SF_TOKEN
)
```

### Load File from SF

```python
df = helpers.load_report("00O1M000007QmXqUAK", sf)
```

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "raw" / "report.csv"
summary_file = Path.cwd() / "data" / "processed" / f"summary_{today:%b-%d-%Y}.pkl"
```

```python
df.to_csv(in_file, index_label=False, index=False)
```

```python
df = pd.read_csv(in_file)
```

### Column Cleanup

- Remove all leading and trailing spaces
- Rename the columns for consistency.

```python
# https://stackoverflow.com/questions/30763351/removing-space-in-dataframe-python
df.columns = [x.strip() for x in df.columns]
```

```python
cols_to_rename = {"col1": "New_Name"}
df.rename(columns=cols_to_rename, inplace=True)
```

### Clean Up Data Types

```python
df.head()
```

### Data Manipulation

```python
# df = df.drop(['Test: ID'], axis=1)
```

```python
# For this ticket, everything will be contained in this cell
# test = pd.pivot_table(df, index='18 Digit ID', columns=['Full Name', 'High School Class'], aggfunc=max)
df["idx"] = df.groupby(["18 Digit ID", "Full Name", "High School Class"]).cumcount()
test = df.pivot(index="18 Digit ID", columns="idx")[["Global Academic Year", "Version"]]
```

```python
test = df.set_index(
    ["18 Digit ID", "Full Name", "High School Class", "Test: ID"]
).unstack()
# test.columns = test.columns.map(lambda x: print(x))
# test = test.reset_index()
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

Other options besides pickle include:
- feather
- msgpack
- parquet

```python
df.to_pickle(summary_file)
```

```python
test = df.pivot_table(
    index=["18 Digit ID", "Full Name", "High School Class"],
    columns=["Version", "Global Academic Year"],
    aggfunc="max",
)
test.columns = test.columns.map(lambda x: "{}_{}_{}".format(x[2], x[1], x[0]))
test = test.reset_index()
```

```python
test.to_csv("long_to_wide.csv")
```

```python

```
