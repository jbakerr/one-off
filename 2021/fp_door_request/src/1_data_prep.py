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
# query = """ """
hs_students = SF_SOQL("hs_students", soql.hs_students)
hs_students.load_from_sf_soql(sf)
hs_students.write_file(file_level="child")

ps_students = SF_SOQL("ps_students", soql.ps_students)
ps_students.load_from_sf_soql(sf)
ps_students.write_file(file_level="child")


scholarships = SF_SOQL("scholarships", soql.scholarship_query)
scholarships.load_from_sf_soql(sf)
scholarships.write_file(file_level="child")


scholarships_group = pd.crosstab(
    scholarships.df.BB_Student__c,
    scholarships.df.BB_Scholarship__c,
    values=scholarships.df.BB_Amount__c,
    aggfunc="sum",
)


ps_df = ps_students.df.merge(
    scholarships_group, left_on="C_Id", right_on="BB_Student__c", how="left"
)


def determine_pell(efc):
    if pd.isna(efc):
        return "Missing EFC"
    elif efc >= 5711:
        return "Pell Ineligible"
    elif efc >= 1:
        return "Partial Pell"
    elif efc == 0:
        return "Full Pell"
    else:
        return "Error"


hs_students.df["Pell Bucket"] = hs_students.df.apply(
    lambda x: determine_pell(x["C_FA_Req_Expected_Financial_Contribution__c"]), axis=1
)

ps_df["Pell Bucket"] = ps_df.apply(
    lambda x: determine_pell(x["C_FA_Req_Expected_Financial_Contribution__c"]), axis=1
)


new_hs_columns = {
    "C_Id": "Contact Id",
    "C_Full_Name__c": "Full Name",
    "C_Email": "Email",
    "A_SITE__c": "Site",
    "C_HIGH_SCHOOL_GRADUATING_CLASS__c": "High School Class",
    "C_Total_Bank_Book_Balance_contact__c": "Total Bank Book Balance",
    "C_Total_Bank_Book_Earnings_current__c": "Total Bank Book Earnings (current)",
    "C_BB_Disbursements_total__c": "Total Bank Book Disbursements",
    "C_ACT_Highest_Composite_official__c": "ACT Highest Composite",
    "C_ACT_Highest_Composite_Single_Sitting__c": "ACT Highest Composite (single sitting)",
    "C_ACT_Superscore_highest_official__c": "ACT Superscore (highest official)",
    "C_ACT_Math_highest_official__c": "ACT Math (highest official)",
    "C_ACT_Science_highest_official__c": "ACT Science (highest official)",
    "C_ACT_English_highest_official__c": "ACT English (highest official)",
    "C_ACT_Reading_highest_official__c": "ACT Reading (highest official)",
    "C_ACT_Writing_highest_official__c": "ACT Writing (highest official)",
    "C_SAT_Highest_Total_single_sitting__c": "SAT Highest Total Single Sitting",
    "C_SAT_Math_highest_official__c": "SAT Math (highest official)",
    "C_SAT_Reading_Writing_highest_official__c": "SAT Reading/Writing (highest official)",
    "C_SAT_SuperScore_Official__c": "SAT SuperScore Highest Official",
    "C_GPA_Cumulative__c": "College Elig. GPA (11th CGPA)",
    "C_FA_Req_Annual_Adjusted_Gross_Income__c": "FA Req: Annual Adjusted Gross Income",
    "C_FA_Req_CA_Dreamer_Application__c": "FA Req: CA Dreamer Application",
    "C_FA_Req_EFC_Source__c": "FA Req: EFC Source",
    "C_FA_Req_Expected_Financial_Contribution__c": "FA Req: Exp Financial Contribution (EFC)",
    "C_FA_Req_FAFSA__c": "FA Req: FAFSA/Alternative Financial Aid",
    "C_FA_Req_Guardian_has_FSA_ID__c": "FA Req: Guardian has FSA ID?",
    "C_FA_Req_State_Financial_Aid_Process_Comp__c": "FA Req: State Financial Aid Process Comp",
    "C_FA_Req_Student_has_FSA_ID__c": "FA Req: Student has FSA ID?",
    "C_Citizen_c__c": "Citizen?",
    "C_Student_Starting_Grade__c": "Student Starting Grade",
    "C_Ethnic_background__c": "Ethnic Background",
    "C_Gender__c": "Gender",
}

new_ps_columns = {
    "GAS_Anticipated_Date_of_Graduation_4_Year__c": "Anticipated date of graduation (4 year)",
    "C_Current_School__c": "Current School",
    "C_Current_School_Type__c": "Current School Type",
    "C_College_Track_Status__c": "College Track Status",
    "C_Current_Enrollment_Status__c": "Current Enrollment Status",
    "C_Indicator_Years_Since_HS_Graduation__c": "Years since high school graduation",
    "GAS_Anticipated_Date_of_Transfer__c": "Anticipated date of transfer",
    "College Track Emergency Fund": "Previous year Emergency Fund award (FY21)",
    "DOOR": "Previous year DOOR award (FY21)",
    "C_STATESTUDENTID__c": "College ID",
    "C_Current_CC_Advisor2__c": "Current CC Advisor",
}


hs_df = hs_students.df.rename(columns=new_hs_columns)

ps_df = ps_df.rename(columns=new_hs_columns)

ps_df = ps_df.rename(columns=new_ps_columns)

ps_df.drop(
    columns=[
        "C_Anticipated_Date_of_Transfer__r",
        "C_Anticipated_Date_of_Graduation_4_Year__r",
    ],
    inplace=True,
)


with pd.ExcelWriter("../data/processed/FY22_DOOR_Projections.xlsx") as writer:
    hs_df.to_excel(writer, sheet_name="HS Students", index=False)
    ps_df.to_excel(writer, sheet_name="College Students", index=False)

