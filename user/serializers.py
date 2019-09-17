import hashlib
from rest_framework import serializers
from user.models import Users
# from django.contrib.auth.models import User


class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username']


class AddContactSerializer(serializers.Serializer):

    self_id = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def update(self, instance, data):
        u = Users.objects.get(id=data['user_id'])
        instance.contacts.add(u)
        instance.save()
        return instance


class ContactListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'contacts', 'username']


class RequestVerifiedUser(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'is_verified', 'verificationtoken'] 

    def update(self, instance, validated_data):
        # instance.is_verified = validated_data.get('is_verified',instance.is_verified)
        instance.is_verified = True
        instance.save()
        print('TEST______________')
        return instance


class ShortUserProfileSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name

    class Meta:
        model = Users
        fields = ['username', 'full_name']



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['last_name', 'first_name', 'id'] 



class RequestEditProSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['last_name', 'first_name', 'profile_pic']

    def update(self, isinstance, validated_data):
        isinstance.first_name = validated_data.get('first_name',isinstance.first_name)
        isinstance.last_name = validated_data.get('last_name',isinstance.last_name)
        isinstance.profile_pic = validated_data.get('profile_pic',isinstance.profile_pic)
        isinstance.save()
        return isinstance



class RequestSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"

    def create(self, data):
        # hash_password = hashlib.md5(data['password'].encode()).hexdigest()
        # changed_data['password'] = hash_password
        # changed_data = data
        # del changed_data['groups']
        # del changed_data['user_permissions']
        u = Users(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
            password = data['password'],
            email=data['email'],
        )
        u.set_password(data['password'])
        u.save()
        return u

class RequestLoginSerialize(serializers.Serializer):
    username = serializers.CharField(
        max_length=30 , required=True , allow_blank=False
    )
    password = serializers.CharField(
        max_length=30 , required=True , allow_blank=False
    )


class RequestGetSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=False , allow_blank=False , max_length=100
        )
    last_name = serializers.CharField(
        required=False , allow_blank=False , max_length=100
        )

    def validate(self, data):
        if 'first_name'not in data and 'last_name' not in data:
            raise serializers.ValidationError('At least one of firstname or lastname parameters are required')
        return data



class UsersSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=True , allow_blank=False , max_length=100
        )
    last_name = serializers.CharField(
        required=True , allow_blank=False , max_length=100
        )


    def validate_number_of_frineds(self, data):
        if data == 5:
            raise serializers.ValidationError(
                'hala har chizi ke mikhaym'
            )
        return data

    def create(self, validated_data):
        u = Users(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            # birthday = validated_data['birthday'],
            # number_of_friends = validated_data['number_of_frineds']
        )
        u.save()
        return u