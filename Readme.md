## Hello I'm Prashant Sonar submitting this repo as per my best knowledge to be get considerable for the practical assingment Please follow the below steps to setup this project

## clone the project using
git clone 

## Create the .env using 
copy .env.example and rename with .env

## Create the virtaulenv using 
virtualenv env

## install requirements using below command
pip install -r requirements.txt

## make migration using
python manage.py makemigrations

## create database tables using
python manage.py migrate

## Run server using
python manage.py runserver