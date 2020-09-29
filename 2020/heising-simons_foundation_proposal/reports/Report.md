---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.2
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Heising-Simons Proposal Data

```python
%load_ext autoreload
%autoreload 2
```

```python
import pandas as pd
from datetime import datetime
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from ct_snippets.load_sf_class import SF_SOQL, SF_Report
warnings.filterwarnings('ignore')

```

```python
%matplotlib inline
```

```python
df = pd.read_pickle("../data/interim/data.pkl")
```

### Breakdown of AY 2019-20 Students Who Are Dreamers - By Student Type

```python
prev_year_df = df[~pd.isna(df.AY2019_20_Student)]


prev_year_student_type = prev_year_df.pivot_table(
    index=["Site", "AY2019_20_Student"],
    columns="Dreamer",
    values="C_Id",
    aggfunc="count",
    dropna=True,
    margins=True,
    fill_value=0,
)
prev_year_student_type
```

### Percent of AY 2019-20 Students Who Are Dreamers

```python
prev_year_student_type_percent = pd.crosstab(
    [prev_year_df.Site], prev_year_df.Dreamer, normalize="index", margins=True
).style.format("{:.0%}")

prev_year_student_type_percent
```

### Current AY Dreamer Breakdown By Student Type

```python
current_year_df = df[df.status.isin(["High School Student", "Post-Secondary Student"])]


current_year_student_type = current_year_df.pivot_table(
    index=["Site", "status"],
    columns="Dreamer",
    values="C_Id",
    aggfunc="count",
    dropna=True,
    margins=True,
    fill_value=0,
)

current_year_student_type

```

### Current Year Dreamer Percentage

```python
current_year_student_type_percent = pd.crosstab(
    [current_year_df.Site], current_year_df.Dreamer, normalize="index", margins=True
).style.format("{:.0%}")

current_year_student_type_percent
```

### Alumni Dreamer Breakdown

```python
alumni = df[df.status == "Alumni"]


alumni_percent = pd.crosstab([alumni.Site], alumni.Dreamer, margins=True)
alumni_percent
```

```html

<script>
$(document).ready(function(){
    window.code_toggle = function() {
        (window.code_shown) ? $('div.input').hide(250) : $('div.input').show(250);
        window.code_shown = !window.code_shown
    }
    if($('body.nbviewer').length) {
        $('<li><a href="javascript:window.code_toggle()" title="Show/Hide Code"><span class="fa fa-code fa-2x menu-icon"></span><span class="menu-text">Show/Hide Code</span></a></li>').appendTo('.navbar-right');
        window.code_shown=false;
        $('div.input').hide();
    }
});
</script>


<style>

div.prompt {display:none}


h1, .h1 {
    font-size: 33px;
    font-family: "Trebuchet MS";
    font-size: 2.5em !important;
    color: #2a7bbd;
}

h2, .h2 {
    font-size: 10px;
    font-family: "Trebuchet MS";
    color: #2a7bbd; 
    
}


h3, .h3 {
    font-size: 10px;
    font-family: "Trebuchet MS";
    color: #5d6063; 
    
}

.rendered_html table {

    font-size: 14px;
}

.output_png {
  display: flex;
  justify-content: center;
}

.cell {
    padding: 0px;
}


</style>
```

```python

```
