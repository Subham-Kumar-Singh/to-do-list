from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .decorators import *

from django.views.decorators.cache import never_cache


# Create your views here.


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
# @permission_required('todo.can_view_all_todos', raise_exception=True) 
def create(request):
    if request.user.is_authenticated:
        user=request.user
        form = TaskForm(request.POST)   
        if form.is_valid():
            todo=form.save()
            todo.user=user
            # if form.is_valid:
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
                form.save()
                return redirect('/')
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
