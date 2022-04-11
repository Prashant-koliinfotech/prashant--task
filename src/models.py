from django.db import models
from django.utils.translation import gettext_lazy as _


class Student(models.Model):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')    

class Subject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_marks")
    subject_name = models.CharField(max_length=255)
    subject_marks = models.FloatField(default=0)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.student.first_name +" "+self.student.last_name