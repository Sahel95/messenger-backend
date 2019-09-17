from datetime import datetime
from pprint import pprint
import uuid
import hashlib

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from messenger.utils import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication 
from django.core.mail import send_mail
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from user.models import Users
from chat.models import *
from user.serializers import *
from messenger.task import Bye, send_email




class UserSearch(APIView):
    permission_classes=[AllowAny]

    def post(self, request):

        users = Users.objects.filter(username__startswith=str(request.POST['username']))
        serializer = UserSearchSerializer(instance=users, many=True)

        return Response(
            {
                'data' : serializer.data
            },
            status=status.HTTP_200_OK
        )

class ContactList(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        print(request.POST['self_id'])
        print(request.POST['user_id'])
        user = Users.objects.get(id=request.POST['self_id'])
        print(user)
        serializer = AddContactSerializer(data=request.POST, instance=user)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'data' : 'User added to your contacts'
                }
            )

        else:
            return Response(
                {
                    'msg' : 'serializer is NOT valid!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )





    def get(self, request):
        user = Users.objects.get(id=request.GET['id'])
        # print(user.contacts.all())
        serializer = ContactListSerializer(instance=user)

        return Response(
            {
                'data': serializer.data
             },
            status=status.HTTP_200_OK
        )





def user_list_view(request):

    user_message_count = {}

    for u in Users.objects.all():
        recievedmessages = []
        conversations = Conversations.objects.filter(members__id = u.id )

        for c in conversations:
            messages = Messages.objects.filter(conversation_id = c.id)

            for m in messages:
                if m.sender_id.id != u.id :
                    recievedmessages.append(m)

        d = len(recievedmessages)
        user_message_count[u] = d

    return render (
        request,
        'userlist.html',
        {
            "users" : Users.objects.all(),
            "user_message_count" : user_message_count
        }
    )

class UserList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        users = Users.objects    
        serializer = UserListSerializer(instance = users , many=True)
        return Response (
            {'data' : serializer.data},
            status=status.HTTP_200_OK
        )



class EditProfileViews(APIView):

    permission_classes = [IsAuthenticated]


    def put(self, request):

        u = Users.objects.get(id=request.user.id)
        serializer = RequestEditProSerializer (instance=u, data=request.data)
        # if data['token'] == u.token:
        if serializer.is_valid():
            serializer.save()
            return Response (
                {'message' : 'your data saved!'},
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                {
                    'message' : 'your token is wrong'
                },
                status=status.HTTP_400_BAD_REQUEST
            )



class GetVerification(APIView):


    def get(self, request, username, token):

        u = Users.objects.get(username=username)
        data = {
            'username' : username
        }

        serializer = RequestVerifiedUser(data=data, instance=u)

        strverificationtoken = str(u.verificationtoken)

        if token == strverificationtoken :
            if serializer.is_valid():
                print('TEST_________________')
                serializer.save()
                return Response(
                    {'msg':'your email is verified'},
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {'msg':'serializer is NOT valid'},
                    status=status.HTTP_404_NOT_FOUND            
                )              

        else:
            return Response(
                {'msg':'your email is NOT verified'},
                status=status.HTTP_404_NOT_FOUND            
            )


class SignupViews(APIView):

    # authentication_classes = (
    #     CsrfExemptSessionAuthentication, BasicAuthentication)

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = RequestSignupSerializer (data=request.POST)

        if serializer.is_valid():
            Bye.delay()
            serializer.save()
            u = Users.objects.get(username=serializer.data['username'])
            data = {
                'email' : serializer.data['email'],
                'token' : u.verificationtoken,
                'username' : serializer.data['username']
            }
            send_email.delay(data)

            return Response(
                {
                    'message':'your account have been created successfully',
                    'data' : serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

# @permission_classes([AllowAny, ])
class LoginView(APIView):

    # authentication_classes = (
    #     CsrfExemptSessionAuthentication, BasicAuthentication)

    permission_classes = [AllowAny]

    def post(self,request):
        serializer = RequestLoginSerialize(data=request.POST)
        if serializer.is_valid():

            u = authenticate(
                request,
                username=serializer.data['username'],
                password=serializer.data['password']
            )

            if u is None:
                return Response(
                    {
                        'message' : 'your username is wrong'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
            if u:
                user = Users.objects.get(username=serializer.data['username'])
                secret_key = "1234"
                payload = jwt_payload_handler(user)
                # token = jwt.encode(payload, secret_key, algorithm='HS256').decode('utf-8')
                # token = jwt.encode(payload, settings.SECRET_KEY)
                token = jwt.encode(payload, secret_key)
                u.token = token
                u.save()

                print(token)
                print(payload)
                print(u.token)
                print(type(token))
                
                login(request, u)
                return Response(
                    {
                        'message' : 'your account info is correct',
                        'first_name' : u.first_name,
                        'id' : u.id,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message' : 'your password is wrong'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
        ) 


class UserListItemView(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    permission_classes = [IsAuthenticated]



    def get(self,request):
        request_serializer = RequestGetSerializer(data = request.GET)
        users = Users.objects
 

        if request_serializer.is_valid():
            if 'first_name' in request_serializer.data:
                users = users.filter(
                    first_name = request_serializer.data['first_name']
                )

            if 'last_name' in request_serializer.data:
                users = users.filter(
                    last_name = request_serializer.data['last_name']
                )

            serializer = UsersSerializer(instance = users , many=True)

            return Response (
                {'data' : serializer.data},
                status=status.HTTP_200_OK)

        else:
            return Response (
                request_serializer.errors,
                status = status.HTTP_400_BAD_REQUEST  
            )

    def post(self,request):

        serializer = UsersSerializer( data = request.POST)
       
        if serializer.is_valid():
            user = serializer.save()
        else:
            return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
        
        return Response(
            {'data' : serializer.data},
            status.HTTP_201_CREATED
            )


