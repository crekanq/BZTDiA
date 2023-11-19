from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from .forms import SignUpForm, SignInForm, MessageForm
from .models import Chat, Message


class SignUpView(View):
    template_name = 'users/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chat')
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create a common chat
            common_chat, created = Chat.objects.get_or_create()

            # Add the new user to the common chat
            common_chat.users.add(user)

            login(request, user)
            return redirect('signin')
        return render(request, self.template_name, {'form': form})


class SignInView(View):
    template_name = 'users/signin.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('chat')
        form = SignInForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignInForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        return render(request, self.template_name, {'form': form})


class CreateChatView(UserPassesTestMixin, View):
    template_name = 'users/create_chat.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('signin')

    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return render(request, self.template_name, {'users': users})

    def post(self, request):
        selected_users_ids = request.POST.getlist('selected_users')
        users = User.objects.filter(id__in=selected_users_ids)
        chat = Chat.objects.create()
        chat.users.add(request.user, *users)
        return redirect('/')


class ChatView(UserPassesTestMixin, View):
    template_name = 'users/chat.html'

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('signin')

    def get(self, request):
        # Fetch the common chat
        common_chat, created = Chat.objects.get_or_create()

        # Fetch all user chats, including the common chat
        user_chats = Chat.objects.filter(users=request.user)

        # Combine user chats and the common chat
        all_chats = user_chats | Chat.objects.filter(id=common_chat.id)

        message_form = MessageForm()
        return render(request, self.template_name, {'chats': all_chats, 'message_form': message_form})


    def post(self, request):
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data['content']
            chat_id = message_form.cleaned_data['chat_id']
            chat = Chat.objects.get(id=chat_id)
            Message.objects.create(chat=chat, sender=request.user, content=content)
        else:
            print(message_form.errors)

        return redirect('chat')

    def toggle_chat_visibility(self, chat_id):
        chat = Chat.objects.get(id=chat_id)
        chat.hidden = not chat.hidden
        chat.save()

    def get(self, request):
        user_chats = Chat.objects.filter(users=request.user)
        message_form = MessageForm()
        return render(request, self.template_name, {'chats': user_chats, 'message_form': message_form})

    def post(self, request):
        if 'toggle_chat' in request.POST:
            chat_id = request.POST.get('chat_id')
            self.toggle_chat_visibility(chat_id)
            return redirect('chat')

        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data['content']
            chat_id = message_form.cleaned_data['chat_id']
            chat = Chat.objects.get(id=chat_id)
            Message.objects.create(chat=chat, sender=request.user, content=content)
        else:
            print(message_form.errors)

        return redirect('chat')
