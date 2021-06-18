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
sf_data = SF_SOQL("data", soql.historical_students)
sf_data.load_from_sf_soql(sf)
sf_data.write_file()

hs_students = ['Leave of Absence', 'Current CT HS Student']
ps_students = ['Active: Post-Secondary']

sf_data.df[sf_data.df['AR_student_audit_status__c'].isin(hs_students)]['student_type'] = 'HS Student'

def create_student_type(status):
    if status in hs_students:
        return "HS Student"
    else:
        return "PS Student"

sf_data['student_type'] = 
alumni  = SF_SOQL("data", soql.alumni)
alumni.load_from_sf_soql(sf)
alumni.write_file()

alumni.df['student_type'] = "Graduate"

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

#Display the results of the upload
# sf_upload.process_bulk_results()
