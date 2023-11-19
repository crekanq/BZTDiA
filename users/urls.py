from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import SignUpView, SignInView, CreateChatView, ChatView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create_chat/', CreateChatView.as_view(), name='create_chat'),
    path('', ChatView.as_view(), name='chat'),
]
