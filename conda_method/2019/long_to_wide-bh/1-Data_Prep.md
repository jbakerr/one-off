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

## long_to_wide_bq

Request for a long version of all ACT test scores

### Data Sources
- file1 : Description of where this file came from

### Changes
- 11-05-2019 : Started project

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
```

### File Locations

```python
today = datetime.today()
in_file = Path.cwd() / "data" / "raw" / "FILE1"
summary_file = Path.cwd() / "data" / "processed" / f"summary_{today:%b-%d-%Y}.pkl"
```

```python
df = pd.read_csv(in_file)
```

### Column Cleanup

- Remove all leading and trailing spaces
- Rename the columns for consistency.

```python
# https://stackoverflow.com/questions/30763351/removing-space-in-dataframe-python
df.columns = [x.strip() for x in df.columns]
```

```python
cols_to_rename = {"col1": "New_Name"}
df.rename(columns=cols_to_rename, inplace=True)
```

### Clean Up Data Types

```python
df.dtypes
```

### Data Manipulation

```python

```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

Other options besides pickle include:
- feather
- msgpack
- parquet

```python
df.to_pickle(summary_file)
```
