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
student_life = SF_SOQL("student_life", soql.student_life)
student_life.load_from_sf_soql(sf)
# student_life.write_file()
# student_life.read_file(subfolder="raw", file_type=".csv", file_level="child")
student_life.date_columns = ["SLA_Start_Date__c", "SLA_End_Date__c"]
student_life.adjust_date()

# bank_book = SF_SOQL("bank_book", soql.bank_book)
# bank_book.load_from_sf_soql(sf)
# # bank_book.write_file()
# bank_book.read_file(subfolder="raw", file_type=".csv", file_level="child")
# bank_book.date_columns = ["BB_Date__c"]
# bank_book.adjust_date()


# scholarships = SF_SOQL("scholarships", soql.scholarships)
# scholarships.load_from_sf_soql(sf)
# # scholarships.write_file()
# scholarships.read_file(subfolder="raw", file_type=".csv", file_level="child")
# scholarships.date_columns = ["SA_Date_Applied_date__c"]
# scholarships.adjust_date()


academic_terms = SF_SOQL("academic_terms", soql.academic_terms)
academic_terms.load_from_sf_soql(sf)
# academic_terms.write_file()
academic_terms.read_file(subfolder="raw", file_type=".csv", file_level="child")
academic_terms.date_columns = ["AS_Start_Date__c", "AS_End_Date__c"]
academic_terms.adjust_date()


# Student Life
student_life_merged = student_life.df.merge(
    academic_terms.df, left_on="SLA_Student__c", right_on="AS_Student__c", how="left"
)

student_life_merged = student_life_merged[
    student_life_merged["SLA_Start_Date__c"].between(
        student_life_merged["AS_Start_Date__c"], student_life_merged["AS_End_Date__c"]
    )
]

student_life_merged = student_life_merged.sort_values(
    by=["SLA_Student__c", "AS_Start_Date__c"]
)

df = student_life_merged.drop_duplicates(
    subset=["SLA_Student__c", "SLA_Id"], keep="first"
)

sl = df[df["SLA_Start_Date__c"] > df["AS_Start_Date__c"]]

# student_life_merged.to_csv("../data/processed/student_life.csv")


# # Bank Book
# bank_book_merged = bank_book.df.merge(
#     academic_terms.df, left_on="BB_Student__c", right_on="AS_Student__c", how="left"
# )

# bank_book_merged = bank_book_merged[
#     bank_book_merged["BB_Date__c"].between(
#         bank_book_merged["AS_Start_Date__c"], bank_book_merged["AS_End_Date__c"]
#     )
# ]

# bank_book_merged.to_csv("../data/processed/bank_book.csv")


# Scholarships

scholarships_merged = scholarships.df.merge(
    academic_terms.df,
    left_on=["SA_Student__c", "SA_High_School_Class__c", "SA_HS_Grade__c"],
    right_on=["AS_Student__c", "AS_High_School_Class__c", "AS_Grade__c"],
    how="left",
)

scholarship_subset = scholarships_merged[
    ~pd.isna(scholarships_merged["AS_Academic_Year__c"])
]
scholarship_subset = scholarship_subset.drop_duplicates(
    ["SA_Id", "AS_Academic_Year__c"]
)

# scholarships_merged = scholarships_merged[
#     scholarships_merged["SA_Date_Applied_date__c"].between(
#         scholarships_merged["AS_Start_Date__c"], scholarships_merged["AS_End_Date__c"]
#     )
# ]

scholarship_subset.to_csv("../data/processed/scholarships.csv")

data_dict = {
    "SA_Id": "Id",
    "AS_Academic_Year__c": "Academic_Year__c",
    # "AS_Academic_Year__c": "Academic_Year__c",
}


data = generate_data_dict(scholarship_subset, data_dict)

success_df, fail_df = sf_bulk(
    scholarships_merged, "Scholarship_Application__c", data, sf,
)

