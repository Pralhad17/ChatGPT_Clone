from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import openai
from .models import ChatGPT
from django.utils import timezone


# Home page

def home(request):
    return render(request,'chatbot/index.html')



# Register user

def user_register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'chatbot/register.html',{'forms':form})


# login user

def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data =request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username,password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('chatbot')
            else:
                error_message = 'Invalid username or password'
                return render(request, 'login.html', {'error_message': error_message})
    return render (request,'chatbot/login.html',{'forms':form})


#  Open Ai Api key

openai_api_key = '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'
openai.api_key = openai_api_key

# Ask OpenAI

def ask_openai(message):
    response = openai.ChatCompletion.create(
        model ='gpt-4',
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": message},
        ]
    )
    
    answer = response.choices[0].message.content.strip()
    return answer


# Create view
@login_required(login_url='login')
def chatbot(request):
    chats = ChatGPT.objects.filter(user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = ChatGPT(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot/ChatGPT.html', {'chats': chats})




# User logout

def user_logout(request):
    auth.logout(request)
    return redirect("login")



