import pandas as pd
from simple_salesforce import Salesforce, format_soql
import os
from dotenv import load_dotenv
from ct_snippets.load_sf_class import SF_SOQL, SF_Report
from ct_snippets.sf_bulk import SF_Bulk
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
spring = SF_SOQL("spring", soql.spring_query)
spring.load_from_sf_soql(sf)

fall = SF_SOQL("fall", soql.fall_query)
fall.load_from_sf_soql(sf)

mse = SF_SOQL("mse", soql.mse)
mse.load_from_sf_soql(sf)

df = spring.df.append(fall.df, ignore_index=True)
df = df[["CA_Student__c", "C_Student__c"]]

mse.df.rename(columns={'SLA_Student__c': 'CA_Student__c'},inplace=True)

df = df.append(mse.df,ignore_index=True)

df_unique = df[["CA_Student__c", "C_Student__c"]].drop_duplicates()



df_unique.rename(
    columns={"CA_Student__c": "Id", "C_Student__c": "Full Name"}, inplace=True
)

filename = "../data/processed/" + "student_list" + ".xlsx"
writer = pd.ExcelWriter(filename, engine="xlsxwriter")
df_unique.to_excel(writer, index=False)
workbook = writer.book
worksheet = writer.sheets['Sheet1']


def format_excel(df, workbook, worksheet):

    fmt_header = workbook.add_format(
        {
            "bold": True,
            #  'width': 256,
            "text_wrap": True,
            # "valign": "top",
            "align": "left",
            "fg_color": "#505050",
            "font_color": "#FFFFFF",
            "border": 0,
        }
    )
    for col, value in enumerate(df.columns.values):
        worksheet.write(0, col, value, fmt_header)
    worksheet.set_column(0, len(df.columns), 60)
    writer.save() 

format_excel(df_unique,workbook, worksheet)



# Sample for pushing data to SFDC

# sf_upload = SF_Bulk(sf_data.df)

# sf_upload.data_dict = {
#     "C_Id": "Id",
# }

# sf_upload.generate_data_dict()

# Option to use either segmented uploads or one upload.
# Segmented Uploads:
# sf_upload.process_segmented_upload(5, sf_object="Contact", sf=sf)

# One Upload:
# sf_upload.sf_bulk("Task", sf, bulk_type="insert")

# Display the results of the upload
# sf_upload.process_bulk_results()
