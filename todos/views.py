from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from decouple import config
import requests

# Create your views here.


def index(request):
    todos=Todo.objects.all()
    context={
        'todos':todos
    }
    return render(request, 'todos/index.html', context)

# def new(request):
#     print(request.method)
#     return render(request, 'todos/new.html')

def create(request):
    if request.method =='POST':
        title = request.POST.get('title')
        due_date = request.POST.get('due-date')
        Todo.objects.create(title=title, due_date=due_date)
        # print((title,due_date))
        sendMessage(request)
        return redirect('todos:index')
    else:
        return render(request, 'todos/create.html')
    
# def edit(request, pk):
#     todo = Todo.objects.get(id=pk)
#     context={
#         'todo':todo,
#     }
#     return render(request, 'todos/edit.html',context)

def update(request,pk):
    todo=get_object_or_404(Todo, id=pk)
    # todo=Todo.objects.get(id=pk)
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
    # todo=Todo.objects.get(id=pk)
    todo.delete()
    return redirect('todos:index')


# telegram에 bot으로 message 보내기
def sendMessage(request):
    base_url = "https://api.telegram.org"
    # chat_id, command = getUpdates()
    token = config('DONG_KEY')
    send_to_sir = '새 일이 생겼어요!'
    method = "sendMessage"
    chat_id = "873780022"
    url = f"{base_url}/bot{token}/{method}?chat_id={chat_id}&text={send_to_sir}"
    requests.get(url)
    # return render_template('home.html', command=command, chat_id=chat_id)