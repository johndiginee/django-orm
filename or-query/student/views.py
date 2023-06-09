from django.shortcuts import render
from .models import Student, Teacher
from django.db import connection
from django.db.models import Q

# Part 2
#################################################################
def student_list_(request):

    posts = Student.objects.all()

    print(posts)
    print(posts.query)
    print(connection.queries)

    return render(request, 'output.html',{'posts':posts})

def student_list_(request):
    posts = Student.objects.filter(surname__startswith='austin') | Student.objects.filter(surname__startswith='baldwin')

    print(posts)
    print(connection.queries)

    return render(request, 'output.html',{'posts':posts})

def student_list(request):
    posts = Student.objects.filter(Q(surname__startswith='austin') | ~Q (surname__startswith='baldwin') | Q (surname__startswith='avery-parker'))

    print(posts)
    print(connection.queries)

    return render(request, 'output.html',{'posts':posts})

# Part 3 
### AND query ##############################################################

def student_list_(request):
    posts = Student.objects.filter(classroom=1) & Student.objects.filter(age=20)

    print(posts)
    print(connection.queries)

    return render(request, 'output.html',{'posts':posts})

# Part 4
### UNION query ##############################################################

def student_list_(request):

    posts = Student.objects.all().values_list("firstname").union(Teacher.objects.all().values_list("firstname"))

    print(posts)
    print(connection.queries)
    return render(request, 'output.html',{'posts':posts})

# Part 5
### NOT query ##############################################################

def student_list_(request):

    posts = Student.objects.exclude(age__gt=20)
    # posts = Student.objects.exclude(age=20) & Student.objects.exclude(firstname__startswith='raquel')

    # gt
    # gte
    # lt
    # lte

    print(posts)
    print(connection.queries)
    return render(request, 'output.html',{'posts':posts})


# Part 6
### Select and Output Individual Fields  ##############################################################

def student_list_(request):

    posts = Student.objects.filter().only('firstname', 'age')

    print(posts)
    print(connection.queries)
    return render(request, 'output.html',{'data':posts})


# Part 7
### Performing Raw SQL Queries  ##############################################################

def student_list_(request):

    # posts = Student.objects.all()

    sql = "SELECT * FROM student_student"
    posts = Student.objects.raw(sql)[:2]

    # for s in Student.objects.raw("SELECT * FROM student_student"): 
    #     print(s)
        

    # print(posts)
    # print(connection.queries)
    return render(request, 'output.html',{'data':posts})


# Part 8
### Bypassing ORM  ##############################################################

def dictfetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
def student_list(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM student_student WHERE age >20")
    r = dictfetchall(cursor)
    
    print(connection.queries)

    return render(request, 'output.html',{'data':r})