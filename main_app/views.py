from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):

    return render(request,"index.html")

def register(request):
        errors = User.objects.user_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
            return redirect("/")
        else:
            first_name = request.POST["fname"]
            last_name = request.POST["lname"]
            Email = request.POST["email"]
            Password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name=first_name,last_name=last_name, email=Email, password=Password)
            request.session['uid'] = new_user.id
            request.session['fname'] = new_user.first_name


            return redirect("/")

def login_page(request):
    return render(request, 'index.html')

def login_process(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/login')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['uid'] = user.id
        request.session['fname'] = user.first_name

        return redirect('/dashboard')

def clear(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    context={
        "this_user":User.objects.get(id=request.session['uid']),
        "all_qoute":Quote.objects.all(),
        "all_user":User.objects.all()

    }
    return render(request,'dashboard.html',context)

def edit_account(request,id):
    context={
        "this_user":User.objects.get(id=id),
    }
    return render(request,'edit_account.html',context)

def updated_account(request,id):
    this_user = User.objects.get(id=id)

    errors = User.objects.update_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect(f"/edit_account/{this_user.id}")
    else:
        this_user.first_name=request.POST['f_name']
        this_user.last_name=request.POST['l_name']
        this_user.email=request.POST['Email']
        this_user.save()

    return redirect('/dashboard')

def add_quote(request):
    this_user = User.objects.get(id=request.session['uid'])

    errors = User.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/dashboard')

    else:
        all_qoute=Quote.objects.all()
        Quote.objects.create(
            Author=request.POST['Author'],
            quote=request.POST['quote'],
            poster=User.objects.get(id=request.session['uid'])
            )
        return redirect('/dashboard')

def view_account(request,id):
    context={
        'Poster':User.objects.get(id=id),
        'Quote':Quote.objects.all()
    }
    return render(request,'view_account.html',context)

def delete(request,id):
    this_quote=Quote.objects.get(id=id)
    this_quote.delete()
    return redirect('/dashboard')