hs_students = """
SELECT 
Id,
Full_Name__c, 
Email, 
Site__r.Name,
HIGH_SCHOOL_GRADUATING_CLASS__c,
Total_Bank_Book_Balance_contact__c,
Total_Bank_Book_Earnings_current__c,
BB_Disbursements_total__c,
ACT_Highest_Composite_official__c,
ACT_Highest_Composite_Single_Sitting__c,
ACT_Superscore_highest_official__c,
ACT_Math_highest_Official__c,
ACT_Science_highest_official__c,
ACT_English_highest_official__c,
ACT_Reading_highest_official__c,
ACT_Writing_highest_official__c,
SAT_Highest_Total_single_sitting__c,
SAT_Math_highest_official__c,
SAT_Reading_Writing_highest_official__c,
SAT_SuperScore_Official__c,
GPA_Cumulative__c,
FA_Req_Annual_Adjusted_Gross_Income__c,
FA_Req_CA_Dreamer_Application__c,
FA_Req_EFC_Source__c,
FA_Req_Expected_financial_Contribution__c,
FA_Req_FAFSA__c,
FA_Req_Guardian_has_FSA_ID__c,
FA_Req_State_Financial_Aid_Process_Comp__c,
FA_Req_Student_has_FSA_ID__c,
Citizen_c__c,
Student_Starting_Grade__c,
Ethnic_Background__c,
Gender__c
FROM Contact
WHERE College_Track_Status__c IN ('11A' , '12A') AND HIGH_SCHOOL_GRADUATING_CLASS__c = '2021'
AND Site__r.Name != 'College Track Arlen'

"""


ps_students = """
SELECT 
Id,
Full_Name__c, 
Email, 
Site__r.Name,
HIGH_SCHOOL_GRADUATING_CLASS__c,
Total_Bank_Book_Balance_contact__c,
Total_Bank_Book_Earnings_current__c,
BB_Disbursements_total__c,
ACT_Highest_Composite_official__c,
ACT_Highest_Composite_Single_Sitting__c,
ACT_Superscore_highest_official__c,
ACT_Math_highest_Official__c,
ACT_Science_highest_official__c,
ACT_English_highest_official__c,
ACT_Reading_highest_official__c,
ACT_Writing_highest_official__c,
SAT_Highest_Total_single_sitting__c,
SAT_Math_highest_official__c,
SAT_Reading_Writing_highest_official__c,
SAT_SuperScore_Official__c,
GPA_Cumulative__c,
FA_Req_Annual_Adjusted_Gross_Income__c,
FA_Req_CA_Dreamer_Application__c,
FA_Req_EFC_Source__c,
FA_Req_Expected_financial_Contribution__c,
FA_Req_FAFSA__c,
FA_Req_Guardian_has_FSA_ID__c,
FA_Req_State_Financial_Aid_Process_Comp__c,
FA_Req_Student_has_FSA_ID__c,
Citizen_c__c,
Student_Starting_Grade__c,
Anticipated_Date_of_Graduation_4_Year__r.Name,
Current_School__c,
Current_School_Type__c,
toLabel(College_Track_Status__c),
Current_Enrollment_Status__c,
Indicator_Years_Since_HS_Graduation__c,
Anticipated_Date_of_Transfer__r.Name,
Current_CC_Advisor2__c,
STATESTUDENTID__c,
Ethnic_Background__c,
Gender__c
FROM Contact
WHERE College_Track_Status__c IN ('15A', '16A')
AND Site__r.Name != 'College Track Arlen'

"""

scholarship_query = """

SELECT 
Id, 
Amount__c, 
Scholarship__c, 
Scholarship_Application__c, 
Student__c

FROM Bank_Book__c
WHERE Scholarship__c IN ('DOOR', 'College Track Emergency Fund') AND
 RecordType.Name = 'Scholarship Distributions' AND 
Date__c < 2021-06-30 AND 
DATE__c >= 2020-07-01
"""

