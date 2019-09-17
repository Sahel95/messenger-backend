from django.urls import path, re_path
from chat.views import *

urlpatterns = [
    # re_path('list/(?P<userid>\d{0,10})', conversation_view),
    path('message/', ChatView.as_view()),
    path('conversation/', ConversationInfo.as_view()),
    path('conversation/messages/',MessageList.as_view()),
    path('conversationtest/',ConversationList.as_view()),
    path('conversationlist/',ConversationView.as_view())
]