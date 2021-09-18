from django.shortcuts import render, redirect
from home.models import Notes, User
from django import forms
from notesapp.utils import random_color
from django.http import JsonResponse, HttpResponseRedirect
from django.db import IntegrityError
import json
from django.contrib.auth import authenticate, login as login_user, logout
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
import random
from django.template.loader import render_to_string 

# Create your views here.

class NoteForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea( attrs = {
        'class': 'new_note'
    }))

class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs = {
        'class': 'register_form_input'
    }))
    firstName = forms.CharField(label="First name", widget=forms.TextInput(attrs = {
        'class': 'register_form_input'
    }))
    lastName = forms.CharField(label="Last name", widget=forms.TextInput(attrs = {
        'class': 'register_form_input'
    }))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs = {
        'class': 'register_form_input'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs = {
        'class': 'register_form_input'
    }))
    confirmPassword = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs = {
        'class': 'register_form_input'
    }))

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs = {
        'class': 'register_form_input'
    }))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs = {
        'class': 'register_form_input'
    }))
    


def home_notes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content')
            note = Notes(content=content, color=random_color(), user=request.user)
            note.save()

            return redirect(home_notes)

    else:
        if request.user.is_authenticated:
            return render(request, 'home/home.html', {
                'notes': Notes.objects.filter(user=request.user),
                'note_form': NoteForm()
            })
        else:
             return render(request, 'home/home.html', {
                'notes': Notes.objects.all(),
                'note_form': NoteForm()
            })

def delete_note(request, note_id):
    try:
        note = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        return JsonResponse({"error": "Note not found."}, status=404)

    note.delete()

    return JsonResponse({"status": 204})

@csrf_exempt
def edit_note(request, note_id):
    try:
        note_id = Notes.objects.get(pk=note_id)
    except Notes.DoesNotExist:
        return JsonResponse({"error": "Note not found."}, status=404)

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print(data)
    print('_'*100)
    print(data['note_id'])
    print('_'*100)
    print(data['new_text'])
    print('_'*100)
    note = Notes.objects.get(pk=data['note_id'])
    note.content = data['new_text']
    note.save()

    return JsonResponse({"message": "Edited succesfuly"}, status=201)


def register_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        password = request.POST["password"]
        confirmation = request.POST["confirmPassword"]

        if password != confirmation:
            return render(request, 'register.html', {
                'message': "Passwords don`t match"
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.last_name = lastName
            user.first_name = firstName
            user.save()

        except IntegrityError:
            return render(request, "register.html", {
                'message': "Username already taken.",
                'register_form': RegisterForm()
            })
        login_user(request, user)
        return HttpResponseRedirect(reverse("main_notes"))

    return render(request, 'register.html', {
        'register_form': RegisterForm()
    })


def login_person(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login_user(request, user)
            return HttpResponseRedirect(reverse("main_notes"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html", {
            'login_form': LoginForm()
        })

def logout_user(request):
    logout(request)
    return render(request, 'home/home.html', {
        'notes': Notes.objects.all(),
        'note_form': NoteForm(),
        'message': 'Logged out succesfuly',
    })


def send_rand_mail(request):
    if request.method == 'POST':
        notes = Notes.objects.filter(user=request.user)
        only_notes = []
        for note in notes:
            only_notes.append(note.content)

        text_note = random.choice(only_notes)

        subject = "Your daily quote by you"
        from_email = "bambruproductos@gmail.com"
        to_email = request.user.email

        html_template = 'note.html'

        html_message = render_to_string(html_template, { 'message': text_note, })

        message = EmailMessage(subject, html_message, from_email, [to_email])
        message.content_subtype = 'html' # this is required because there is no plain text email message
        message.send()

        return redirect(home_notes)