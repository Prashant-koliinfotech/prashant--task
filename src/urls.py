
from django.urls import path
from src.views import StudentDetailsAPIView, StudentListAPIView, SubjectAPIView, AverageMarksAPIView
from django.conf.urls.static import  static
from django.conf import settings

urlpatterns = [
    path('student-list/', StudentListAPIView.as_view()),
    path('student-details/<int:pk>/', StudentDetailsAPIView.as_view()),
    path('add-student-marks/', SubjectAPIView.as_view()),
    path('average-marks/', AverageMarksAPIView.as_view()),

]
