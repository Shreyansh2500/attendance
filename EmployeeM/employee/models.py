from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Table name - EmployeeDetail
class EmployeeDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    empcode = models.CharField(max_length=20)
    contact=models.CharField(max_length=20,null=True)
    joiningDate=models.DateField(null=True)

    def __str__(self):
     return self.user.username


