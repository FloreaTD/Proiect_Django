from django import forms
from django.contrib.auth.models import User
from . import models


class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']

class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['facultate','specializare']

class BookForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields=['nume','isbn','autor','categorie']

class IssuedBookForm(forms.Form):
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(), to_field_name="isbn", label='Nume si Isbn')
    
    facultate2 = forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(), to_field_name='facultate', label='Nume si specializare')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(IssuedBookForm, self).__init__(*args, **kwargs)

        if user and user.groups.filter(name='ADMIN').exists():
            # se afiseaza toti studentii daca utilizatorul este admin
            self.fields['facultate2'].queryset = models.StudentExtra.objects.all()
        elif 'facultate2' in self.fields:
            # se afiseaza doar numele studentului daca utilizatorul este student
            self.fields['facultate2'].queryset = models.StudentExtra.objects.filter(user=user)

    
