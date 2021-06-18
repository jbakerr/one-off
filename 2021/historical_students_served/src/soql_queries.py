historical_students = """
SELECT Academic_Year__r.Name, student_audit_status__c, COUNT(Id) student_count
FROM Academic_Semester__c
WHERE Term__c = 'Spring'
AND student_audit_status__c IN ('Current CT HS Student', 'Leave of Absence', 'Active: Post-Secondary')
AND End_Date__c >= 2014-06-30 AND End_Date__c <= 2020-09-01
GROUP BY Academic_Year__r.Name, student_audit_status__c
"""


alumni = """
SELECT Contact_4_Year_Degree_Earned_AT_Lookup__r.Academic_Year__r.Name, COUNT(Id) student_count
FROM Contact
WHERE Contact_4_Year_Degree_Earned_AT_Lookup__r.Academic_Year__r.Start_Date__c >= 2013-09-01 AND 
Contact_4_Year_Degree_Earned_AT_Lookup__r.Academic_Year__r.Start_Date__c < 2021-09-01
GROUP BY Contact_4_Year_Degree_Earned_AT_Lookup__r.Academic_Year__r.Name
"""