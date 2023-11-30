from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from . import forms,models
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import date
from .models import StudentExtra


def admin_approval_view(request):
    if not e_admin(request.user):
        return redirect('afterlogin')

    students = StudentExtra.objects.filter(is_approved=False)
    return render(request, 'library/adminapproval.html', {'students': students})


def approve_student_view(request, user_id):
    if not e_admin(request.user):
        return redirect('afterlogin')

    student = StudentExtra.objects.get(user_id=user_id)
    student.is_approved = True
    student.save()

    return redirect('admin_approval')


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')


def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')


def waitingapproval(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('waitingapproval')
    return render(request,'library/waitingapproval.html')


def studentsignup_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            f2.is_approved = False
            user2=f2.save()
            student_group = Group.objects.get_or_create(name='STUDENT')
            student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)


def e_admin(user):
    return user.groups.filter(name='ADMIN').exists()


@login_required(login_url='login')
def afterlogin_view(request):
    try:
        student = StudentExtra.objects.get(user=request.user)
        if student.is_approved:
            return render(request, 'library/studentafterlogin.html')
        else:
            return render(request, 'library/waitingapproval.html')
    except StudentExtra.DoesNotExist:
        return render(request, 'library/adminafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(e_admin)
def addbook_view(request):
    form=forms.BookForm()
    if request.method=='POST':
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})


@login_required(login_url='adminlogin')
@login_required(login_url='studentlogin')
def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})


#@login_required(login_url='adminlogin') || pentru admin
@login_required(login_url='studentlogin')
def issuebook_view(request):
    form = forms.IssuedBookForm(user=request.user)  
    is_admin = request.user.is_authenticated and e_admin(request.user)

    if request.method == 'POST':
        form = forms.IssuedBookForm(request.POST, user=request.user)  

        if form.is_valid():
            obj = models.IssuedBook()
            obj.facultate = form.cleaned_data['facultate2'].facultate  
            obj.isbn = form.cleaned_data['isbn2'].isbn  
            obj.save()
            return render(request, 'library/bookissued.html')

    return render(request, 'library/issuebook.html', {'form': form})



@login_required(login_url='adminlogin')
@user_passes_test(e_admin)
def viewissuedbook_view(request):
    carti_emise = models.IssuedBook.objects.all()
    li = []
    for ce in carti_emise:
        emdate = str(ce.data_emitere.day) + '-' + str(ce.data_emitere.month) + '-' + str(ce.data_emitere.year)
        expdate = str(ce.data_expirare.day) + '-' + str(ce.data_expirare.month) + '-' + str(ce.data_expirare.year)

        carti = list(models.Book.objects.filter(isbn=ce.isbn))
        students = list(models.StudentExtra.objects.filter(facultate=ce.facultate))

        for student, carte in zip(students, carti):
            t = (student.get_name, student.facultate, carte.nume, carte.autor, emdate, expdate)
            li.append(t)
            
    if request.method == 'POST' and 'delete_id' in request.POST:
        delete_id = request.POST['delete_id']
        book_to_delete = get_object_or_404(models.IssuedBook, id=delete_id)
        book_to_delete.delete()
    return render(request, 'library/viewissuedbook.html', {'li': li})


@login_required(login_url='adminlogin')
@user_passes_test(e_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id)
    carti_emise = models.IssuedBook.objects.filter(facultate=student[0].facultate)
    li1 = []
    li2 = []
    for ce in carti_emise:
        carti = models.Book.objects.filter(isbn=ce.isbn)
        for carte in carti:
            t = (request.user, student[0].facultate, student[0].specializare, carte.nume, carte.autor)
            li1.append(t)
        emdate = str(ce.data_emitere.day) + '-' + str(ce.data_emitere.month) + '-' + str(ce.data_emitere.year)
        expdate = str(ce.data_expirare.day) + '-' + str(ce.data_expirare.month) + '-' + str(ce.data_expirare.year)
        
        t = (emdate, expdate)
        li2.append(t)

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})
