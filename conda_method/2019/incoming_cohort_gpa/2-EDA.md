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

## Incoming Cohort GPA

Looking at the distrobutions of incoming cohort's gpa for the past 4 FYS.

This notebook contains basic statistical analysis and visualization of the data.

### Data Sources
- summary : Processed file from notebook 1-Data_Prep

### Changes
- 11-13-2019 : Started project

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import seaborn as sns
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

### Perform Data Analysis

```python
df.head()
```

```python
def generate_hist(df, subset):

    colors = ["tab:red", "tab:blue", "tab:green", "tab:pink", "tab:olive"]

    sites = df["Site"].unique()

    fig, axes = plt.subplots(
        1, 4, figsize=(13, 3.75), dpi=100, sharex=True, sharey=True
    )

    for i, (ax, year) in enumerate(
        zip(axes.flatten(), sorted(df["High School Class"].unique()))
    ):

        x = df.loc[(df["High School Class"] == year), "GPA (Term)"]
        mu = x.mean()
        sigma = x.std()
        ax.hist(
            x,
            alpha=0.5,
            bins=20,
            density=False,
            stacked=True,
            label=str(year),
            color=colors[i],
        )
        ax.set_title(
            "Class of "
            + str(year)
            + "\n $\mu={mu:.2f}$, $\sigma={sigma:.2f}$".format(mu=mu, sigma=sigma),
            fontsize=16,
        )

    plt.suptitle(
        "Histogram of {subset}'s Incoming Cohort GPAs".format(subset=subset),
        y=1.15,
        size=16,
    )
    plt.tight_layout()

    for ax in axes.flat:
        ax.set_xlabel("GPA", fontsize=14)
        ax.set_ylabel("Count of Students", fontsize=14)

    for ax in axes.flat:
        ax.label_outer()
```

```python
def generate_hist_for_region(df, region):
    subset = region
    _df = df[df["Region"] == region]
    generate_hist(_df, subset=region)
    for site in _df.Site.unique():
        site_df = _df[_df.Site == site]
        generate_hist(site_df, subset=site)
```

```python
generate_hist_for_region(df, "College Track Northern California Region")
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

```python

```
