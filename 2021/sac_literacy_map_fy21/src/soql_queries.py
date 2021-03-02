workshop_report = """
SELECT 
	Id, 
	Student__c, 
	Student__r.HIGH_SCHOOL_GRADUATING_CLASS__c, 
	Formula_Total_Session_Hours__c, 
	Workshop_Dosage_Type__c, 
	Workshop_Department__c, 
	Class_Session__r.Class__r.Duration__c,
	Outcome__c
FROM Class_Attendance__c
WHERE Student__r.SITE__r.Name = 'College Track Sacramento' AND 
Workshop_Global_Academic_Year__c = 'AY 2019-20' AND 
Attendance_Numerator__c = 1 AND 
Workshop_Department__c IN ('College Completion', 'Academic Affairs')
"""