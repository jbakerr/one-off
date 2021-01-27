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
# rf = Reportforce(session_id=sf.session_id, instance_url=sf.sf_instance)


# Sample for loading from SOQL
query = """ 
SELECT Id, Student__c, School__r.Name, Grade__c, Student__r.Graduated_4_Year_Degree_6_Years__c, Student__r.Site__r.Name,Student__r.College_First_Enrolled_School__c, Student__r.College_4_Year_Degree_Earned__c, Indicator_Years_Since_HS_Grad_to_Date__c, Student__r.Ind_Start_Graduate_Same_School_6yrs__c, Student__r.GPA_Cumulative__c 
FROM Academic_Semester__c
WHERE Student__r.Indicator_Completed_CT_HS_Program__c = true AND RecordType.Name ='College/University Semester' AND Student__r.Indicator_Years_Since_HS_Graduation__c >= 6 AND Student__r.GPA_Cumulative__c <= 3


"""
data = SF_SOQL("data", query)
data.load_from_sf_soql(sf)


# Group 1 - students who started and finished at same school within 6 years

group_1 = pd.crosstab(
    index=[data.df["A_SITE__c"], data.df["C_College_First_Enrolled_School__c"]],
    columns=data.df["C_Ind_Start_Graduate_Same_School_6yrs__c"],
    values=data.df["AS_Student__c"],
    aggfunc="nunique",
    margins=True,
)

group_1.reset_index().to_csv("../data/processed/grad_rate_same_school.csv")


# Group 2 - Students who started at a given school, but then go on to graduate anywere

group_2 = pd.crosstab(
    index=[data.df["A_SITE__c"], data.df["C_College_First_Enrolled_School__c"]],
    columns=data.df["C_Graduated_4_Year_Degree_6_Years__c"],
    values=data.df["AS_Student__c"],
    aggfunc="nunique",
    margins=True,
)

group_2.reset_index().to_csv("../data/processed/grad_rate_start_any_school.csv")


# Group 3 - Students who attended a given school at least one semester and then graduated - from anywhere

group_3 = pd.crosstab(
    index=[data.df["A_SITE__c"], data.df["A_School__c"]],
    columns=data.df["C_Graduated_4_Year_Degree_6_Years__c"],
    values=data.df["AS_Student__c"],
    aggfunc="nunique",
    margins=True,
)

group_3.reset_index().to_csv("../data/processed/grad_rate_attended_school.csv")

# Group 4 - Students who graduated from a school within 6 years and attended that same school within 6 years
def determine_year_6_status(grad_school, six_year_grad_status, year_six_school):
    if six_year_grad_status == True:
        return grad_school
    else:
        return year_six_school


df_sub = data.df[data.df["AS_Grade__c"] == "Year 6"]

df_sub["year_six_school_or_grad"] = df_sub.apply(
    lambda x: determine_year_6_status(
        x["C_College_4_Year_Degree_Earned__c"],
        x["C_Graduated_4_Year_Degree_6_Years__c"],
        x["A_School__c"],
    ),
    axis=1,
)

group_4 = pd.crosstab(
    index=[df_sub["A_SITE__c"], df_sub["year_six_school_or_grad"]],
    columns=df_sub["C_Graduated_4_Year_Degree_6_Years__c"],
    values=data.df["AS_Student__c"],
    aggfunc="nunique",
    margins=True,
)

group_4.reset_index().to_csv("../data/processed/grad_rate_six_year_school.csv")


# Sample for saving data
# data.write_file(subfolder="interim", file_type=".pkl")

