query = """
SELECT Student__r.SITE__r.Name, Student__c, Id, RecordType.Name, Amount__c, Scholarship__c, Student__r.HIGH_SCHOOL_GRADUATING_CLASS__c, Student__r.AY_2019_20_Student_Served__c
FROM Bank_Book__c 
WHERE Academic_Semester__r.Academic_Year__r.Name ='AY 2019-20' AND Student__r.Region__r.Name LIKE '%Colorado%' AND Scholarship_Application__r.RecordType.Name IN ('Bank Book', 'DOOR', 'Internal') AND Student__r.AY_2019_20_Student_Served__c != NULL

"""
