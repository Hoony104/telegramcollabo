from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import Todo
from django.views.decorators.csrf import csrf_exempt
import json
from decouple import config
import requests

def sendMessage(request, title, due_date):
    base_url = 'https://api.telegram.org'
    token = config('TOKEN')
    send_to_sir = f'{title} (D-day: {due_date})'
    method = 'sendMessage'
    chat_ids = ['873780022', '861812746']
    for chat_id in chat_ids:
        url = f'{base_url}/bot{token}/{method}?chat_id={chat_id}&text={send_to_sir}'
        requests.get(url)


def index(request):
    todos=Todo.objects.all()
    context={
        'todos':todos
    }
    return render(request, 'todos/index.html', context)


def create(request):
    if request.method =='POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')
        Todo.objects.create(title=title, due_date=due_date)
        sendMessage(request, title, due_date)
        return redirect('todos:index')
    else:
        return render(request, 'todos/create.html')


def update(request,pk):
    todo=get_object_or_404(Todo, id=pk)
    if request.method=='POST':
        title= request.POST.get('title')
        due_date= request.POST.get('due-date')
        todo.title=title
        todo.due_date=due_date
        todo.save()
        return redirect('todos:index')
    else:
        context={
            'todo':todo,
        }
        return render(request, 'todos/update.html',context)

def delete(request,pk):
    todo=get_object_or_404(Todo, id=pk)
    todo.delete()
    return redirect('todos:index')


@csrf_exempt
def telegram(request):
    res = json.loads(request.body)
    text = res.get('message').get('text')
    chat_id = res.get('message').get('chat').get('id')
    base = 'https://api.telegram.org'
    token = config('TOKEN')
    url = f'{base}/bot{token}/sendMessage?text={text}&chat_id={chat_id}'
    requests.get(url)
    return HttpResponse('가랏')