from __future__ import unicode_literals

from django.db import models

# Create your models here.
# '''
#yahan pe change kiya hai dekhne ke liye 
class Person(models.Model):
	ID = models.AutoField(primary_key=True)
	password = models.CharField(max_length = 20)
	name = models.CharField(max_length = 50)
	email = models.EmailField(unique=True)
	phone = models.BigIntegerField(unique=True)							
	address = models.CharField(max_length = 150, null = True, blank = True)
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
	institute = models.CharField(max_length=200)
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

class PendingFaculty(Person):
	institute = models.CharField(max_length=200)
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
	course_id = models.AutoField(primary_key = True)
	name = models.CharField(max_length = 50)
	syllabus = models.CharField(max_length = 1000)
	credits = models.IntegerField()
	fees = models.IntegerField()
	durationWeeks = models.IntegerField()
	faculty = models.ManyToManyField(Faculty)
	student = models.ManyToManyField(Student, blank=True, null=True)
	pre_requisites = models.ManyToManyField('self', blank=True, null=True)

class Calendar(models.Model):
	course = models.ForeignKey(Course, on_delete = models.CASCADE)
	date = models.DateField()
	content = models.CharField(max_length = 3000, null = True)
	quiz = models.CharField(max_length = 3000, null = True)
	class Meta:
		unique_together = ('course','date')

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
