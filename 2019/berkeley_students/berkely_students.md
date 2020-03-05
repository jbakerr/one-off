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

```python
import pandas as pd
import numpy as np

students = pd.read_csv("report1571678778407.csv")
ids = pd.read_csv("report1571676878970.csv")
```

```python
ids.head()
```

```python
students["College ID"] = students["18 Digit ID"].map(
    ids.set_index("18 Digit ID")["Student College ID#"].to_dict()
)

# df2['gender'] = df2.userId.map(df1.set_index('userId')['gender'].to_dict())
```


```python
students.to_csv("Berkeley Students.csv")
```

```python

```
