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

This notebook contains basic statistical analysis and visualization of the data.

### Data Sources
- summary : Processed file from notebook 1-Data_Prep

### Changes
- 12-02-2019 : Started project

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
import xlsxwriter
```

```python
%matplotlib inline
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "processed" / f"summary_{today:%b-%d-%Y}.pkl"
report_dir = Path.cwd() / "reports"
report_file = report_dir / f"Excel_Analysis_{today:%b-%d-%Y}.xlsx"
```

```python
df = pd.read_pickle(in_file)
```

### Perform Data Analysis

```python
# getting pivot table of number of students by year

student_count_pivot = pd.pivot_table(
    df,
    index="High School Class",
    values="18 Digit ID",
    aggfunc=pd.Series.nunique,
    margins=True,
)
student_count_pivot
```

```python
df.head()
```

```python
workshop_pivot = pd.pivot_table(
    df,
    index=["High School Class"],
    values="calc_duration",
    columns="report_group",
    aggfunc=sum,
    margins=True,
    fill_value=0,
)
```

```python
workshop_pivot
```

### Save Excel file into reports directory

Save an Excel file with intermediate results into the report directory

```python
writer = pd.ExcelWriter(report_file, engine="xlsxwriter")
```

```python
workshop_pivot.to_excel(writer, sheet_name="Workshop Details")
student_count_pivot.to_excel(writer, sheet_name="Student Details")
```

```python
writer.save()
```

```python

```
