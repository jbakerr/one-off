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

```python
from helpers import generate_hist_for_region_year
import pandas as pd
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import seaborn as sns

%load_ext autoreload
%autoreload 2
```

# Incoming Cohort GPAs (Combined Years)

### Notes:
* Only for classes of 2019-2022 (when applicable)
* Only included students who had GPA data avaliable in their first year at College Track
* Took the first record of a student's GPA in their 9th grade (defaulted to the Fall semester, but if data for Fall wasn't present, would use Spring data)

```python
%matplotlib inline
```

```python
today = datetime.today()
in_file = "/Users/bakerrenneckar/code/one-off/incoming_cohort_gpa/data/processed/summary_Nov-13-2019.pkl"
report_dir = Path.cwd() / "reports"
```

```python
df = pd.read_pickle(in_file)
```

## Northern California

```python
generate_hist_for_region_year(df, "Northern California", type="combined")
```

## New Orleans

```python
generate_hist_for_region_year(df, "New Orleans", type="combined")
```

## Colorado

```python
generate_hist_for_region_year(df, "Colorado", type="combined")
```

## Los Angeles

```python
generate_hist_for_region_year(df, "Los Angeles", type="combined")
```

## DC

```python
generate_hist_for_region_year(df, "DC", type="combined")
```

```python

```
