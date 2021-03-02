student_list = """
SELECT 
	Id, 
	LastName, 
	FirstName,
	Current_School__c,
	Email,
	Total_Community_Service_Hours_Completed__c,
	Total_Bank_Book_Earnings_current__c,
	FA_Req_Expected_Financial_Contribution__c,
	CoVitality_Scorecard_Color_Most_Recent__c

FROM Contact
WHERE SITE__r.Name = 'College Track East Palo Alto' AND 
HIGH_SCHOOL_GRADUATING_CLASS__c = '2022' AND 
College_Track_Status__c = '11A'
"""


academic_term = """
SELECT 
	Id, 
    Student__c,
	Global_Academic_Semester__r.Name,
	GPA_Semester__c,
	GPA_semester_cumulative__c,
	Attendance_Rate__c
	
FROM Academic_Semester__c
WHERE Student__r.SITE__r.Name = 'College Track East Palo Alto' AND 
Student__r.HIGH_SCHOOL_GRADUATING_CLASS__c = '2022' AND 
Student__r.College_Track_Status__c = '11A'
AND Global_Academic_Semester__r.Name IN ('Fall 2020-21 (Semester)', 'Spring 2020-21 (Semester)')
"""

test = """
SELECT 
	Contact_Name__c,	
	MAX(ACT_English__c) ACT_English,
	MAX(ACT_Mathematics__c) ACT_Math,
	MAX(ACT_Reading__c) ACT_Reading,
	MAX(ACT_Composite_Score__c) ACT_Composite
	
FROM Test__c
WHERE Contact_Name__r.SITE__r.Name = 'College Track East Palo Alto' AND 
Contact_Name__r.HIGH_SCHOOL_GRADUATING_CLASS__c = '2022' AND 
Contact_Name__r.College_Track_Status__c = '11A'
GROUP BY Contact_Name__c
"""

mse = """

SELECT 
	Student__c,
	Id,
	Competitive__c

	
FROM Student_Life_Activity__c
WHERE Student__r.SITE__r.Name = 'College Track East Palo Alto' AND 
Student__r.HIGH_SCHOOL_GRADUATING_CLASS__c = '2022' AND 
Student__r.College_Track_Status__c = '11A' AND 
RecordType.Name = 'Summer Experience' 
AND Competitive__c = true

"""
