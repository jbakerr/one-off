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

## Site Attendance Average

For ticket 8191

This notebook contains basic statistical analysis and visualization of the data.

### Data Sources
- summary : Processed file from notebook 1-Data_Prep

### Changes
- 06-19-2020 : Started project

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
# warnings.filterwarnings('ignore')

```

```python
%matplotlib inline
%load_ext nb_black
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

```

### Save Excel file into reports directory

Save an Excel file with intermediate results into the report directory

```python
writer = pd.ExcelWriter(report_file, engine='xlsxwriter')
```

```python
df.to_excel(writer, sheet_name='Report')
```

```python
writer.save()
```
