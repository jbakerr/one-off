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
query = soql.query
data = SF_SOQL("data", query)
data.load_from_sf_soql(sf)

df = data.df.groupby(
    ["BB_Scholarship__c", "RT_RecordType__c", "C_AY_2019_20_Student_Served__c"]
).aggregate({"BB_Amount__c": np.sum, "BB_Student__c": pd.Series.nunique})

df = df.reset_index()

df_sub = df[
    ~(
        (df.RT_RecordType__c == "Scholarship Awards")
        & (df.BB_Scholarship__c == "College Track Emergency Fund")
    )
]

# *total $ in College Track scholarships earned and paid to CO students during the 2019-20 academic year:
grouped_df = df_sub.groupby("RT_RecordType__c").sum().reset_index()
# paid
grouped_df[
    grouped_df.RT_RecordType__c.isin(
        ["Bank Book Disbursements", "Scholarship Awards", "Scholarship Distributions"]
    )
]["BB_Amount__c"].sum()

# earned
grouped_df[
    grouped_df.RT_RecordType__c.isin(
        ["Bank Book Earnings", "Scholarship Awards", "Scholarship Distributions"]
    )
]["BB_Amount__c"].sum()

# *total $ of Bank Book scholarships CO high school students earned during the 2019-20 academic year


# Sample for saving data
# data.write_file(subfolder="interim", file_type=".pkl")

