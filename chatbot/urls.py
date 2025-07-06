from django.urls import path
from .views import chatbot_view

urlpatterns = [
    path('', chatbot_view, name='chatbot'),
    path('consult/', chatbot_view, name='consult'),
]
