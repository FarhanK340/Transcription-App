from django.shortcuts import render
from .models import Room, Message
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
# from django.template.response import TemplateResponse


def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']

        try:
            get_room = Room.objects.get(room_name=room)
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
        return redirect('chatApp:room', room_name=room, username=username)


    return render(request, 'chatApp/index.html')


# def MessageView(request, room_name, username):
#     get_room = Room.objects.get(room_name=room_name)
#     get_messages = Message.objects.filter(room=get_room)

#     if not get_room or not get_messages:
#         # set status code to 404
#         return HttpResponse(status = 404)

#     context = {
#         'messages': get_messages,
#         'user': username,
#         'room_name': room_name,
#     }

#     return render(request, 'chatApp/message.html', context)

def MessageView(request, room_name, username):
    # Use `get_object_or_404` for cleaner handling
    get_room = get_object_or_404(Room, room_name=room_name)
    get_messages = Message.objects.filter(room=get_room)


    # if not get_messages.exists():  # Check if room exists
    #     # return an error message with status code 404
    #     return HttpResponse("No messages found", status=404)

    # check if room exists
    if not get_room:
        # set status code to 404
        return HttpResponse("No room found", status = 404)

    context = {
        'messages': get_messages,
        'user': username,
        'room_name': room_name,
    }

    return render(request, 'chatApp/message.html', context)


