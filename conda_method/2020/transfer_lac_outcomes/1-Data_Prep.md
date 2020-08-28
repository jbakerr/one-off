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

## transfer_lac_outcomes

For ticket #8571

### Data Sources
- file1 : Link to SF Report
- file2:  Link to SF Report (As Needed)
- file3:  Link to SF Report (As Needed)

### Changes
- 08-17-2020 : Started project

```python
# ALWAYS RUN
# General Setup 

%load_ext dotenv
%dotenv
from simple_salesforce import Salesforce
from salesforce_reporting import Connection, ReportParser
import pandas as pd
from pathlib import Path
from datetime import datetime
import helpers
import os
import numpy as np
from reportforce import Reportforce
from collections import OrderedDict



SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Salesforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)

```

### File Locations

```python

def recursive_walk(od_field: OrderedDict, field_name=None):
    """
    Recursively flattens each row the results of simple salesforce.
    Only works for bottom up queries.
    :param od_field: results returned by simple salesforce (multiple objects)
    :return: returns a flattened list of dictionaries
    """
    d = {}
    for k in od_field.keys():
        if isinstance(od_field[k], OrderedDict) & (k != "attributes"):
            if "attributes" in od_field[k].keys():
                ret_df = recursive_walk(od_field[k], k)
                d = {**d, **ret_df}
        else:
            if k != "attributes":
                obj = "".join(
                    [char for char in od_field["attributes"]["type"] if char.isupper()]
                )
                if field_name:
                    field_name_normalized = field_name.split("__")[0] + "__c"
                    if (
                        field_name.split("__")[0]
                        == od_field["attributes"]["type"].split("__")[0]
                    ):
                        d[f"{obj}_{k}"] = od_field[k]
                    else:
                        d[f"{obj}_{field_name_normalized}"] = od_field[k]

                else:
                    d[f"{obj}_{k}"] = od_field[k]
    return d


def transform_sf_result_set_rec(query_results: OrderedDict):
    """
    Recursively flattens the results of simple salesforce. It needs flattening when  selecting
    multiple objects.
    :param query_results:
    :return:
    """
    data = []
    for res in query_results:
        d = recursive_walk(res)
        data.append(d)
    return data

```

```python
# ALWAYS RUN
today = datetime.today()


in_file1 = Path.cwd() / "data" / "raw" / "sf_output_file1.csv"
summary_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"


in_file2 = Path.cwd() / "data" / "raw" / "sf_output_file2.csv"
summary_file2 = Path.cwd() / "data" / "processed" / "processed_data_file2.pkl"


in_file3 = Path.cwd() / "data" / "raw" / "sf_output_file3.csv"
summary_file3 = Path.cwd() / "data" / "processed" / "processed_data_file3.pkl"


in_file4 = Path.cwd() / "data" / "raw" / "sf_output_file4.csv"
summary_file4 = Path.cwd() / "data" / "processed" / "processed_data_file4.pkl"
```

### Load Report From Salesforce

```python
cc_grad_query = "SELECT Id, SITE__r.Name, Region__r.Name, College_First_Enrolled_School_Type__c, Graduated_4_Year_Degree_6_Years__c, HIGH_SCHOOL_GRADUATING_CLASS__c FROM Contact WHERE Indicator_Completed_CT_HS_Program__c = true AND Indicator_Years_Since_HS_Graduation__c >= 6 AND College_First_Enrolled_School_Type__c = 'Predominantly associate\\'s-degree granting'"
```

```python
cc_grad_df_results = sf.query_all(cc_grad_query)['records']
```

```python
cc_grad_df =  pd.DataFrame(transform_sf_result_set_rec(cc_grad_df_results))
```

```python
cc_grad_df.C_HIGH_SCHOOL_GRADUATING_CLASS__c = cc_grad_df.C_HIGH_SCHOOL_GRADUATING_CLASS__c.astype(int)
```

```python
cc_grad_df[cc_grad_df['C_HIGH_SCHOOL_GRADUATING_CLASS__c']>2010].C_Graduated_4_Year_Degree_6_Years__c.value_counts(normalize=True)
```

```python
cc_grad_df.C_Graduated_4_Year_Degree_6_Years__c.value_counts(normalize=True)
```

```python
cc_grad_df.C_Graduated_4_Year_Degree_6_Years__c.value_counts(normalize=False)
```

```python
cc_grad_df[cc_grad_df.C_Graduated_4_Year_Degree_6_Years__c == True]['C_Id']
```

```python
cc_transfer_query ="""
SELECT Id, Student__c, Student__r.SITE__r.Name, Student__r.Region__r.Name, Student__r.HIGH_SCHOOL_GRADUATING_CLASS__c, Indicator_Years_Since_HS_Grad_to_Date__c, Global_Academic_Semester__r.Name, Enrolled_in_a_4_year_college__c
FROM Academic_Semester__c 
WHERE Student__r.Indicator_Completed_CT_HS_Program__c = true AND Student__r.Indicator_Years_Since_HS_Graduation__c >= 3 AND 
Student__r.College_First_Enrolled_School_Type__c = 'Predominantly associate\\'s-degree granting' AND 
Indicator_Years_Since_HS_Grad_to_Date__c <= 3.5
"""
```

```python
cc_transfer_results = sf.query_all(cc_transfer_query)['records']
```

```python
cc_transfer_df =  pd.DataFrame(transform_sf_result_set_rec(cc_transfer_results))
```

```python
transfered = cc_transfer_df.groupby('AS_Student__c').sum()
```

```python
transfered[transfered.AS_Enrolled_in_a_4_year_college__c >=1].index
```

```python
(cc_transfer_df.groupby('AS_Student__c').sum()['AS_Enrolled_in_a_4_year_college__c'] >= 1).value_counts()
```

```python
cc_transfer_df
```

```python
cc_transfer_df.groupby('AS_Student__c').sum()
```

```python
# Run if downloading report from salesforce
# File 1 
report_id_file1 = "SF_REPORT_ID"
file_1_id_column = '18 Digit ID' # adjust as needed
sf_df = sf.get_report(report_id_file1, id_column=file_1_id_column)



# File 2 (As needed)
# report_id_file2 = "SF_REPORT_ID"
# file_2_id_column = '18 Digit ID' # adjust as needed
# sf_df_file2 =  sf.get_report(report_id_file2, id_column=file_2_id_column)

# File 3 (As needed)
# report_id_file3 = "SF_REPORT_ID"
# file_3_id_column = '18 Digit ID' # adjust as needed
# sf_df_file3 =  sf.get_report(report_id_file3, id_column=file_3_id_column)

```

#### Save report as CSV

```python
# Only run if ran above cell
# File 1
sf_df.to_csv(in_file1, index=False)


# File 2 and 3 (As needed)
# sf_df_file2.to_csv(in_file2, index=False)
# sf_df_file3.to_csv(in_file3, index=False)

```

### Load DF from saved CSV
* Start here if CSV already exist 

```python
# ALWAYS RUN 
# Data Frame for File 1 - if using more than one file, rename df to df_file1
df = pd.read_csv(in_file1)


# Data Frames for File 1 and 2 (As needed)

# df_file2 = pd.read_csv(in_file2)
# df_file3 = pd.read_csv(in_file3)
```

### Data Manipulation

```python
# File 1
df = helpers.shorten_site_names(df)
df = helpers.clean_column_names(df)

# File 2
# df_file2 = helpers.shorten_site_names(df_file2)
# df_file2 = helpers.clean_column_names(df_file2)
```

### Save output file into processed directory

Save a file in the processed directory that is cleaned properly. It will be read in and used later for further analysis.

```python
# Save File 1 Data Frame (Or master df)
df.to_pickle(summary_file)
```
