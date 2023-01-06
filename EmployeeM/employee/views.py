from django.shortcuts import render
from .models import *
# Create your views here.
def index(request):
    return render(request,'index.html')

def registration(request):
    flag=""

    if request.method=="POST":
       firstname = request.POST['firstname']
       lastname = request.POST['lastname']
       empcode = request.POST['empcode']
       email = request.POST['email']
       password= request.POST['password']
       
       try:
        user = User.objects.create_user(first_name=firstname,last_name=lastname,username=email,password=password)
        EmployeeDetail.objects.create(user = user,empcode=empcode)
        return render(request,'emp_login.html')
       except: 
        flag="Yes" 
    return render(request,'emp_registration.html',locals() )

def emp_login(request):
    return render(request,'emp_login.html')

