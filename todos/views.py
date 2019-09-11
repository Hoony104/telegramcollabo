from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo


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


def sendMessage(request, title, due_date):
    import requests
    from decouple import config

    base_url = "https://api.telegram.org"
    token = config('DONG_KEY')
    send_to_sir = f'{title} (D-day: {due_date})'
    method = "sendMessage"
    chat_ids = ["873780022", '861812746']
    for chat_id in chat_ids:
        url = f"{base_url}/bot{token}/{method}?chat_id={chat_id}&text={send_to_sir}"
        requests.get(url)
