from datetime import date


from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MessagesListSerializer
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


from chat.pagination import *
from chat.serializers import *
from messenger.utils import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication 


from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator 


# def login (func):

#     def wrapper(request):
#         if type(request.user) is AnonymousUser:
#             return Response(
#                 {'message':'Unauthorize'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         else:
#             func()
    
#     return wrapper

# def login (func):

#     def wrapper(request, *args, **kwargs):
#         if type(request.user) is AnonymousUser:
#             return Response(
#                 {'message':'Unauthorize'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         else:
#             func(request, *args, **kwargs)
#         return response
    
#     return wraps(func)(wrapper)





class MessageList(generics.ListAPIView):
    permission_classes = [AllowAny]

    # pagination_class = StandardResultsSetPagination
    #lookup_url_kwarg = "id"
    # conversation = Conversations.objects.get(id=id)
    # queryset = Messages.objects.filter(conversation_id=conversation)
    # serializer_class = MessagesListSerializer

    def get (self, request,  *args, **kwargs):
        conversation = Conversations.objects.get(id=request.GET['id'])
        message = Messages.objects.filter(conversation_id=conversation)
        serializer = MessagesListSerializer(instance=message, many=True)

        paginator = Paginator(serializer.data, 2)
        page = request.GET['page']
        data = paginator.get_page(page)

        for m in data.object_list:
            message = Messages.objects.get(id=m['id'])
            message.seen = True
            message.save()

        # print(serializer.data[2:4])
        return Response(
            {
                'page': request.GET['page'],
                'count': 2,
                'data': data.object_list
            },
            status=status.HTTP_200_OK
        )


class ConversationList(APIView):
    permission_classes = [AllowAny]

    def get (self, request):
        user = Users.objects.get(id=request.GET['id'])
        # list = [x for x in user.conversations.all()]
        conversations = user.conversations.all()
        serializer = ConversationListSerializer(instance=conversations, many=True)

        mydict = {}
        for s in serializer.data:
            c = Conversations.objects.get(id=s['id'])
            print(c.messages.last())
            mydict[c.name] = c.messages.last()

        print(mydict)

        return Response(
            {
                "data": {
                    'conversation' : serializer.data,
                }
            }
        )

    # def get (self,request):
    #     conversations = Conversations.objects
    #     serializer = ConversationsListSerializer(instance = conversations , many=True)
    #     return Response (
    #         {'data' : serializer.data},
    #         status=status.HTTP_200_OK
    #     )


class ConversationInfo (APIView):
    permission_classes = [AllowAny]

#MEMBER of CONVERSATION
    def post (self, request):
        data = request.POST
        request_serializer = RequestConversationMemberSrializer(data=data)
        conversation = Conversations.objects.get(name=data['name'])
        if request_serializer.is_valid():
            members = []
            print(conversation.members.all())
            for m in conversation.members.all():
                members.append(m.id)

            return Response(
                {'members id' : members }
            )        
        return Response(
            {'msg' : 'sadadad'}
        )

#DATA of CONVERSATION
    def get (self,request):
        conversation = Conversations.objects.get(id=request.GET['id'])
        serializer = ConversationsDataSerializer(instance=conversation)
        return Response (
            {'data' : serializer.data},
            status=status.HTTP_200_OK
        )


class ChatView (APIView):
    permission_classes = [AllowAny]

    # @method_decorator(login)
    def get(self,request):

        # request_serializer = RequestGetSearchMessageSerializers ( data = request.GET )
        data = request.GET
        conversation= Conversations.objects.get(id=data['conversation_id'])
        print(conversation.messages.all)
        from_date = data.get('from_date', conversation.date_modified)
        to_date = data.get('to_date', date.today())
        messages = Messages.objects.filter(
            conversation_id=conversation,
            date__range=[from_date, to_date],
            text__startswith=data.get('text', None)
        )
        serializer = MessagesListSerializer (instance=messages, many=True)
        print(messages)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK

        )

        # else:
        #     return Response (
        #         request_serializer.errors,
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        #


    # @method_decorator(login_required)
    #SEND MESSAGE
    def post (self,request):

        if type(request.user) is AnonymousUser:
            return Response(
                {'message':'Unauthorize'},
                status=status.HTTP_401_UNAUTHORIZE
            )
        else:
            print(dir(request))
            print(request.user.id)
            u = Users.objects.get(id=request.user.id)
            print(request.POST)
            print((request.data))
            serializer = RequestChatSerializers (data=request.data, context={'user':u})
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {'message' : 'massaged saved!'},
                    status = status.HTTP_201_CREATED
                )
            
            else:
                return Response(
                        {'message' : 'Serializer in NOT valid!'},
                        status = status.HTTP_400_BAD_REQUEST
                    )



    def put (self,request):
        data = request.data
        u = Users.objects.get(token=data['token'])
        m = Messages.objects.get(id=data['message_id'], sender_id=u)
        serializer = RequestEditMessageSerializer(instance=m,data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message' : 'massaged edited!'},
                status = status.HTTP_201_CREATED
            )
        return Response(
                {'message' : 'ERROR'},
                status = status.HTTP_400_BAD_REQUEST
            )






class ConversationView(APIView):

    permission_classes = [AllowAny]

    def get(self,request):
        conversation = Conversations.objects.get(name=request.GET['name'])
        print('-------------------------------------',conversation)
        messages = Messages.objects.filter(conversation_id=conversation)
        print('------------------------------------',messages)
        serializer = ConversationMessagesSerializer (instance=messages, many=True)

        return Response(
            {'data': serializer.data}
        )








    # elif request.method == 'POST':
    #     print('request.body:',request.body)
    #     print('request.POST:',request.POST)
    #     new_user = Users (
    #         first_name = request.POST['firstname'],
    #         last_name = request.POST['lastname']
    #     )
    #     users.append(new_user)
    #     return render(
    #         request,
    #         'userlist.html',
    #         {
    #         'users':users
    #         }
    #     )
