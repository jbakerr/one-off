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

## NOLA Male African American Data

For ticket 7413

This notebook contains basic statistical analysis and visualization of the data.

### Data Sources
- summary : Processed file from notebook 1-Data_Prep

### Changes
- 02-24-2020 : Started project

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
```

```python
%matplotlib inline
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"
report_dir = Path.cwd() / "reports"
report_file = report_dir / "Excel_Analysis_{today:%b-%d-%Y}.xlsx"
```

```python
df = pd.read_pickle(in_file)
```

### Perform Data Analysis

```python
func = lambda x: 100 * x.count() / df.shape[0]

df["High School Class"].value_counts()
```

```python
df[df["Indicator: Years Since HS Graduation"] >= 6].pivot_table(
    index=["High School Class"],
    columns="Graduated: 4-Year Degree <=6 years",
    values="18 Digit ID",
    aggfunc=len,
)
```

```python
df["accepted_into_college"] = df["# Four Year College Acceptances"] > 0
accepted = df.pivot_table(
    index="High School Class",
    values=["18 Digit ID"],
    columns="accepted_into_college",
    aggfunc="count",
)

accepted
# accepted.div(accepted.iloc[:,-1], axis=0 )
```


```python
pd.crosstab(
    df["High School Class"],
    df["accepted_into_college"],
    values=df["18 Digit ID"],
    aggfunc=len,
    normalize="index",
)
```

```python
accepted.iloc[:, -1]
```

```python
df.head()
```

```python
df.pivot_table(
    index="High School Class",
    values=["18 Digit ID"],
    columns="Indicator: College Matriculation",
    aggfunc="count",
)
```


```python
df.pivot_table(
    index="High School Class",
    values=["18 Digit ID"],
    columns="Indicator: Persisted into Year 2 (Wide)",
    aggfunc="count",
)
```


### Save Excel file into reports directory

Save an Excel file with intermediate results into the report directory

```python
writer = pd.ExcelWriter(report_file, engine="xlsxwriter")
```

```python
df.to_excel(writer, sheet_name="Report")
```

```python
writer.save()
```
