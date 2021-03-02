import pandas as pd
from simple_salesforce import Salesforce, format_soql
import os
from dotenv import load_dotenv
from ct_snippets.load_sf_class import SF_SOQL, SF_Report
from ct_snippets.sf_bulk import (
    sf_bulk,
    sf_bulk_handler,
    generate_data_dict,
    process_bulk_results,
)
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
# query = """ """
workshops = SF_SOQL("workshops", soql.workshop_report)
workshops.load_from_sf_soql(sf)
workshops.write_file()


workshops.df["calc_duration"] = workshops.df.apply(
    lambda x: x["C_Duration__c"] / 60, axis=1
)


(
    abs(
        workshops.df["calc_duration"]
        - workshops.df["CA_Formula_Total_Session_Hours__c"]
    )
    > 0.5
).value_counts()

workshops.df.loc[
    (
        abs(
            workshops.df["calc_duration"]
            - workshops.df["CA_Formula_Total_Session_Hours__c"]
        )
        > 0.5
    ),
    "CA_Formula_Total_Session_Hours__c",
] = 1


workshops.df["report_group"] = ""

workshops.df.loc[workshops.df.CA_Outcome__c == "Drop-in", "report_group"] = "Other"


workshops.df.loc[
    workshops.df["CA_Workshop_Dosage_Type__c"].str.contains("Tutoring"), "report_group"
] = "Other"


workshops.df.loc[
    (workshops.df.CA_Outcome__c == "Make Up") & (workshops.df.report_group != "Other"),
    "report_group",
] = "Small Group"

workshops.df.loc[
    (workshops.df.CA_Outcome__c.str.contains("Attended"))
    & (workshops.df.report_group != "Other"),
    "report_group",
] = "Small Group"

workshops.df.loc[
    (workshops.df.CA_Outcome__c == "Tardy") & (workshops.df.report_group != "Other"),
    "report_group",
] = "Small Group"


workshops.df.loc[workshops.df["report_group"] == "", "report_group"] = "Other"


workshop_table = pd.crosstab(
    index=workshops.df.C_HIGH_SCHOOL_GRADUATING_CLASS__c,
    columns=workshops.df.report_group,
    values=workshops.df.CA_Formula_Total_Session_Hours__c,
    aggfunc="sum",
    margins="index",
)

student_table = workshops.df.groupby("C_HIGH_SCHOOL_GRADUATING_CLASS__c")["CA_Student__c"].nunique()




workshop_table.to_excel("../data/processed/sac_literacy_map_data.xlsx",
             sheet_name='Workshop')

student_table.to_excel("../data/processed/sac_literacy_map_data.xlsx",
             sheet_name='student')

```python
workshop_pivot.to_excel(sheet_name="Workshop Details")
student_count_pivot.to_excel(writer, sheet_name="Student Details")

# Sample for saving data
# data.write_file(subfolder="interim", file_type=".pkl")


# Sample for pushing data to SFDC
# data_dict = {"C_Id": "Id"}

# data = generate_data_dict(data.df, data_dict)
# results_df = sf_bulk("Contact", data, sf, batch_size=50, use_serial=True)
# fail_df = process_bulk_results(results_df, data.df)

