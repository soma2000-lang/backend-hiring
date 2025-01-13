from django.db import models


# Create your models here.
class Site(models.Model):
    RECORD_CAPACITY_LOW = 1  # user records between 500-10000
    RECORD_CAPACITY_MEDIUM = 2  # user records between 10000-50000
    RECORD_CAPACITY_HIGH = 3  # user records between 50000-200000

    RECORD_CAPACITY_CHOICES = (
        (RECORD_CAPACITY_LOW, "Low"),
        (RECORD_CAPACITY_MEDIUM, "Medium"),
        (RECORD_CAPACITY_HIGH, "High"),
    )

    name = models.CharField(max_length=100)
    domain = models.URLField()
    url = models.URLField()
    description = models.TextField()
    record_capicity = models.IntegerField(choices=RECORD_CAPACITY_CHOICES)
    totalusers = models.IntegerField(default=0) #for the job that may be already present in the database
    totaljobs = models.IntegerField(default=0) #for the users that may be already presentin the
    
    def __str__(self):
        return self.name


# you can choose to reuse the User model from django.contrib.auth.models
class UserRecords(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    dob = models.DateField()
    is_active = models.BooleanField(default=True)  # do not count for active records if false
    def __str__(self):
        return self.name
    
class Jobs(models.Model):
    
    Task_1="task1"
    Task_2="task2"
    Task_3="task3"
    Task_4="task4"
    Task_5="task5"
    TASK_CHOICES = (
        (Task_1, 'Task 01'),
        (Task_2, 'Task 02'),
        (Task_3, 'Task 03'),
        (Task_4, 'Task 04'),
        (Task_5, 'Task 05'),
    )
    user=models.ForeignKey(UserRecords,on_delete=models.CASCADE,default=1)
    site=models.ForeignKey(Site,on_delete=models.CASCADE,default=1)
    execution_time=models.FloatField(default=0.0)
    status=models.BooleanField()
    task=models.CharField(max_length=20, choices=TASK_CHOICES,blank=True)
    status = models.CharField(max_length=10 ,default='pending')

    def save(self, *args, **kwargs):
        
        if self.execution_time <= 0.001:
            self.task = self.Task_1
        elif self.execution_time <= 0.01:
            self.task = self.Task_2
        elif self.execution_time <= 0.1:
            self.task = self.Task_3
        elif self.execution_time <= 1:
            self.task = self.Task_4
        elif self.execution_time <= 10:
            self.task = self.Task_5
      
        
        
        super().save(*args, **kwargs)
        def __str__(self):
            return "%s -%s- %s" % (self.user.name, self.pk, self.task)
        
      
    
    
    
