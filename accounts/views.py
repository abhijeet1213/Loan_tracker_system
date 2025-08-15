from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt 
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.http import  HttpResponse,HttpResponseRedirect
from .models import *
from django.contrib.auth.hashers import make_password, check_password
import json
import random
import string
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
# Create your views here.

@csrf_exempt
def ks_login(request):
        # print(request.user.username)
        if request.user.is_authenticated:
           
            if  request.user.is_login == 0:
                 return render(request, 'password_reset.html')
           
            elif request.user.is_user == 1 and request.user.is_login == 1:    
                return HttpResponseRedirect(reverse('dashboard'))
            elif request.user.is_user == 1 and request.user.is_manager == 1: 

                return HttpResponseRedirect(reverse('dashboard'))
            
            else:
                return HttpResponseRedirect(reverse('dashboard'))

        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
          
            try:
                User = get_user_model()

            # user_loggedin=authenticate(request,username=email,password=password)
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'login.html', {"msg": "Incorrect Username or Passwordddd"})

        # Authenticate user (assuming you're using email as username)
            user_loggedin = authenticate(request, username=User.objects.get(email=email).username, password=password)
            # user = UserLogin.userAuth_objects.get(email_address=email,password=password)
          
            if user_loggedin is not None: 
               
                login(request, user_loggedin)
                
                if request.user.is_authenticated:
            
                    if  request.user.is_login == 0:
                        return render(request, 'password_change.html')
                    
                    elif request.user.is_user == 1:    
                        return HttpResponseRedirect(reverse('dashboard'))
                    elif request.user.is_manager == 1:    
                        return HttpResponseRedirect(reverse('dashboard'))
            else:
                return render(request, 'login.html',{"msg" : "Incorrect Username or Password "})
        else:
               return render(request, 'login.html')

@login_required(login_url='/')
@csrf_exempt
def create_user(request):
    if request.method=='POST':
       
        password_string=get_random_password()
        data=dict(json.loads(request.body))
        rl_type=data['role_type']
        t_status=data['t_status']
        print(t_status)
        print(rl_type)

        if rl_type == "1" :
           is_manager=0
           is_user=1
        else:
            is_manager=1
            is_user=0
  
        if t_status == "1":
           is_active=1
        else:
            is_active=0
        submit_data=CustomeUser.objects.create_user(
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        email=data['e_mail'],
                        username=data['e_mail'],
                        password=password_string,
                        is_active=is_active,
                        is_manager=is_manager,
                        is_login=0,
                        is_user=is_user                  
                )
        submit_data.save()
        msg=(password_string)
        return HttpResponse(msg)


@login_required(login_url='/')
@csrf_exempt
def reset_pass(request):
    if request.method=='POST':
        data=dict(json.loads(request.body))
        user=CustomeUser.objects.get(id=request.user.id)
        user.set_password(data['pass']) 
        user.save()   
        return HttpResponse('')            
    else:
        return render(request,'register.html')
                        
@login_required(login_url='/')
@csrf_exempt
def reset_pass_username(request):
    if request.method=='POST':
        data=dict(json.loads(request.body))
        try:
            user=CustomeUser.objects.get(username=data['username'])
            user.set_password(data['pass']) 
            user.save()               
            return HttpResponse('')
        except Exception as e:
            return HttpResponse('')

@login_required(login_url='/')
@csrf_exempt
def updateuser(request):
 if request.method=='POST':
        data=dict(json.loads(request.body))
        rl_type=data['role_type']
        t_status=data['t_status']
        

        if rl_type == "1" :
           is_manager=0
           is_user=1
        else:
            is_manager=1
            is_user=0

        if t_status == "1":
           is_active=1
        else:
            is_active=0

        CustomeUser.objects.filter(email=data['e_mail']).update(
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        username=data['e_mail'],
                        is_active=is_active,
                        is_manager=is_manager,
                        is_login=1,
                        is_user=is_user         
                )
        msg=('password_string')
        return HttpResponse(msg)

@login_required(login_url='/')
@csrf_exempt
def register(request):

        user_details=CustomeUser.objects.all()
        context={
            'data':user_details
        }

        html_template = loader.get_template('register_user.html')
        return HttpResponse(html_template.render(context, request))

def get_random_password():
    # choose from all lowercase letter
    random_source = string.ascii_letters + string.digits + string.punctuation
    # select 1 lowercase
    password = random.choice(string.ascii_lowercase)
    # select 1 uppercase
    password += random.choice(string.ascii_uppercase)
    # select 1 digit
    password += random.choice(string.digits)
    # select 1 special symbol
    password += random.choice(string.punctuation)

    # generate other characters
    for i in range(6):
        password += random.choice(random_source)

    password_list = list(password)
    # shuffle all characters
    random.SystemRandom().shuffle(password_list)
    password = ''.join(password_list)
    return password

@login_required(login_url='/')
@csrf_exempt
def passwword_reset(request):
    
    msg = ""
    if request.method == 'POST':
      
        data = dict(json.loads(request.body))
      
        pwd = ( data['p1'])
        usr=CustomeUser.objects.get(username=request.user.username)
        usr.set_password(pwd)
        usr.is_login="1"
        usr.save()
        msg = "1"
        logout(request)
        request.session.flush()
        return HttpResponse(msg)

@login_required(login_url='/')

def logout_request(request):
    logout(request)
    # request.session.flush()
    #messages.info(request, "You have successfully logged out.") 
    return redirect('/')