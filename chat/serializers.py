from rest_framework import serializers
from chat.models import Messages, Conversations
from user.models import Users
from datetime import datetime
from user.serializers import RequestSignupSerializer,ShortUserProfileSerializer
# from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist


class ConversationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversations
        fields = '__all__'


class ConversationsInfoMembersSerializer(serializers.ModelSerializer):
    
    members=ShortUserProfileSerializer(many=True)
    
    class Meta:
        model = Conversations
        fields = '__all__'


class MessagesListSerializer(serializers.ModelSerializer):

    # sender_id = RequestSignupSerializer()
    # conversation_id = ConversationsInfoMembersSerializer()

    class Meta:
        model = Messages
        fields = '__all__'


class ConversationsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversations
        fields = '__all__'


class RequestConversationMemberSrializer(serializers.ModelSerializer):
    class Meta:
        model = Conversations
        fields = ['name']


class RequestChatSerializers(serializers.Serializer):

    conversation_id = serializers.IntegerField(min_value=1)
    text = serializers.CharField(required=False)
    picture = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=False, required=False)
    file = serializers.FileField(max_length=None, allow_empty_file=False, use_url=False, required=False)

    def create(self, validated_data):
        # u = Users.objects.get(
        #         token= validated_data['token'])
        print(self.context)
        print('---------------',validated_data)
        c = Conversations.objects.get(
                id=validated_data['conversation_id'])
        m = Messages(
            sender_id=self.context['user'],
            conversation_id=c,
            date=datetime.now(),
            text=validated_data.get('text', None),
            picture=validated_data.get('picture', None),
            file=validated_data.get('file', None)
        )
        m.save()
        return m


class RequestGetSearchMessageSerializers(serializers.Serializer):
    conversation_id = serializers.IntegerField (
        min_value=1, required=True
    )
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)
    text = serializers.CharField(required=False)
    # size = serializers.IntegerField(
    #     min_value = 1, required=True
    # )

    # def create(self, data):
    #     conversation= Conversations.objects.get(id=data['conversation_id'])
    #     from_date = data.get('from_date', None)
    #     to_date = data.get('to_date', None)
    #     messages = Messages.objects.filter(
    #         conversation_id=conversation,
    #         date__range=[from_date, to_date],
    #         text__startswith=data.get('text', None)
    #     )
    #     return messages

class ConversationMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Messages
        exclude = ['conversation_id']

class SearchMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class RequestEditMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ['text','id']

    def update(self, instance, validated_data):
        print (instance)
        instance.text = validated_data.get('text',instance.text)
        instance.save()
        return instance