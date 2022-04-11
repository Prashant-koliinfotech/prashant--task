from functools import partial
from multiprocessing import context
from os import stat
from tokenize import Triple
from wsgiref.simple_server import ServerHandler
from xml.etree.ElementTree import SubElement
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from src.models import Subject, Student
from src.serializers import (StudentSerializer,
    SubjectSerializer, StudentMarksDetailsSerializer, AverageMarksSerializer)
from collections import defaultdict

class StudentListAPIView(APIView):
    """
    Student list Api to add student and get all students with total marks data.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self) :
        return self.queryset.order_by('-id')

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = StudentSerializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student details added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class StudentDetailsAPIView(APIView):
    """
    Student Details Api to get student with its marks details
    and update student data.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self, pk) :
        return self.queryset.filter(pk=pk).first()

    def get(self, request, pk, format=None):
        instance = self.get_queryset(pk)
        if instance:
            serializer = StudentMarksDetailsSerializer(instance)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Student not found with provided pk!"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        instance = self.get_queryset(pk)
        serializer = StudentSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student details updated successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class SubjectAPIView(APIView):
    """
    Subject  Api to add student with its marks details.
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_queryset(self) :
        return self.queryset.order_by('-id')

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = StudentSerializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        student_obj = Student.objects.filter(pk=int(request.data['student'])).first()

        if student_obj:
            serializer = SubjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(student=student_obj)
                return Response({"message": "Student marks added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"Please provide valid student id!"}, status=status.HTTP_400_BAD_REQUEST)

class AverageMarksAPIView(APIView):
    """
    Average Marks Api to get average marks for all the students.
    """
    queryset = Subject.objects.all()
    serializer_class = AverageMarksSerializer

    def get_queryset(self) :
        return self.queryset.order_by('-id')

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = AverageMarksSerializer(queryset, many=True)
        subject_names = []
        for data in queryset:
            if data.subject_name not in subject_names:
                subject_names.append(data.subject_name)
        
        subjects = defaultdict(list)
        for sub_data in serializer.data:
            for i in range(len(subject_names)):
                if sub_data["subject_name"] == subject_names[i]:
                    subjects[sub_data['subject_name']].append(sub_data['subject_marks'])
        new_subjects = []
        total_students = Student.objects.count()
        for key,subject in subjects.items():
            value = sum(subject) / total_students
            new_subjects.append({key:value})
        return Response({"data": new_subjects}, status=status.HTTP_200_OK)