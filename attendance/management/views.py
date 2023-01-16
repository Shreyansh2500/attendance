from django.shortcuts import render,redirect,HttpResponse
import calendar
from django.http import HttpResponseRedirect
from calendar import HTMLCalendar
#from datetime import datetime
import datetime
from .models import *
from .models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import numpy as np
from calendar import monthrange

# Create your views here.
@login_required(login_url='/login')
def home(request):
    #now=datetime.now()
    #get current time
    #time=now.strftime('%H:%M:%S')
    return render(request,"base.html")

@login_required(login_url='/login')
def decision(request,leaveId,status):
    approval = Leave.objects.all().filter(id=leaveId).first()
    if status:
        if approval.Type=="Medical":
            approval.Employee_name.Medical_leave-=approval.No_of_Days
        elif approval.Type=="Personal":
            approval.Employee_name.Personal_leave-=approval.No_of_Days
        approval.Employee_name.save()        
        approval.Pending_Status="Approved"
    elif status==0:
        approval.Pending_Status="Rejected"
    approval.Approved = request.user    
    approval.save()  
    return redirect('/approval/')   

@login_required(login_url='/login')
def approval(request):
    approvals = Leave.objects.all().filter(Pending_Status="Pending").order_by('-Start_date')
    return render(request,"approval.html",{'approvals':approvals})

def calculatePercentage(user,month,year):
    monthRecord = Record.objects.all().filter(Employee_name=user,Month=month,Year=year)
    startdate = datetime.date(year,month,1)
    enddate = datetime.date.today()
    leaveRecord = Leave.objects.all().filter(Employee_name=user,Start_date__range=[startdate,enddate],Pending_Status="Approved")
    
    medicalRecord = leaveRecord.filter(Type="Medical",Pending_Status="Approved")
    PersonalRecord = leaveRecord.filter(Type="Personal",Pending_Status="Approved")
    medical=0
    personal=0
    for i in medicalRecord:
        if i.End_date<=datetime.date.today():
            medical+=i.No_of_Days
        else:
            last_day = datetime.date(int(year),int(month),datetime.date.today().day+1)
            days = np.busday_count(i.Start_date,last_day)
            medical+=days
    for i in PersonalRecord:
        if i.End_date<=datetime.date.today():
            personal+=i.No_of_Days
        else:
            last_day = datetime.date(int(year),int(month),datetime.date.today().day+1)
            days = np.busday_count(i.Start_date,last_day)
            personal+=days
    present=monthRecord.__len__()
    last_day = datetime.date(int(year),int(month),datetime.date.today().day+1)
    saturdayCount=np.busday_count(startdate,last_day,weekmask='Sat')
    sundayCount=np.busday_count(startdate,last_day,weekmask='Sun')
    Holiday = saturdayCount+sundayCount
    absent=datetime.date.today().day - medical - personal - present-Holiday
    return (medical,personal,present,absent,Holiday)
    

def calculateHours(user,month,year,day=datetime.date.today().day):
    monthRecord = Record.objects.all().filter(Employee_name=user,Month=month,Year=year)
    totalHour = 0
    averageHour = 0
    day = monthrange(year,month)[1]
    startdate = datetime.date(year,month,1)
    enddate = datetime.date(year,month,day)
    startweek = int(startdate.strftime("%U"))
    endweek = int(enddate.strftime("%U"))
    weeks = [x for x in range(startweek,endweek+1)]
    print(weeks)
    print(startweek)
    print(endweek)
    weekHour = [0 for x in range(startweek,endweek+1)]

    for hr in monthRecord:
        totalHour+=hr.Time_worked
        curr = int(hr.Date.strftime("%U"))
        currIndex = weeks.index(curr)
        print(currIndex)
        weekHour[currIndex]+=hr.Time_worked

    medical,personal,present,absent,Holiday=calculatePercentage(user,datetime.date.today().month,datetime.date.today().year)
    averageHour = round(totalHour/(present+absent),2)
    totalHour = round(totalHour,2)
    print(weekHour)
    return (totalHour,averageHour,weekHour)    

@login_required(login_url='/login')
def dashboard(request):
    '''
    year=datetime.now().year
    month=datetime.now().strftime('%B')
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(year, month_number)
    val = calendar.month(year, month_number)
    '''
    totalH,averH,weekHour = calculateHours(request.user,datetime.date.today().month,datetime.date.today().year)
    medical,personal,present,absent,Holiday=calculatePercentage(request.user,datetime.date.today().month,datetime.date.today().year)
    return render(request,"dashboard.html",locals())


def find_leaves(user):
    return Leave.objects.filter(Employee_name=user).order_by('-Start_date')
    
@login_required(login_url='/login')
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

@login_required(login_url='/login')
def seekEmployeeRecord(request,Employee_id):
    users = User.objects.all().filter(Manager=False).order_by('-Employee_id')
    currentUser = users.filter(Employee_id=Employee_id).first()
    totalH,averH,weekHour = calculateHours(currentUser,datetime.date.today().month,datetime.date.today().year)
    medical,personal,present,absent,Holiday=calculatePercentage(currentUser,datetime.date.today().month,datetime.date.today().year)
    leaves = find_leaves(currentUser)
    return render(request,"record.html",locals())



@login_required(login_url='/login')
def record(request):
    users = User.objects.all().filter(Manager=False).order_by('-Employee_id')
    currentUser = users.first()
    totalH,averH,weekHour = calculateHours(currentUser,datetime.date.today().month,datetime.date.today().year)
    medical,personal,present,absent,Holiday=calculatePercentage(currentUser,datetime.date.today().month,datetime.date.today().year)
    leaves = find_leaves(currentUser)
    print(leaves)
    return render(request,"record.html",locals())

@login_required(login_url='/login')
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


def loginUser(request):
    if request.method=="POST":
        username = request.POST.get("username")
        print(username)
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user)
            recordExist = Record.objects.all().filter(Employee_name=user,Date=datetime.datetime.today()).first()              
            print(recordExist)
            if recordExist==None:
                Record.objects.create(Employee_name=user)
            else:
                recordExist.Modified_time = recordExist.Logout_time
                recordExist.save() 

            print(recordExist)
            return redirect('/dashboard/')
    return render(request,"login.html")  

@login_required(login_url='/login')
def logoutUser(request):
    try:
        recordExist = Record.objects.all().filter(Employee_name=request.user,Date=datetime.datetime.today()).first()              
        print(recordExist)
        if recordExist:
            recordExist.Logout_time = datetime.datetime.now()
            recordExist.save() 
        logout(request)
    except:
        pass
    return redirect('/login/')     


