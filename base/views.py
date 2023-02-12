from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .forms import *
from .models import *
# Create your views here.


def taskList(request):
    list = Task.objects.all()
    context = {'list': list}
    return render(request, 'base/task_list.html', context)


def taskdetail(request, pk):
    taskId = Task.objects.get(id=pk)
    context = {'taskId': taskId}
    return render(request, 'base/task_detail.html', context)


def create(request):

    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'base/create.html', context)


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

    context = {'task':task}
    return render(request, 'base/delete.html', context)
