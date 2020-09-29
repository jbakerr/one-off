import pandas as pd
from simple_salesforce import Salesforce, format_soql
import os
from dotenv import load_dotenv
from ct_snippets.load_sf_class import SF_SOQL, SF_Report
from ct_snippets.sf_bulk import sf_bulk, sf_bulk_handler, generate_data_dict
from reportforce import Reportforce
import numpy as np
import soql_queries as soql
import variables


load_dotenv()


SF_PASS = os.environ.get("SF_PASS")
SF_TOKEN = os.environ.get("SF_TOKEN")
SF_USERNAME = os.environ.get("SF_USERNAME")

sf = Salesforce(username=SF_USERNAME, password=SF_PASS, security_token=SF_TOKEN)
rf = Reportforce(session_id=sf.session_id, instance_url=sf.sf_instance)


# Sample for loading from SOQL
query = """
SELECT Id, DV_Status__c, AY_2019_20_Student_Served__c, toLabel(College_Track_Status__c), SITE__r.Name
FROM Contact
WHERE (AY_2019_20_Student_Served__c != NULL OR College_Track_Status__c IN ('18a','11A','12A','15A', '17A')) AND SITE__c !='0011M00002GdtrEQAR' 
 """
data = SF_SOQL("data", query)
data.load_from_sf_soql(sf)

data.shorten_site_names(site_column="A_SITE__c")

df = data.df.replace({"C_DV_Status__c": np.nan}, "No",)
df = df.replace("Unsure", "No")

df.rename(
    columns={
        "C_DV_Status__c": "Dreamer",
        "C_AY_2019_20_Student_Served__c": "AY2019_20_Student",
        "site_short": "Site",
    },
    inplace=True,
)


def determine_student_type(status):
    if status in (["Onboarding", "Current CT HS Student", "Leave of Absence"]):
        return "High School Student"
    elif status == "Active: Post-Secondary":
        return "Post-Secondary Student"
    elif status == "CT Alumni":
        return "Alumni"
    else:
        return status


df["status"] = df.apply(
    lambda x: determine_student_type(x["C_College_Track_Status__c"]), axis=1
)

df.to_pickle("../data/interim/data.pkl")


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

prev_year_student_type_percent = pd.crosstab(
    [prev_year_df.Site], prev_year_df.Dreamer, normalize="index"
).style.format("{:.0%}")


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

current_year_student_type_percent = pd.crosstab(
    [current_year_df.Site], current_year_df.Dreamer, normalize="index"
).style.format("{:.0%}")


alumni = df[df.status == "Alumni"]


alumni_percent = pd.crosstab([alumni.Site], alumni.Dreamer)


# Sample for saving data

