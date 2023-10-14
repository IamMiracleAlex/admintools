from django.db import models

class TestSetup(models.Model): 
    created = models.DateField(auto_now = True)

class TestInProgress(models.Model): 
    created = models.DateField(auto_now = True)

class TestResult(models.Model): 
    created = models.DateField(auto_now = True)