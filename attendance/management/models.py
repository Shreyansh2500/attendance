from django.db import models
from django.contrib.auth.models import User
import numpy as np
#from datetime import datetime
import datetime

class Leave(models.Model):
    Employee_name = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='employee')
    Start_date = models.DateField('start-date')
    End_date = models.DateField('end-date')
    No_of_Days = models.IntegerField('no-of-days',blank=True,null=True)
    Reason = models.TextField('reason',blank=True,null=True)
    Approved = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,related_name='manager')
    #'approved',max_length=20
    LEAVE_CHOICES = (
        ('Personal', 'Personal'),
        ('Medical', 'Medical'),
    )
    Type = models.CharField(max_length=10,choices=LEAVE_CHOICES)
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected','Rejected')
    )
    Pending_Status = models.CharField(max_length=25,choices=STATUS_CHOICES,default="Pending",blank=True,null=True)

    def __str__(self):
      return self.Employee_name.first_name +' '+self.Employee_name.last_name+'-'+str(self.Start_date)+'-'+str(self.End_date)

    def save(self,*args,**kwargs):
        try:
            year,month,day = self.End_date.split("-")
            last_day = datetime.date(int(year),int(month),int(day)+1)
            days = np.busday_count(self.Start_date,last_day)
            self.No_of_Days=days
        except:
            pass
        super().save(*args,**kwargs)    
  

class Record(models.Model):
    Employee_name = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    Date = models.DateField('date')
    Day = models.IntegerField('day')
    Month = models.IntegerField('month')
    Year = models.IntegerField('year')
    Access_time = models.TimeField('access-time')
    Logout_time = models.TimeField('logout-time')
    Modified_time = models.TimeField('modified-time')
    Time_worked = models.FloatField('time-worked',blank=True,null=True)

    def __str__(self):
        return str(self.Date)+'-'+self.Employee_name.first_name +' '+self.Employee_name.last_name
    
    def time_worked(self):
        time_hr = (self.Logout_time.hour-self.Modified_time.hour)+(self.Modified_time.hour-self.Access_time.hour)
        time_min = (self.Logout_time.minute-self.Modified_time.minute)+(self.Modified_time.minute-self.Access_time.minute)
        time_w = time_hr + (time_min/60)
        return time_w

    def save(self,*args,**kwargs):
        self.Time_worked=self.time_worked()
        super().save(*args,**kwargs)    



    

