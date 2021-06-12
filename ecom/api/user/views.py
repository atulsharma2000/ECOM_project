from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model  # important one
from django.views.decorators.csrf import csrf_exempt  # adding some stuff in CSRF files so that we can make request from another site
from django.contrib.auth import login, logout

import re
import random
   
# used for running regular expresions
# Create your views here.


def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))
    # for _ in range(length) this piece of the code will generate string which is 10 character long and i.e. our session token.


@csrf_exempt                                # here we used the decorator
def signin(request):                        #custom method
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameter.'})

    username = request.POST['email']
    password = request.POST['password']
    # validation part
    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({'error': 'Enter a valid email.'})
    if len(password) < 4:
        return JsonResponse({'error': 'Password needs to be atleast 4 char.'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)   #grabs the model based on email

        if user.check_password(password):           #given by django 
            usr_dict = UserModel.objects.filter(email=username).values().first()
            usr_dict.pop('password')

            if user.session_token != "0":       # not equal to 0(default value) means session already running
                user.session_token = "0"        #for next time it logs in then its gets 0
                user.save()
                return JsonResponse({'error': "Previous session exists!"})
            
            token = generate_session_token()       #genrated token
            user.session_token = token
            user.save()
            login(request, user)       # default login provided by django, where we porovided chain on the request and provied user
            return JsonResponse({'token': token, 'user': usr_dict})  #throwing to front-end
        else:
            return JsonResponse({'error': 'Invalid Password'})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})



def signout(request, id):
    # we need id of that user cuz of session tokens and this id will be responsible for modifying database, flushing out the session token again
    logout(request)
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({'error': "Invalid User ID"})

    return JsonResponse({'success': "Logout success"})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}   

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]      #based on action we are returning it

        except KeyError:
            return [permission() for permission in self.permission_classes]