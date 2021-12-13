from django.shortcuts import render, redirect
from .models import Chat, Message
from django.http import HttpResponse, JsonResponse


def home_page(request):
    return render(request, 'home_page.html')


def chat(request, chat):
    username = request.GET.get('username')
    chat_details = Chat.objects.get(name=chat)
    return render(request, 'chat.html', {
        'username': username,
        'chat': chat,
        'chat_details': chat_details
    })


def checkview(request):
    chat = request.POST['chat_name']
    username = request.POST['username']

    if Chat.objects.filter(name=chat).exists():
        return redirect('/'+chat+'/?username='+username)
    else:
        new_chat = Chat.objects.create(name=chat)
        new_chat.save()
        return redirect('/'+chat+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    chat_id = request.POST['chat_id']

    new_message = Message.objects.create(value=message, user=username, chat=chat_id)
    new_message.save()
    return HttpResponse('Message was sent')


def getMessages(request, chat):
    chat_details = Chat.objects.get(name=chat)

    messages = Message.objects.filter(chat=chat_details.id)
    return JsonResponse({"messages":list(messages.values())})