from django.urls import path
from . import views

urlpatterns = [
    path('listing/<int:listing_id>/chat/', views.initiate_conversation, name='initiate_conversation'),
    path('conversation/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:conversation_id>/send/', views.send_message, name='send_message'),
]

