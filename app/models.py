from __future__ import unicode_literals

from django.db import models

# Create your models here.

'''
Why are we using the is a relationship? Why just not three tables, one for each Student class, Faculty Class and Admin class. 
That is why I have made the Person class as abstract here. It means that a table won't be created for it; It is just the common attributes for the 
three tables. 
'''

'''
No relationship tables added till now.
'''

# '''

class Person(models.Model):
	#ID = models.CharField(max_length = 10,primary_key = True) 	# Like S1, F4, A1 etc if not abstract. If it is abstract, we can make it as integer.
	ID = models.AutoField(primary_key=True)
	password = models.CharField(max_length = 20)
	name = models.CharField(max_length = 50)
	email = models.EmailField(unique=True)
	phone = models.BigIntegerField(unique=True)							
	address = models.CharField(max_length = 150)
	dob = models.DateField()
	class Meta:
		abstract = True

class Student(Person):
	parent_email_id = models.EmailField()
	institute = models.CharField(max_length=200)
	year = models.IntegerField(choices = (
		(1, 'Freshman'),
		(2, 'Sophomore'),
		(3, 'Junior'),
		(4, 'Senior'),
		(5, 'Graduate')
		)
	)
	department = models.CharField(max_length = 2, choices = (
		('AE','Aerospace Engineering'),
		('AG','Agricultural & Food Engineering'),
		('AR','Architecture & Regional Planning'),
		('BT','Biotechnology'),
		('CH','Chemical Engineering'),
		('CY','Chemistry'),
		('CE','Civil Engineering'),
		('CS','Computer Science & Engineering'),
		('EE','Electrical Engineering'),
		('EC','Electronics & Electrical Communication Engineering'),
		('GG','Geology & Geophysics'),
		('HS','Humanities & Social Sciences'),
		('IE','Industrial & Systems Engineering'),
		('MA','Mathematics'),
		('ME','Mechanical Engineering'),
		('MT','Metallurgical & Materials Engineering'),
		('MI','Mining Engineering'),
		('NA','Ocean Engineering & Naval Architecture'),
		('PH','Physics'),
		)
	)


class Faculty(Person):
	department = models.CharField(max_length = 2, choices = (
		('AE','Aerospace Engineering'),
		('AG','Agricultural & Food Engineering'),
		('AR','Architecture & Regional Planning'),
		('BT','Biotechnology'),
		('CH','Chemical Engineering'),
		('CY','Chemistry'),
		('CE','Civil Engineering'),
		('CS','Computer Science & Engineering'),
		('EE','Electrical Engineering'),
		('EC','Electronics & Electrical Communication Engineering'),
		('GG','Geology & Geophysics'),
		('HS','Humanities & Social Sciences'),
		('IE','Industrial & Systems Engineering'),
		('MA','Mathematics'),
		('ME','Mechanical Engineering'),
		('MT','Metallurgical & Materials Engineering'),
		('MI','Mining Engineering'),
		('NA','Ocean Engineering & Naval Architecture'),
		('PH','Physics'),
		)
	)

class Admin(Person):
	# Note : There won't be any requirement of these many details for the admin.
	# So better, we can shift some attributes from Person to Student and Faculty Classes.
	# Or we may also want to remove the abstract class Person completely.
	pass

class Course(models.Model):
	course_id = models.CharField(max_length = 10,primary_key = True) #contains dept and year
	name = models.CharField(max_length = 50)
	syllabus = models.CharField(max_length = 1000)
	credits = models.IntegerField()
	fees = models.IntegerField()
	durationWeeks = models.IntegerField()
	faculty = models.ManyToManyField(Faculty)
	student = models.ManyToManyField(Student)
	pre_requisites = models.ForeignKey('self', on_delete = models.CASCADE)

class Calendar(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	date = models.DateField()
	content = models.CharField(max_length = 3000)
	class Meta:
		unique_together = ('course','date')

class Question(models.Model):
	calendar = models.ForeignKey(Calendar,on_delete=models.CASCADE)
	number = models.IntegerField()
	text = models.CharField(max_length = 500)
	op1 = models.CharField(max_length = 100)
	op2 = models.CharField(max_length = 100)
	op3 = models.CharField(max_length = 100)
	op4 = models.CharField(max_length = 100)
	answer = models.SmallIntegerField(choices = (
		(1,op1),
		(2,op2),
		(3,op3),
		(4,op4),
		)
	)
	# answer = (
	# 	('a',op1),
	# 	('b',op2),
	# 	('c',op3),
	# 	('d',op4),
	# 	)
	class Meta:
		unique_together = ('calendar','number')

class Notif(models.Model):
	notif_from_role =  models.CharField(max_length = 10, choices = (
		('S','Student'),
		('F','Faculty'),
		('A','Admin'),
		)
	)
	
	notif_from_id = models.IntegerField()
	notif_to_role = models.CharField(max_length = 10, choices = (
		('S','Student'),
		('F','Faculty'),
		('A','Admin'),
		)
	)
	notif_to_id = models.IntegerField()
	text = models.CharField(max_length = 1000)
# '''