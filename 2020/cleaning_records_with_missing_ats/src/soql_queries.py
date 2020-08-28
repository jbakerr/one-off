student_life = """
SELECT Id, 
Student__c,
Semester__r.Global_Academic_Semester__r.Name, 
Semester__r.Academic_Year__r.Name, 
Start_Date__c, 
End_Date__c
FROM Student_Life_Activity__c
WHERE Semester__c = NULL 
AND Student__r.SITE__c != '0011M00002GdtrEQAR'
"""


bank_book = """
SELECT Id, Student__c,
	Academic_Semester__r.Global_Academic_Semester__r.Name, Academic_Year__c, Date__c
FROM Bank_Book__c
WHERE Scholarship_Application__r.RecordType.Name = 'Bank Book'
AND Academic_Semester__c = NULL AND Student__r.SITE__c != '0011M00002GdtrEQAR'
"""


scholarships = """
SELECT Id,
Student__c, 
Academic_Year__r.Name,
Date_Applied_date__c, 
Status__c, 
Amount_Awarded__c, 
RecordType.Name,
High_School_Class__c,
HS_Grade__c
FROM Scholarship_Application__c
WHERE RecordType.Name IN ('External', 'Internal', 'DOOR')
AND Academic_Year__c = NULL
AND Student__r.SITE__C != '0011M00002GdtrEQAR'
"""


academic_terms = """
SELECT Id, 
Start_Date__c, 
End_Date__c,
Global_Academic_Semester__r.Name, 
Student__c, 
Academic_Year__c
FROM Academic_Semester__c
"""
