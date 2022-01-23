from http.client import HTTPResponse
from django.forms import forms
from django.shortcuts import render, redirect
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
# Create your views here.

# rooms = [
#     {'id' : 1, 'name': 'Class1'}, 
#     {'id' : 2, 'name': 'Class2'},
#     {'id': 3, 'name': 'Class3'}
# ]

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Password doesn't match!")
        except:
            messages.error(request, "Username does not exist!")
        
        

    context = {'page': page}
    return render(request, 'base/login_form.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home') 

def registerUser(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # print(form.errors)
            messages.error(request, "An error occurred during registration!")
    return render(request, 'base/login_form.html', {'form': form})

def home(request):
    q = request.GET.get('q')
    if q == None: q = ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:4]
    room_count = rooms.count()
    topics = Topic.objects.all()[0:3]
    context = {'rooms': rooms, 'topics': topics, 'room_count' : room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    if request.method == 'POST':
        Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('message')
        )
        room.participants.add(request.user)
        return redirect('room',pk = room.id)
        
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(
            name = request.POST.get('room_name'),
            topic = topic,
            host = request.user,
            description = request.POST.get('room_about')        
        )
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'base/create_room.html', context)

@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HTTPResponse("You are not allowed here!")

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('room_name')
        room.topic = topic
        room.description = request.POST.get('room_about')
        room.save() 
        return redirect('home')
    context = {'form': form, 'room': room, 'topics': topics}
    return render(request, 'base/create_room.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HTTPResponse("You are not allowed here!")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    context = {'room':room}
    return render(request, 'base/delete_room.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.method == "POST":
        message.delete()
        return redirect('home')
    context = {'room':message}
    return render(request, 'base/delete_room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    room = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user' : user, 'rooms': room, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/user_profile.html', context)


@login_required(login_url='login')
def editUser(request):
    form = UserForm(instance=request.user)
    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/edit-user.html', context)

def topicsView(request):
    q = request.GET.get('q')
    if q == None: q = ''

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activities(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})