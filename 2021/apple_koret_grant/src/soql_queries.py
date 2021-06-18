from simple_salesforce import format_soql
from variables import spring_workshops, fall_workshops


spring_query = format_soql(
    """
SELECT Student__c, Student__r.Name, Workshop_Display_Name__c
FROM Class_Attendance__c
WHERE Attendance_Numerator__c = 1
AND Student__r.College_Track_Status__c = '11A'
AND Academic_Semester__r.Name LIKE '%Spring 2020-21%'
AND Workshop_Display_Name__c IN {spring_workshops}
""",
    spring_workshops=spring_workshops,
)

fall_query = format_soql(
    """
SELECT Student__c, Student__r.Name, Workshop_Display_Name__c
FROM Class_Attendance__c
WHERE Attendance_Numerator__c = 1
AND Student__r.College_Track_Status__c = '11A'
AND Academic_Semester__r.Name LIKE '%Fall 2020-21%'
AND Workshop_Display_Name__c IN {fall_workshops}
""",
    fall_workshops=fall_workshops,
)


mse = """
SELECT Student__c, Student__r.Name
FROM Student_Life_Activity__c
WHERE Student__r.College_Track_Status__c = '11A'
AND STEM__c = TRUE
AND Semester__r.Name LIKE '%Summer 2019-20%'
AND Status__c = 'Approved'
AND Student__r.Region__r.Name LIKE '%Northern California%'

"""
