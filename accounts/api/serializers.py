from django.forms import ValidationError
from rest_framework import serializers

from accounts.models import User, DeletedUser


from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ValidateEmailSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2', 'email']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        """
            Get Data given to serializer as request.data
        """
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        validators = []

    def validate(self, attrs):
        """
            Get Data given to serializer as request.data
        """
        password = attrs.get('password')
        email = attrs.get('email')
        user_obj = User.objects.filter(email=email)
        if user_obj.exists():
            print('User exists good')
        else:
            raise serializers.ValidationError("User with this email not found")
        return attrs


import base64
from django.core.files.base import ContentFile
import random
import binascii


class UserSignupSerializer(serializers.ModelSerializer):


    class Meta:
        model = User

        fields = ["id",
                  "first_name",
                  "last_name"
                  "mobile",
                  "email",
                  "profile_pic",
                  "advocate_license",
                  "birth_date",
                  "address",
                  "gender",
                  "profession"]

        read_only_fields=["mobile","id"]

    def update(self, instance, validated_data):
        file_array = {'profile_pic': instance.profile_pic,
                      'advocate_license':instance.advocate_license}
        for i in file_array:
            print(validated_data.get(i, ''))
            if validated_data.get(i, ''):

                image_data = validated_data.get(i)
                # print(len(image_data.split(';base64,')))
                try:
                    data = ContentFile(base64.b64decode(image_data))
                except binascii.Error as e:
                    print(e)
                    raise binascii.Error(f'{i} send data is in incorrect format it should be in bash 64')
                file_name = str(random.random()) + '.' + 'png'
                file_array[i].save(file_name, data, save=True)
                validated_data.pop(i)
                print('done')

        super().update(instance, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id",
                  "first_name",
                  "last_name",
                  "mobile",
                  "email",
                  "profile_pic",
                  "birth_date",
                  "address",
                  "gender",
                  ]
        read_only_fields=["mobile","id"]
        extra_kwargs = {
            'mobile': {'write_only': False},

        }
    def update(self, instance, validated_data):
        file_array = {'profile_pic': instance.profile_pic,
                      }
        for i in file_array:
            print(validated_data.get(i, ''))
            if validated_data.get(i, ''):

                image_data = validated_data.get(i)
                # print(len(image_data.split(';base64,')))
                try:
                    data = ContentFile(base64.b64decode(image_data))
                except binascii.Error as e:
                    print(e)
                    raise binascii.Error(f'{i} send data is in incorrect format it should be in bash 64')
                file_name = str(random.random()) + '.' + 'png'
                file_array[i].save(file_name, data, save=True)
                validated_data.pop(i)
                print('done')
        validated_data.mobile=instance.mobile
        print(validated_data.mobile,instance.mobile)
        super().update(instance, validated_data)



class PublicUserProfileSerializer(serializers.ModelSerializer):
    user_interest=serializers.SerializerMethodField()
    startup_stage=serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'first_name', ]
    def get_startup_stage(self,obj):
        if obj.startup_stage:
            return obj.startup_stage.stage_name
        return obj.startup_stage
    def get_user_interest(self,obj):
        if obj.user_interest:
            return obj.user_interest.name
        return obj.user_interest


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class UserSendResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['mail']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)
            link = 'http://localhost:8000/api/accounts/reset-password/' + uid + '/' + token
            print(link)
            data = {
                'subject': "Reset Your Password",
                'to_email': user.email,
                'to_email': "Click Following Link to reset password." + link
            }
            return attrs
        else:
            raise serializers.ValidationError("You are not a registered user.")


class UserResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not valid or expired")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Password and Confirm Password doesn't match")


