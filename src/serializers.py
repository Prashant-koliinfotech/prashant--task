
from ast import Sub
from rest_framework import serializers
from src.models import Student, Subject
from django.db.models import Sum, Avg


class StudentSerializer(serializers.ModelSerializer):
    total_marks = serializers.SerializerMethodField()
    average_marks = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth', 'total_marks', 'average_marks']
    
    def get_total_marks(self, instance):
        total = Subject.objects.filter(student=instance).aggregate(total_marks=Sum('subject_marks'))
        return total['total_marks']

    def get_average_marks(self, instance):
        average_marks = Subject.objects.filter(student=instance).aggregate(average_marks=Avg('subject_marks'))
        return average_marks['average_marks']



class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'student', 'subject_name', 'subject_marks']


class StudentMarksDetailsSerializer(serializers.ModelSerializer):
    marks = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['id', 'email', 'first_name', 'last_name', 'date_of_birth',  'marks']

    def get_marks(self, instance):
        return SubjectSerializer(Subject.objects.filter(student=instance), many=True).data

class AverageMarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('subject_name', 'subject_marks')
    


