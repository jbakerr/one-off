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

## Fight for Children Ward8

For development ticket #7001

### Data Sources
- file1 : https://ctgraduates.lightning.force.com/lightning/r/Report/00O1M000007Qw82UAC/view
- file2:  Link to SF Report (As Needed)
- file3:  Link to SF Report (As Needed)

### Changes
- 01-29-2020 : Started project

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
in_file1 = Path.cwd() / "data" / "raw" / "sf_output_file1.csv"
# in_file2 = Path.cwd() / "data" / "raw" / "sf_output_file3.csv"
# in_file3 = Path.cwd() / "data" / "raw" / "sf_output_file3.csv"

summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"
```

### Load Report From Salesforce

```python
# File 1
report_id_file1 = "00O1M000007Qw82UAC"
sf_df = helpers.load_report(report_id_file1, sf)

# File 2 and 3 (As needed)
# report_id_file2 = "SF_REPORT_ID"
# report_id_file3 = "SF_REPORT_ID"
# sf_df = helpers.load_report(report_id_file2, sf)
# sf_df = helpers.load_report(report_id_file3, sf)
```

```python
sf_df.head()
```

#### Save report as CSV

```python
# File 1
sf_df.to_csv(in_file1, index=False)


# File 2 and 3 (As needed)d
# sf_df.to_csv(in_file2, index=False)
# sf_df.to_csv(in_file3, index=False)
```


### Load DF from saved CSV
* Start here if CSV already exist

```python
# Data Frame for File 1 - if using more than one file, rename df to df_file1
df = pd.read_csv(in_file1)


# Data Frames for File 1 and 2 (As needed)

# df_file2 = pd.read_csv(in_file2)
# df_file3 = pd.read_csv(in_file3)
```

### Data Manipulation

```python
df
```

```python
ward_8_zips = [20032, 20020, 20373, 20024]

df["ward_8_resident"] = df.apply(
    lambda x: x["Mailing Zip/Postal Code"] in ward_8_zips, axis=1
)
```

```python
df.head()
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
# Save File 1 Data Frame (Or master df)
df.to_pickle(summary_file)
```

```python
len(df)
```

```python

```
