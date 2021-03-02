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

students = SF_SOQL("students", soql.student_list)
students.load_from_sf_soql(sf)
students.write_file()

academic_terms = SF_SOQL("academic_terms", soql.academic_term)
academic_terms.load_from_sf_soql(sf)
academic_terms.write_file()

test = SF_SOQL("test", soql.test)
test.load_from_sf_soql(sf)
test.write_file()

mse = SF_SOQL("mse", soql.mse)
mse.load_from_sf_soql(sf)
mse.write_file()


academic_terms.df

academic_term_pivot = academic_terms.df.pivot_table(
    values=[
        "AS_GPA_semester__c",
        "AS_GPA_semester_cumulative__c",
        "AS_Attendance_Rate__c",
    ],
    index="AS_Student__c",
    columns="GAS_Global_Academic_Semester__c",
)

academic_term_pivot.columns = [
    "_".join(col) for col in academic_term_pivot.columns.values
]

academic_term_pivot.rename(
    columns={
        "AS_Attendance_Rate__c_Fall 2020-21 (Semester)": "Fall Attendance",
        "AS_Attendance_Rate__c_Spring 2020-21 (Semester)": "Spring Attendance",
        "AS_GPA_semester__c_Fall 2020-21 (Semester)": "Fall Term GPA",
        "AS_GPA_semester_cumulative__c_Fall 2020-21 (Semester)": "Fall Cum GPA",
    },
    inplace=True,
)

test.df.rename(
    columns={
        "AR_ACT_English": "ACT English",
        "AR_ACT_Math": "ACT Math",
        "AR_ACT_Reading": "ACT Reading",
        "AR_ACT_Composite": "ACT Composite",
    },
    inplace=True,
)

df = students.df.merge(
    academic_term_pivot, left_on="C_Id", right_on="AS_Student__c", how="left"
)

df = df.merge(test.df, left_on="C_Id", right_on="AR_Contact_Name__c", how="left")

df["Participated in Competitive MSE"] = df.apply(
    lambda x: x.C_Id in list(mse.df["SLA_Student__c"]), axis=1
)


df.rename(
    columns={
        "C_Id": "Salesforce ID",
        "C_LastName": "Last Name",
        "C_FirstName": "First Name",
        "C_Current_School__c": "School",
        "C_Email": "Email",
        "C_Total_Community_Service_Hours_Completed__c": "Service Hours (current)",
        "C_Total_Bank_Book_Earnings_current__c": "Bank Book Earned",
        "C_FA_Req_Expected_Financial_Contribution__c": "EFC (Expected Family Contribution) ",
        "C_CoVitality_Scorecard_Color_Most_Recent__c": "Most Recent CoVi Color",
    },
    inplace=True,
)

df.drop(columns="AR_Contact_Name__c", inplace=True)

# Sample for saving data
df.to_csv("../data/processed/student_list.csv", index=False)

df.to_excel("../data/processed/student_list.xlsx")

# Sample for pushing data to SFDC
# data_dict = {"C_Id": "Id"}

# data = generate_data_dict(data.df, data_dict)
# results_df = sf_bulk("Contact", data, sf, batch_size=50, use_serial=True)
# fail_df = process_bulk_results(results_df, data.df)

