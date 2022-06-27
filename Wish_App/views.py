from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *


def index(request):
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash = bcrypt.hashpw(
                request.POST['pass'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                password=hash
            )
            user.save()
            request.session['user_id'] = user.id
            messages.success(request, "User successfully Add")
            return redirect('/wishes')


def login(request):
    if request.method == 'POST':
        error = User.objects.login_validator(request.POST)
        if len(error) > 0:
            for key, value in error.items():
                messages.error(request, value)
            return redirect('/')
        else:
            request.session['user_id'] = User.objects.get(
                email=request.POST['email']).id
            return redirect('/wishes')


def logout(request):
    del request.session['user_id']
    return redirect('/')


def wishes(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "wishes": Wish.objects.all().order_by('-id')

    }
    return render(request, "wishes.html", context)


def addWish(request):
    if not 'user_id' in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session['user_id']),

    }
    return render(request, "addWish.html", context)


def create(request):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method == 'POST':
        if request.method == 'POST' and 'submit' in request.POST:
            errors = Wish.objects.validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/addWish')
            else:
                user = User.objects.get(id=request.session['user_id'])
                wish = Wish.objects.create(
                    item=request.POST['item'],
                    desc=request.POST['desc'],
                    isGranted=False,
                    user=user,
                )
                # travel.list.add(user)
                wish.save()
                messages.success(request, "wish successfully Add")
                return redirect('/wishes')
        if request.method == 'POST' and 'cancel' in request.POST:
            return redirect('/wishes')


def remove(request, ID):
    if not 'user_id' in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=ID)
    wish.delete()

    messages.success(request, "wish deleted successfully")
    return redirect('/wishes')


def edit(request, ID):
    if not 'user_id' in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=ID)
    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "wish": Wish.objects.get(id=ID),
    }
    return render(request, "editWish.html", context)


def update(request):
    if not 'user_id' in request.session:
        return redirect('/')
    if request.method == 'POST':
        if request.method == 'POST' and 'Edit' in request.POST:
            errors = Wish.objects.validator(request.POST)
            ID = request.POST['ID']
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect(f'/edit/{ID}')
            else:
                ID = request.POST['ID']
                travel = Wish.objects.get(id=ID)
                travel.item = request.POST['item']
                travel.desc = request.POST['desc']
                travel.save()
                messages.success(request, "Wish successfully Updated")
                return redirect('/wishes')
        if request.method == 'POST' and 'cancel' in request.POST:
            return redirect('/wishes')


def like(request, ID):
    if not 'user_id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    wish = Wish.objects.get(id=ID)
    wish.likes.add(user)
    wish.save()
    return redirect('/wishes')


def Granted(request, ID):
    if not 'user_id' in request.session:
        return redirect('/')
    wish = Wish.objects.get(id=ID)
    wish.isGranted = True
    wish.save()
    return redirect('/wishes')


def view(request):
    if not 'user_id' in request.session:
        return redirect('/')
    wishes: Wish.objects.all()
    usersWishes = Wish.objects.filter(isGranted=True)
    yourWishesGrant = Wish.objects.filter(
        isGranted=True, user=request.session['user_id'])
    yourWishesPend = Wish.objects.filter(
        isGranted=False, user=request.session['user_id'])
    context = {
        "usersWishes": usersWishes,
        "yourWishesGrant": yourWishesGrant,
        "yourWishesPend": yourWishesPend


    }
    return render(request, "detailsWish.html", context)
