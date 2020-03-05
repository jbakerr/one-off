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

# FY20 United Way of Southeast Louisiana (UWSELA) Interim Report Data

```python
import pandas as pd
from pathlib import Path
from datetime import datetime
import numpy as np



in_file = Path.cwd() / "data" / "processed" / "processed_data.pkl"
df = pd.read_pickle(in_file)
```


```python
df["Income"] = (
    df["Annual household income"]
    .replace({"\$": "", ",": "", "-": 0}, regex=True)
    .astype(float)
)
```

```python
def create_income_bucket(value):
    if value < 11872:
        return "Less than or equal to 30% of Median Income"
    elif value < 19392:
        return "Between 30% of 50% of Median Income"
    elif value < 31265:
        return "Between 51% and 80% of Median Income"
    else:
        return "Greater than 80% of Median Income"
```

```python
df["Income Bucket"] = df.apply(lambda x: create_income_bucket(x["Income"]), axis=1)
```

```python
df["GPA (Prev Term CGPA)"] = pd.to_numeric(df["GPA (Prev Term CGPA)"], errors="coerce")
```

```python
senior_df = df[df["High School Class"] == 2020]
```

```python
hs_df = df[df["Contact Record Type"] == "Student: High School"]
```

## Follow up Questions
- Questions that were added on after the ticket was originally submitted.

<!-- #region -->
### *% of freshmen and sophomores required to attend MathBlast who complete the 3-5 weeks


10 students didn't attend more than 80% of their classes, out of 46 students who were enrolled in Math Blast over the 2019 Summer.

10 / 46 = 21%


<!-- #endregion -->

### *% of juniors who successfully complete recommended dual enrollment classes

I confirmed, we don't currently have a method to track this.


### *% of rising seniors who complete "College Prep Institute" to prepare for matriculation

This workshop is completed during the spring for rising seniors. We will have updated data for class of 2021 students at the end of the Spring 2019-20 semster.



### *average # of four-year colleges to which high school seniors apply


```python
np.mean(senior_df["# Four Year College Applications"])
```

### *# of community service hours high school seniors complete throughout high school

Can you give me the average # of hours and the cumulative # of hours class of 2020 seniors have completed as a group?


#### Total Hours for Class of 2020

```python
sum(senior_df["Community Service Hours"])
```

#### Average Hours for Class of 2020

```python
np.mean(senior_df["Community Service Hours"])
```

### *% and # of NOLA high school students with at least a 3.0 GPA during the reporting period
--you gave me % of NOLA high school and college students with 3.0+ GPAs

The first table is the count, the second table is the percent

```python
(hs_df["GPA (Prev Term CGPA)"] >= 3).value_counts(normalize=False)
```

```python
(hs_df["GPA (Prev Term CGPA)"] >= 3).value_counts(normalize=True)
```

### *# of class of 2020 NOLA seniors who have received at least one four-year college acceptance
--you gave me the % already

```python
(senior_df["# Four Year College Acceptances"] > 0).value_counts(normalize=False)
```

### *# of class of 2020 NOLA seniors woh have submitted, completed, or are in the "review" phase with FAFSA

```python
senior_df["FA Req: FAFSA/Alternative Financial Aid"].value_counts(normalize=False)
```

## Original Questions


### Count of unduplicated participants during the above timeframe

This number is lower than the FY19 number because NOLA is a 9th grade recuitment site. Thus this only encompases 10th - College aged students who were active in Fall 2019-20.


```python
len(df)
```

### Breakdown of above unduplicated participants by age and sex (example: Male - Youth 6-17).

```python
df.pivot_table(
    index=["Age"],
    aggfunc="count",
    columns="Gender",
    values="18 Digit ID",
    fill_value=0,
    margins=True,
)
```

### Count of unduplicated participants by sex and parish of residence

```python
df.pivot_table(
    index="Parish",
    aggfunc="count",
    columns="Gender",
    values="18 Digit ID",
    fill_value=0,
    margins=True,
)
```

### Count of unduplicated participants by sex and race/ethnicity (example: Male - African American)

```python
df.pivot_table(
    index=["Ethnic background"],
    aggfunc="count",
    columns="Gender",
    values="18 Digit ID",
    fill_value=0,
    margins=True,
)
```

### They also require a breakdown of "Client Type of Household,"

For this, we don't track if a student is head of a household, so by default all options are "Other"

### Count of unduplicated participants by sex and Employment Status



```python
df.pivot_table(
    index=["Employment Status"],
    aggfunc="count",
    columns="Gender",
    values="18 Digit ID",
    fill_value=0,
    margins=True,
)
```

### Count of unduplicated participants based on household income
For median household income I used: $39,576 taken from:

https://www.census.gov/quickfacts/fact/table/neworleanscitylouisiana/INC110218

Using that number would create the following buckets:

* Less than or equal to 30% of median income: $11,872.8

* 30% to 49%: $19,392.24

* 50% to 79%: $31,265.04

* Greater than 80%: anything above $31,265.04



```python
df["Income Bucket"].value_counts()
```

### % of seniors (class of 2020) who have completed at least 100 hours of community service over their high school careers to date

The second table is students who are above 80 hours, used as a proxy to see if they are "on track." 80 was somewhat taken at random, I can replace it with any number if you think there is a better one

```python
(senior_df["Community Service Hours"] >= 100).value_counts(normalize=True)
```

```python
(senior_df["Community Service Hours"] >= 80).value_counts(normalize=True)
```

### % of students with at least 3.0 cumulative GPA (according to most recent data available)

Note, this includes college students

```python
(df["GPA (Prev Term CGPA)"] >= 3).value_counts(normalize=True)
```

### four-year college acceptance rate
--do we have the ability to estimate four-year eligibility for class of 2020 seniors?

Not any way I know of how to do it accurately, in theory it should be near or exactly 100%, but I don't think we have a good way to determine that.

The table below shows the percent of current seniors who have already been accepted into a 4 year program

```python
(senior_df["# Four Year College Acceptances"] > 0).value_counts(normalize=True)
```

### four-year college matriculation rate
--since fall 2019 is the beginning of the 2019-20 academic year, I think I can use the DDT Fall 2019 for this. Please confirm whether you think this is correct.

Yep, that sounds right


### FAFSA completion rate (for seniors eligible for federal student aid)
--do we have a way to estimate whether class of 2020 seniors are "on track" for this by the end of the school year?

Sort of, the table below shows the percent of seniors with the following FAFSA statuses. So the students with Complete and Reviewed would be "on-track" to complete it, but they haven't submitted yet.

```python
senior_df["FA Req: FAFSA/Alternative Financial Aid"].value_counts(normalize=True)
```

### % of high school seniors (class of 2020) that have applied to at least 6 colleges to date

```python
(senior_df["# Four Year College Applications"] >= 6).value_counts(normalize=True)
```

### % of high school seniors (class of 2020) on track to graduate high school

This should be 100%


### % of 2019-20 high school students promoted to the next grade (from the 2018-19 academic year)

This is also 100%


### % of seniors (class of 2020) on track for TOPS Opportunity eligibility

Using a minimum ACT of 20 and GPA of 2.5


```python
(
    (senior_df["GPA (Prev Term CGPA)"] >= 2.5)
    & (senior_df["ACT Superscore (highest official)"] >= 20)
).value_counts(normalize=True)
```

```python
senior_df["Region Specific Funding Eligibility"].value_counts()
```

### *avg. # of outside scholarship applications high school seniors (class of 2020) have submitted so far

Sadly, this is 0, for all class of 2020 students


### % of high school seniors (class of 2020) who attended at least one college affordability workshop

As I think we discussed on a previous ticket, we don't have a college affordability category, however every senior has attend a college completion - which often includes a college affordability component.



### *% of students receiving at least 5 hours of mentoring, enrichment and/or tutoring instruction per week.

We don't have a quick way to track hours per week, so I took a sum of student's hours over the semester and divided it by 12 program weeks. Only one student is even close to hitting a 5 hours / week mark, with most students only at around 20 total hours. This makes sense, because given our program model only the most extreme case a student would be required to attend 5-6 sessions a week, and often those students have a high absenteeism rate.

