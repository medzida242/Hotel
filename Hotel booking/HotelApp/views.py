from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import *
import random
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from .models import Hotel, Comment
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout

# Create your views here.

def index(request):
    return render(request, 'index.html')


# ustimaj da radi fino za kad imaju stranice a ne sa modalima
def registration(request):
    User = get_user_model()
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        name = request.POST['name']
        surname = request.POST['surname']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already in use")
                return redirect('registration')

            elif User.objects.filter(username=username).exists():
                messages.info(request, "Username already in use")
                return redirect('registration')

            else:
                user = User.objects.create_user(username=username, email=email, password=password, name=name,
                                                surname=surname)
                user.is_active = True
                user.save()
                return redirect('login')

        else:
            messages.info(request, "Password not the same")
            return redirect('registration')
    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == "POST":

        password = request.POST['password']
        email = request.POST['email']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')

        else:
            messages.info(request, "Wrong credentials")
            return render(request, 'index.html')

    else:
        return render(request, 'login.html')


def reservation(request):

    hoteli=Hotel.objects.all()
    nase =Hotel.objects.get(ime='ljepi hotel')
    korisnikovhotel = Mjesto.objects.create(imemjesta='ernesovac', drzava='rs')
    korisnikovhotel.save()
    context={
        'hoteli':hoteli,
          'nase':nase
      }    
    return render(request, 'reservation.html', context)

def search(request):
    if request.method == "GET":
        ime_query = request.GET.get('ime_query', '')  # Get the value of the 'ime_query' parameter
        mjesto_query = request.GET.get('mjesto_query', '')  # Get the value of the 'mjesto_query' parameter
        
        ime_rezultat = Hotel.objects.filter(ime__icontains=ime_query) if ime_query else []  # Perform search based on 'ime' attribute
        mjesto_rezultat = Hotel.objects.filter(mjesto__imemjesta__icontains=mjesto_query) if mjesto_query else []  # Perform search based on 'mjesto' attribute
        
        context = {
            'ime_query': ime_query,
            'mjesto_query': mjesto_query,
            'ime_rezultat': ime_rezultat,
            'mjesto_rezultat': mjesto_rezultat
        }
    return render(request, 'search.html', context)
    
def hotel_details(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    comments = Comment.objects.filter(hotel=hotel)
    if request.method == 'POST':
        # Check if a comment delete request is submitted
        if 'delete_comment_id' in request.POST:
            comment_id = request.POST.get('delete_comment_id')
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return redirect('hotel:hotel_details', hotel_id=hotel_id)
        
        # Process other POST requests (e.g., comment submission)
        # ...
    context = {
        'hotel': hotel,
        'comments': comments,
        'user': request.user,
    }
    return render(request, 'hotel_details.html', context)

@login_required
def add_comment(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(hotel=hotel, user=request.user, content=content)
        return redirect('hotel:hotel_details', hotel_id=hotel_id)
    else:
        return redirect('hotel:search')


@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:  # Check if the current user is the owner of the comment
        comment.delete()
    return redirect('delete_comment', comment_id=comment_id)