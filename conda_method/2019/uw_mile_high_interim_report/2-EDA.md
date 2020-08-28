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

## UW Mile High Interim Report

Interim Report for FY20 UW Mile High

This notebook contains basic statistical analysis and visualization of the data.

### Data Sources
- summary : Processed file from notebook 1-Data_Prep

### Changes
- 12-02-2019 : Started project

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
attend_file = Path.cwd() / "data" / "processed" / "processed_attend_data.pkl"
report_dir = Path.cwd() / "reports"
report_file = report_dir / "Excel_Analysis_{today:%b-%d-%Y}.xlsx"
```

```python
df = pd.read_pickle(in_file)
attend_df = pd.read_pickle(attend_file)
```

```python
attend_df["18 Digit ID"].value_counts()
```

### Perform Data Analysis

<!-- #region heading_collapsed=true -->
#### Age, Gender, Race, Citizen Pivots
<!-- #endregion -->

```python hidden=true
# Age Pivot

age_pivot = df.pivot_table(index="Age", values="18 Digit ID", aggfunc=pd.Series.nunique)

age_buckets = {
    "9-13": range(9, 14),
    "14-18": range(14, 19),
    "19-24": range(19, 25),
    "25-64": range(25, 64),
}

age_pivot_buckets = {"Age Range": [], "Count": []}

for name, num_range in age_buckets.items():
    calc = 0
    for i in num_range:
        try:
            calc += age_pivot.loc[i].values[0]
        except:
            continue
    age_pivot_buckets["Age Range"].append(name)
    age_pivot_buckets["Count"].append(calc)
```


```python hidden=true
age_pivot_buckets = pd.DataFrame.from_dict(age_pivot_buckets).set_index("Age Range")
age_pivot_buckets
```

```python hidden=true
# Race Pivot

race_pivot = df.pivot_table(
    index="Ethnic background", values="18 Digit ID", aggfunc=pd.Series.nunique
)
race_pivot
```

```python hidden=true
# Gender Pivot

gender_pivot = df.pivot_table(
    index="Gender", values="18 Digit ID", aggfunc=pd.Series.nunique
)
gender_pivot
```

```python hidden=true
# Citizen Pivot

citizen_pivot = df.pivot_table(
    index="Citizen?", values="18 Digit ID", aggfunc=pd.Series.nunique
)
citizen_pivot
```

#### Students Enrolled in 2 Year Programs

```python
school_type_pivot = df.pivot_table(
    index="Current School Type", values="18 Digit ID", aggfunc=pd.Series.nunique
)
school_type_pivot
```

#### Class Pivot

```python
df["High School Class"].value_counts()
```

```python
len(df)
```

#### Low Income Pivot

```python
low_income_pivot = df.pivot_table(
    index="Indicator: Low-Income", values="18 Digit ID", aggfunc=pd.Series.nunique
)
low_income_pivot
```

#### Attendance Data

```python
attendance_pivot = attend_df.pivot_table(
    index=["Site", "18 Digit ID"],
    values=["Attendance Numerator", "Attendance Denominator"],
    aggfunc=np.sum,
)
```


```python
attendance_pivot["Attendance Rate"] = attendance_pivot.apply(
    lambda x: (x["Attendance Numerator"] / x["Attendance Denominator"]) * 100, axis=1
)
```


```python
(attendance_pivot["Attendance Rate"] >= 80).value_counts()
```

```python
(attendance_pivot["Attendance Numerator"] >= 30).value_counts()
```

```python
attendance_pivot["Attendance Numerator"].describe()
```

### Save Excel file into reports directory

Save an Excel file with intermediate results into the report directory

```python
writer = pd.ExcelWriter(report_file, engine="xlsxwriter")
```

```python
age_pivot_buckets.to_excel(writer, sheet_name="Ages")
race_pivot.to_excel(writer, sheet_name="Ethnicy")
gender_pivot.to_excel(writer, sheet_name="Gender")
citizen_pivot.to_excel(writer, sheet_name="Citizenship")
low_income_pivot.to_excel(writer, sheet_name="Low Income")
```

```python
writer.save()
```

```python

```

```python
attendance_pivot.describe()
```

```python
attendance_pivot.groupby("Site").describe()["Attendance Numerator"]
```

```python
df2
```

```python

```
