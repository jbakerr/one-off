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

# Fight for Children Ward 8 Report

```python
import pandas as pd
from pathlib import Path
from datetime import datetime

%matplotlib inline

today = datetime.today()
in_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"
report_dir = Path.cwd() / "reports"
report_file = report_dir / "Excel_Analysis_{today:%b-%d-%Y}.xlsx"
```

```python
df = pd.read_pickle(in_file)
```

```python
df_current_only = df[df["College Track Status"] == "Current CT HS Student"]
```

### *# of students enrolled (Current CT HS Student Only):

```python
len(df_current_only)
```

### *# of students enrolled (Current CT HS Student AND Onboarding):

```python
len(df)
```

### *#/% racial/ethnic demographics (Current CT HS Student Only):

```python
ethnic_table = df_current_only.pivot_table(
    index="Ethnic background", values="18 Digit ID", aggfunc="count"
)


ethnic_table["% of Total"] = (
    round(
        (ethnic_table["18 Digit ID"] / ethnic_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

ethnic_table
```

### ### *#/% racial/ethnic demographics (Current CT HS Student AND Onboarding):

```python
ethnic_table = df.pivot_table(
    index="Ethnic background", values="18 Digit ID", aggfunc="count"
)

ethnic_table["% of Total"] = (
    round(
        (ethnic_table["18 Digit ID"] / ethnic_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

ethnic_table
```

### *#/% male/female demographics ( Current CT HS Student Only):

```python
gender_table = df_current_only.pivot_table(
    index="Gender", values="18 Digit ID", aggfunc="count"
)

gender_table["% of Total"] = (
    round(
        (gender_table["18 Digit ID"] / gender_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

gender_table
```

### *#/% male/female demographics ( Current CT HS Student AND Onboarding):

```python
gender_table = df.pivot_table(index="Gender", values="18 Digit ID", aggfunc="count")

gender_table["% of Total"] = (
    round(
        (gender_table["18 Digit ID"] / gender_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

gender_table
```

### *#/% low-income (Current CT HS Student Only):


```python
low_income_table = df_current_only.pivot_table(
    index="Indicator: Low-Income", values="18 Digit ID", aggfunc="count"
)

low_income_table["% of Total"] = (
    round(
        (low_income_table["18 Digit ID"] / low_income_table["18 Digit ID"].sum() * 100),
        0,
    ).astype(str)
    + "%"
)

low_income_table
```

### *#/% low-income (Current CT HS Student AND Onboarding):

```python
low_income_table = df.pivot_table(
    index="Indicator: Low-Income", values="18 Digit ID", aggfunc="count"
)

low_income_table["% of Total"] = (
    round(
        (low_income_table["18 Digit ID"] / low_income_table["18 Digit ID"].sum() * 100),
        0,
    ).astype(str)
    + "%"
)

low_income_table
```

### *#/% first-generation (Current CT HS Student Only):

```python
first_gen_table = df_current_only.pivot_table(
    index="First Generation", values="18 Digit ID", aggfunc="count"
)

first_gen_table["% of Total"] = (
    round(
        (first_gen_table["18 Digit ID"] / first_gen_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

first_gen_table
```

### *#/% first-generation (Current CT HS Student AND Onboarding):

```python
first_gen_table = df.pivot_table(
    index="First Generation", values="18 Digit ID", aggfunc="count"
)

first_gen_table["% of Total"] = (
    round(
        (first_gen_table["18 Digit ID"] / first_gen_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

first_gen_table
```

### PSAT Data (Current CT HS Student Only):

The average PSAT Math Score was 374.

The average PSAT English score was 339

The average PSAT Total was 713


### Applicants Data:

Number of Applicants: 99


### Ward 8 Residents (Current CT HS Student Only):


```python
ward_8_table = df_current_only.pivot_table(
    index="ward_8_resident", values="18 Digit ID", aggfunc="count"
)

ward_8_table["% of Total"] = (
    round(
        (ward_8_table["18 Digit ID"] / ward_8_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

ward_8_table
```

### Ward 8 Residents  (Current CT HS Student AND Onboarding):


```python
ward_8_table = df.pivot_table(
    index="ward_8_resident", values="18 Digit ID", aggfunc="count"
)

ward_8_table["% of Total"] = (
    round(
        (ward_8_table["18 Digit ID"] / ward_8_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

ward_8_table
```

### School Breakdown (Current CT HS Student Only):

Sorry, the schools are entered into the system as DCPS. We don't have any additional data


```python
school_table = df_current_only.pivot_table(
    index="Current School", values="18 Digit ID", aggfunc="count"
)

school_table["% of Total"] = (
    round(
        (school_table["18 Digit ID"] / school_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

school_table
```

### School Breakdown (Current CT HS Student AND Onboarding):


```python
school_table = df.pivot_table(
    index="Current School", values="18 Digit ID", aggfunc="count"
)

school_table["% of Total"] = (
    round(
        (school_table["18 Digit ID"] / school_table["18 Digit ID"].sum() * 100), 0
    ).astype(str)
    + "%"
)

school_table
```

```python

```
