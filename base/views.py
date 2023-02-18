from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import *

from django.views.decorators.cache import never_cache

# Email-verification imports
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .token import account_activation_token
# Create your views here.

def activate(request, uidb64, token):
    User=get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except:
        user=None
        
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()

        messages.success(request, "Thank You for you email Configuration. Now you may login your Account.")
        return redirect('login')
    else:
        messages.error(request,"Activation link is inlvalid !")
        
    return redirect('login')


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string("base/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>,please go to <b>{to_email}</b> inbox and click on \
                    recieved activation link to confirm and complete the registration.')
    else:
        messages.error(
            request, f'Problem sending email to {to_email}, check if you typed it correctly.')


@login_required(login_url='login')
def taskList(request):
    list = Task.objects.filter(user=request.user)
    context = {'list': list}
    return render(request, 'base/task_list.html', context)


def taskdetail(request, pk):
    taskId = Task.objects.get(id=pk)
    context = {'taskId': taskId}
    return render(request, 'base/task_detail.html', context)


@login_required(login_url='login')
def create(request):
    if request.user.is_authenticated:
        user = request.user
        form = TaskForm(request.POST)
        if form.is_valid():
            todo = form.save()
            todo.user = user
            todo.save()
            return redirect('/')
        else:
            context = {'form': form}
            return render(request, 'base/create.html', context)


@login_required(login_url='login')
def update(request, pk):
    task = Task.objects.get(id=pk)

    taskform = TaskForm(instance=task)
    if request.method == 'POST':
        taskform = TaskForm(request.POST, instance=task)
        if taskform.is_valid:
            taskform.save()
            return redirect('/')

    # if request.method=='POST':

    context = {'taskform': taskform}
    return render(request, 'base/update.html', context)


def delete(request, pk):

    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        task.delete()
        return redirect('/')

    context = {'task': task}
    return render(request, 'base/delete.html', context)


@unauthenticated_user
@never_cache
def registerPage(request):
    form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect('home')

    else:
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                activateEmail(request, user, form.cleaned_data.get('email'))
                username = form.cleaned_data.get('username')
                messages.success(
                    request, "account was created for " + username)
                return redirect('login')
            else:
                messages.info(request, 'Not registered')
                return redirect('register')
    context = {'form': form}
    return render(request, 'base/register.html', context)


@unauthenticated_user
@never_cache
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('taskList')
        else:

            messages.info(request, 'Username or password is incorrect ')

    context = {}
    return render(request, 'base/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')

