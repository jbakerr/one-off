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

<!-- #region -->
### Incoming Cohort's GPAs


#### Notes on Methodology:
* Only for classes of 2019-2022 (when applicable to a specific site)
* Only included students who had GPA data avaliable in their first year at College Track
* Took the first record of a student's GPA in their 9th grade (defaulted to the Fall semester, but if data for Fall wasn't present, would use Spring data)
* For student who had 8th grade GPA, it was not included due to data consistency issues and the presence of 9th grade GPAs for these students.
<!-- #endregion -->

```python
from helpers import generate_all_charts, generate_bar_grade_bucket
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

```python
%matplotlib inline
```

```python
today = datetime.today()
in_file = "/Users/bakerrenneckar/code/one-off/incoming_cohort_gpa/data/processed/summary_Nov-15-2019.pkl"
report_dir = Path.cwd() / "reports"
```

```python
df = pd.read_pickle(in_file)
```

```python
generate_bar_grade_bucket(df, subset="College Track", style="bold")
```

```python
generate_all_charts(df, "Northern California", type="bucket")
```

```python
generate_all_charts(df, "New Orleans", type="bucket")
```

```python
generate_all_charts(df, "Colorado", type="bucket")
```

```python
generate_all_charts(df, "Los Angeles", type="bucket")
```

```python
generate_all_charts(df, "DC", type="bucket")
```

```python

```
