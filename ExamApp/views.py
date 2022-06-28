from contextlib import redirect_stderr
from datetime import time, timezone
from time import timezone
import bcrypt
from django.contrib import messages
from django.shortcuts import redirect, render, HttpResponse
from .models import *

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        errors = users.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newUser = users.objects.create(
                fname = request.POST['fname'],
                lname = request.POST['lname'],
                email = request.POST['email'],
                password = hash
            )
            newUser.save()
            request.session['user_id'] = newUser.id
            return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = users.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            request.session['user_id'] = users.objects.get(email=request.POST['email']).id
            return redirect('/wishes')


def home(request):
    if not 'user_id' in request.session:
        return redirect('/')
    else:
        context = {
            'user':users.objects.get(id=request.session['user_id']),
            'wishs':wishs.objects.all(),

        }
        return render(request,'profilePage.html',context)
# def wishes(request):
#     dict={
#         'loggedInUser': users.objects.get(id = request.session['user']),
#         'books':books.objects.all()
#     }

def logout(request):
    request.session.clear()
    return redirect('/')

def addWish(request):
    if request.method=='POST':
        errors=wishs.objects.wishValid(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/new')
        else:
            newWish=wishs.objects.create(
                item=request.POST['item'],
                desc=request.POST['desc'],

                user=users.objects.get(id=request.session['user_id']),
            )
            user=users.objects.get(id=request.session['user_id'])
            newWish.save()
            # user.liked_wish.add(newWish)
            # newWish.liked_by.add(user)
            return redirect('/wishes')
    return render(request,'makeWish.html')

def deleteWish(request, id):
    deletshow = wishs.objects.get(id = id)
    deletshow.delete()
    return redirect('/wishes')

def edit(request, id):
    wishes = wishs.objects.get(id= id)
    context = {
        'wish': wishes
    }
    return render(request,'edit.html', context)

def editWish(request, id):
    if request.method == 'POST':
        errors = wishs.objects.wishValid(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/wishes")
        else:
            editwishes = wishs.objects.get(id= id)
            editwishes.item=request.POST['item'] 
            editwishes.desc=request.POST['desc']
            editwishes.save()
    return redirect('/wishes')

def grantwish(request, id):
    if not 'user_id' in request.session:
        return redirect('/')
    wish = wishs.objects.get(id=id)
    wish.granted=True
    wish.save()
    return redirect('/wishes')

