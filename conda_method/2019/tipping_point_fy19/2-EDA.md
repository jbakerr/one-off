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

This notebook contains basic statistical analysis and visualization of the data.

### Data Sources
- summary : Processed file from notebook 1-Data_Prep

### Changes
- 11-08-2019 : Started project

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
```

```python
%matplotlib inline
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "processed" / f"summary_{today:%b-%d-%Y}.pkl"
report_dir = Path.cwd() / "reports"
report_file = report_dir / "Excel_Analysis_{today:%b-%d-%Y}.xlsx"
```

```python
df = pd.read_pickle(in_file)
```

```python
df.head()
```

### Perform Data Analysis

```python

```

```python
def update_2_year_type(row):
    if row["Indicator: College Matriculation"] == "2-year":
        return "2-Year"
    else:
        return row["Fit Type (Affiliation) Lookup"]


df.loc[:, "Fit Type (Affiliation) Lookup"] = df.apply(
    lambda row: update_2_year_type(row), axis=1
)
```

```python
table = (
    df.groupby(["Site", "Fit Type (Affiliation) Lookup"])
    .size()
    .reset_index()
    .pivot(columns="Fit Type (Affiliation) Lookup", index="Site", values=0)
)
```

```python
table_subset = table.iloc[[2, 4, 6]]
```

```python
table_subset.loc["total", :] = table_subset.sum(axis=0)
table_subset_prct = table_subset.divide(table_subset.sum(axis=1), axis=0)
```

```python
table_subset_prct["row_total"] = table_subset_prct.sum(axis=1, numeric_only=False)
```

```python
table_subset_prct
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
