from django.shortcuts import get_object_or_404, redirect
from .models import Conversation,Message
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from listing.models import Listing

@login_required
def initiate_conversation(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    realtor = listing.realtor
    client = request.user  # Automatically fetching logged-in user as client
    
    # Check if a conversation already exists between the client and realtor for this listing
    conversation, created = Conversation.objects.get_or_create(listing=listing, realtor=realtor)
    
    # Automatically add the client to the conversation if not already in it
    if client not in conversation.clients.all():
        conversation.clients.add(client)

    # Redirect the user to the conversation page
    return redirect('conversation_detail', conversation_id=conversation.id)

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.order_by('timestamp')
    return render(request, 'chat/conversation.html', {'conversation': conversation, 'messages': messages})
    
@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        message = Message.objects.create(conversation=conversation, sender=request.user, content=content)
        return JsonResponse({"success": True, "message": {"sender": message.sender.username, "content": message.content}})
    return JsonResponse({"success": False, "error": "Invalid request"})

