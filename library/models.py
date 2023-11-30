from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    facultate = models.CharField(max_length=40)
    specializare = models.CharField(max_length=40)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name+'['+str(self.facultate)+']'
    
    @property
    def get_name(self):
        return self.user.first_name
    
    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice= [
        ('educatie', 'Educație'),
        ('divertisment', 'Divertisment'),
        ('benzi desenate', 'Benzi desenate'),
        ('biografie', 'Biografie'),
        ('istorie', 'Istorie'),
        ('roman', 'Roman'),
        ('fantezie', 'Fantezie'),
        ('thriller', 'Thriller'),
        ('romantic', 'Romantic'),
        ('stiinta-fictiune', 'Științifico-fantastic')
    ]
    nume=models.CharField(max_length=30)
    isbn=models.PositiveIntegerField()
    autor=models.CharField(max_length=40)
    categorie=models.CharField(max_length=30,choices=catchoice,default='education')
    def __str__(self):
        return str(self.nume)+"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedBook(models.Model):
    facultate=models.CharField(max_length=30)
    isbn=models.CharField(max_length=30)
    data_emitere=models.DateField(auto_now=True)
    data_expirare=models.DateField(default=get_expiry)
    def __str__(self):
        return self.facultate
    def delete_record(self):
        self.delete()
