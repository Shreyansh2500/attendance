from django.shortcuts import render,redirect,HttpResponse
import calendar
from django.http import HttpResponseRedirect
from calendar import HTMLCalendar
from datetime import datetime
from .models import *
from .models import User

# Create your views here.
def home(request):
    #now=datetime.now()
    #get current time
    #time=now.strftime('%H:%M:%S')
    return render(request,"base.html")

def decision(request,leaveId,status):
    approval = Leave.objects.all().filter(id=leaveId).first()
    if status:
        approval.Pending_Status="Approved"
    elif status==0:
        approval.Pending_Status="Rejected"
    approval.Approved = request.user    
    approval.save()  
    return redirect('/approval/')   

def approval(request):
    approvals = Leave.objects.all().filter(Pending_Status="Pending").order_by('-Start_date')
    return render(request,"approval.html",{'approvals':approvals})

def dashboard(request):
    year=datetime.now().year
    month=datetime.now().strftime('%B')
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    val = calendar.month(year, month_number)
    return render(request,"dashboard.html",{'cal':val})

def find_leaves(user):
    return Leave.objects.filter(Employee_name=user).order_by('-Start_date')
    

def history(request):
    if request.user.is_authenticated:
        leaves = find_leaves(request.user)
        #print(request.user.id)
        #records = Record.objects.all().filter(Employee_name=request.user,Date=str("2023-01-13")).first()
        #print(records)
        #print(records.time_worked())
        #records.save()
        #print(records)
        return render(request,"history.html",{'leaves':leaves})
    return HttpResponse(request,"Not Found")


def record(request):
    return render(request,"record.html")

def request(request):
    if request.method=="POST":
        #data = request.POST
        type = request.POST.get("type")
        s_date = request.POST.get("s_date")
        e_date = request.POST.get("e_date")
        reason = request.POST.get("reason")        
        print(s_date)
        print(type)
        Leave.objects.create(Employee_name = request.user,Start_date = s_date,End_date=e_date,Type = type,Reason=reason)
        return redirect("/history/")
    return render(request, "request.html")        

