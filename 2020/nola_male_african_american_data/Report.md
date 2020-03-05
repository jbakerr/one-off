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

## Report for NOLA African American Male Students

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
```

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"
report_dir = Path.cwd() / "reports"
report_file = report_dir / "Excel_Analysis_{today:%b-%d-%Y}.xlsx"
```

```python
df = pd.read_pickle(in_file)
```

### Percent of Students Accepted into College

```python
df["accepted_into_college"] = df["# Four Year College Acceptances"] > 0

pd.crosstab(
    df["High School Class"],
    df["accepted_into_college"],
    values=df["18 Digit ID"],
    aggfunc=len,
    normalize="index",
).round(2)
```

### Percent of Students Matriculated into College

```python
df_subset = df[df["High School Class"] > 2014]
pd.crosstab(
    df_subset["High School Class"],
    df_subset["Indicator: College Matriculation"],
    values=df_subset["18 Digit ID"],
    aggfunc=len,
    normalize="index",
).round(2)
```

### • % college freshmen persistence rate


```python
df_subset_less = df_subset[df_subset["High School Class"] < 2019]
pd.crosstab(
    df_subset_less["High School Class"],
    df_subset_less["Indicator: Persisted into Year 2 (Wide)"],
    values=df_subset_less["18 Digit ID"],
    aggfunc=len,
    normalize="index",
).round(2)
```

### • % college graduation rate



```python
df_college_grads = df[df["Indicator: Years Since HS Graduation"] >= 6]

pd.crosstab(
    df_college_grads["High School Class"],
    df_college_grads["Graduated: 4-Year Degree <=6 years"],
    values=df_college_grads["18 Digit ID"],
    aggfunc=len,
    normalize="index",
).round(2)

# pivot_table(index=['High School Class'], columns='Graduated: 4-Year Degree <=6 years', values='18 Digit ID', aggfunc=len)
```

### # of Students Who Completed HS Program (College enrollment proxy) historically

```python
df["High School Class"].value_counts()
```

```python

```
