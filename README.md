# Student Portal
> Student portal with Testing, Internationalization and Localization made with django framework and JS.

## Table of contents
* [Technologies](#technologies)
* [Setup](#setup)
* [Testing](#testing)
* [Internationalization & Localization](#internationalization & localization)
* [Features](#features)
* [User Credintials](#User-Credintials)
* [TODO](#TODO)

## Technologies
* Python 3.9
* Django 2.2.19
* Ajax
* JQuery

## Setup
The first thing to do is to clone the repository:  
`$ git clone https://github.com/OmarFateh/Student-Portal.git`  
Setup project environment with virtualenv and pip.  
`$ virtualenv project-env`  
Activate the virtual environment  
`$ source project-env/Scripts/activate`  
Install all dependencies  
`$ pip install -r requirements.txt`  
Run the server  
`py manage.py runserver`

## Testing
* django unit testing:  
              - accounts app (forms, models, and views)     
              - classroom app (forms, models, and views)   

* pytest & factoryboy:  
              - question app (forms, models, and views)  
              - module app (models)  

## Internationalization & Localization
* Two languages, English & Spanish:      
                        - classroom app  


## Features
* Authentication: Registeration, login, logout, account activation, change and reset password. 

* Teacher:  
      - add/update/delete course  
      - add course's modules  
      - add quiz, page, and assignment to each module.  
      - grade the submitted quiz and assignment.  
      - add question  
      - add answer  
      - vote up/down answer  
      - mark answer as the correct one  

* Student:  
      - enrol to a course   
      - view all course's module   
      - solve course's quizzes  
      - submit assignment  
      - view his course's grade and submissions  
      - add question  
      - add answer  
      - vote up/down answer  
      - mark answer as the correct one for his question  

## User Credintials
- email: fatehomar1@gmail.com  
- password: admin1600
