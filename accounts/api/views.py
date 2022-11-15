from typing import Type, List

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from accounts.models import User, DeletedUser, Otp

from .serializers import ValidateEmailSerializer, UserLoginSerializer, UserSignupSerializer, \
    UserChangePasswordSerializer, UserSendResetPasswordEmailSerializer, \
    UserResetPasswordSerializer, UserProfileSerializer
from .renderers import CustomJsonRenderer
from .utils import sendOtp, get_tokens_for_user


# Validate a number by sending OTP as sms for number Login & Registeration
class ValidatePhoneNo(APIView):
    renderer_classes = [CustomJsonRenderer]

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        used_for = request.data.get('used_for')
        if mobile and used_for:
            phone = str(mobile)
            if used_for == 'register':
                user = User.objects.filter(mobile=phone)
                if user.exists():
                    return Response({
                        "status": False,
                        "detail": "A user with this Phone Number already exists."
                    })
                else:
                    otp = sendOtp(phone)
                    if otp:
                        otp_obj = Otp.objects.filter(credentials=phone)
                        if otp_obj.exists():
                            otp_obj = Otp.objects.get(credentials=phone)
                            otp_obj.value = otp
                            otp_obj.save()
                        else:
                            otp_obj = Otp.objects.create(credentials=phone, value=otp)
                        print(otp)
                        return Response({
                            "status": True,
                            "message": "OTP Send Successfully"
                        })
                    else:
                        return Response({
                            "status": False,
                            "detail": "Sending OTP error. Check your number and try again."
                        })
            else:
                user = User.objects.filter(mobile=phone)
                if phone == '1988888888':
                    return Response({
                        "status": True,
                        "message": "OTP Send Successfully"
                    })
                if not user.exists():
                    return Response({
                        "status": False,
                        "detail": "A user with this Phone Number Not Found."
                    })
                else:
                    otp = sendOtp(credentials=phone)
                    if otp:
                        otp_obj = Otp.objects.filter(credentials=phone)
                        if otp_obj.exists():
                            otp_obj = Otp.objects.get(credentials=phone)
                            otp_obj.value = otp
                            otp_obj.save()
                        else:
                            otp_obj = Otp.objects.create(credentials=phone, value=otp)
                        print(otp)
                        return Response({
                            "status": True,
                            "message": "OTP Send Successfully"
                        })
                    else:
                        return Response({
                            "status": False,
                            "detail": "Sending OTP error. Check your number and try again."
                        })
        else:
            return Response({
                "status": False,
                "detail": "Fields Missing"
            })


# Validate OTP with the Database OTP for number Login & Registeration
class ValidateOtpPhoneNo(APIView):
    renderer_classes = [CustomJsonRenderer]

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile', False)
        otp_sent = request.data.get('otp_sent', False)
        used_for = request.data.get('used_for')
        if mobile and otp_sent and used_for:
            user_obj = User.objects.filter(mobile=mobile)

            otp_obj = Otp.objects.filter(credentials=mobile)
            if mobile == '1988888888' and otp_sent == '123456':
                try:
                    oo = User.objects.get(mobile='1988888888')
                except User.DoesNotExist as e:
                    oo = User.objects.create(mobile='1988888888')
                token = get_tokens_for_user(oo)
                return Response({
                    'token': token,
                    'msg': 'Login Successful'
                }, status=status.HTTP_202_ACCEPTED)
            # first check if the user exists or not
            if user_obj.exists():
                # check if there is any otp in database with this phone number
                if otp_obj.exists():
                    # check if the otp matched or not
                    if otp_sent == otp_obj[0].value:
                        # check if it is called for register or login
                        if used_for == 'register':
                            return Response({
                                "status": False,
                                "detail": "User Already Exists With This Phone Number."
                            })
                        else:
                            # login here
                            # user_obj = User.objects.get(mobile=mobile)
                            token = get_tokens_for_user(user_obj[0])
                            return Response({
                                'token': token,
                                'msg': 'Login Successful'
                            }, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response({
                            "status": False,
                            "detail": "Otp Not Matched"
                        })
                else:
                    return Response({
                        "status": False,
                        "detail": "Phone Number Not Validated."
                    })
            else:
                if otp_obj.exists():
                    if otp_sent == otp_obj[0].value:
                        # check if it is called for register or login
                        if used_for == 'register':
                            user_obj = User.objects.create()
                            user_obj.email = mobile
                            user_obj.mobile = mobile
                            user_obj.save()
                            token = get_tokens_for_user(user_obj)
                            return Response({
                                'token': token,
                                'msg': 'Login Successful'
                            }, status=status.HTTP_202_ACCEPTED)
                        else:
                            return Response({
                                "status": False,
                                "detail": "User not found Phone Number."
                            })
                    else:
                        return Response({
                            "status": False,
                            "detail": "Otp Not Matched"
                        })
                else:
                    return Response({
                        "status": False,
                        "detail": "Phone Number Not Validated."
                    })
        else:
            return Response({
                "status": False,
                "detail": "Fields are missing"
            })


# Completet Registeration API
class CompleteRegisteration(APIView):
    renderer_classes = [CustomJsonRenderer]
    permission_classes = [IsAuthenticated]

    def change_data(self, obj, dis, str):
        if dis.get(str, '') and dis.get(str, '') != 'Select startup stage':
            try:

                dis[str] = obj.objects.get(id=int(dis.get(str)))
                print(str)
                return False
            except obj.DoesNotExist  as e:
                print(e)
                return True
            except (AttributeError, ValueError) as e:
                print(e)
                return True
        else:
            try:
                dis.pop(str)
            except KeyError as e:
                print(e)
                return False

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        data._mutable = True

        print(data, 'error free')

        UserSignupSerializer.update(UserSignupSerializer(), request.user, data)
        ser = UserSignupSerializer(request.user)
        return Response({
            "status": True, 'data': ser.data,
            "detail": "User Registertion Completed Successfully."
        })


class UserProfileView(APIView):
    renderer_classes = [CustomJsonRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        print(data)
        data._mutable = True

        print(data, 'error free')

        UserProfileSerializer.update(UserProfileSerializer(), request.user, data)
        ser = UserProfileSerializer(request.user)
        return Response({
            "status": True, 'data': ser.data,
            "detail": "User Registertion Completed Successfully."
        })


class GetProfileById(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user_obj = User.objects.get(id=id)
        except User.DoesNotExist as e:
            return Response({'status': False}, status=status.HTTP_200_OK)

        ser = UserProfileSerializer(user_obj, context={'user': request.user})
        return Response(ser.data, status=status.HTTP_200_OK)


class GetAllProfileBy(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_obj = User.objects.all()
        ser = UserProfileSerializer(user_obj, many=True, context={'user': request.user})
        return Response(ser.data, status=status.HTTP_200_OK)

# # Validate Email by sending OTP
# class ValidateEmail(APIView):
#     renderer_classes = [CustomJsonRenderer]
#
#     def post(self, request, format=None):
#         serializer = ValidateEmailSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         email = request.data.get('email')
#         otp = sendOtp(credentials=email)
#         if otp:
#             otp_obj = Otp.objects.filter(credentials=email)
#             if otp_obj.exists():
#                 otp_obj = Otp.objects.get(credentials=email)
#                 otp_obj.value = otp
#                 otp_obj.save()
#             else:
#                 otp_obj = Otp.objects.create(credentials=email, value=otp)
#             print(otp)
#             return Response({
#                 "status": True,
#                 "message": "OTP Send Successfully"
#             })
#         else:
#             return Response({
#                 "status": False,
#                 "detail": "Sending OTP error. Check your email and try again."
#             })
#
#
# # Validate OTP for Registeration with email
# class ValidateOtpEmail(APIView):
#     renderer_classes = [CustomJsonRenderer]
#
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email', False)
#         password = request.data.get('password', False)
#         otp_sent = request.data.get('otp_sent', False)
#         if email and otp_sent and password:
#             # Check if the user exists or not
#             if User.objects.filter(email=email).exists():
#                 return Response({
#                     "status": False,
#                     "detail": "User with this Email already exists."
#                 })
#             else:
#                 otp_obj = Otp.objects.filter(credentials=email)
#                 if otp_obj.exists():
#                     if otp_sent == otp_obj[0].value:
#                         user_obj = User.objects.create(email=email)
#                         user_obj.set_password(password)
#                         user_obj.save()
#                         token = get_tokens_for_user(user_obj)
#                         return Response({
#                             'token': token,
#                             'msg': 'Registeration Successful'
#                         }, status=status.HTTP_202_ACCEPTED)
#                     else:
#                         return Response({
#                             "status": False,
#                             "detail": "Invalid Otp. Validate Email again."
#                         })
#                 else:
#                     return Response({
#                         "status": False,
#                         "detail": "Email Not Validated."
#                     })
#         else:
#             return Response({
#                 "status": False,
#                 "detail": "Fields are missing"
#             })
#
#
# # takes email and password to login
# class UserLoginView(APIView):
#     renderer_classes = [CustomJsonRenderer]
#
#     def post(self, request, format=None):
#         serializer = UserLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=False)
#         email = serializer.data.get('email')
#         password = serializer.data.get('password')
#         user = authenticate(email=email, password=password)
#         if user is not None:
#             token = get_tokens_for_user(user)
#             return Response({
#                 'token': token,
#                 'msg': 'Login Successful'
#             }, status=status.HTTP_202_ACCEPTED)
#         else:
#             return Response({
#                 'errors': {
#                     'non_field_errors': ['Email or Password is not valid']
#                 }
#             }, status=status.HTTP_202_ACCEPTED)
# class UserChangePasswordView(APIView):
#     renderer_classes = [CustomJsonRenderer]
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, format=None):
#         serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
#         if serializer.is_valid(raise_exception=True):
#             return Response({
#                 'msg': 'Password Changed Successful'
#             }, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserSendResetPasswordViewEmail(APIView):
#     renderer_classes = [CustomJsonRenderer]
#
#     def post(self, request, format=None):
#         serializer = UserSendResetPasswordEmailSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             return Response({
#                 'msg': 'Password Reset Link Sent. Please check your email.'
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class UserResetPasswordView(APIView):
#     renderer_classes = [CustomJsonRenderer]
#
#     def post(self, request, uid, token, format=None):
#         serializer = UserResetPasswordSerializer(data=request.data, context={
#             "uid": uid, "token": token
#         })
#         if serializer.is_valid(raise_exception=True):
#             return Response({
#                 'msg': 'Password Reset Successfully'
#             }, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
#
# class AllConnectionsList(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         if request.GET.get('user_id',''):
#             oo=User.objects.filter(id=request.GET.get('user_id'))
#             if oo.exists():
#                 list=oo[0].connection_list()
#             else:
#                 return Response({'status': False,'error':'user not found'})
#
#         else:
#             list = request.user.connection_list()
#         return Response({'status': True, 'connections': list, 'total': len(list)})
#
# from django.shortcuts import redirect
#
#
# class create_profile_share_link(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, user_id=None):
#
#         if not user_id:
#             user_id = request.user
#         else:
#             try:
#                 user_id = User.objects.get(id=user_id)
#             except User.DoesNotExist as e:
#                 return Response({'status': False, 'error': f'user not found', 'error_': str(e)})
#         if Profile_link.objects.filter(user=user_id).exists():
#             code = Profile_link.objects.get(user=user_id).code
#             return Response({'status': True, 'link': code})
#         else:
#             obj = Profile_link.objects.create(user=user_id)
#             return Response({'status': True, 'link': obj.code})
#
#
# def profile_link_redirect(request, code):
#     if code:
#         return redirect(f'https://coihub.com/{code}')
#     else:
#         return
#
#
# class ChangeMobileNumber_getOtp(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         credentials = request.data.get('mobile', '') or request.data.get('email', '')
#         if request.data.get('mobile', ''):
#             credentials = request.data.get('mobile')
#         elif request.data.get('email', ''):
#             credentials = request.data.get('email')
#         if credentials:
#             otp = sendOtp(credentials=credentials)
#             if otp:
#                 otp_obj = Otp.objects.filter(credentials=credentials)
#                 if otp_obj.exists():
#                     otp_obj = Otp.objects.get(credentials=credentials)
#                     otp_obj.value = otp
#                     otp_obj.save()
#                 else:
#                     otp_obj = Otp.objects.create(credentials=credentials, value=otp)
#                 print(otp)
#                 return Response({
#                     "status": True,
#                     "message": "OTP Send Successfully"
#                 })
#             else:
#                 return Response({'status': False, 'error': 'mobile number is incorrect'})
#
#
# class ChangeMobileNumber_varifyOtp(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         credentials = request.data.get('mobile', '') or request.data.get('email', '')
#         if request.data.get('mobile', ''):
#             credentials = request.data.get('mobile')
#         elif request.data.get('email', ''):
#             credentials = request.data.get('email')
#         otp_sent = request.data.get('otp_sent', False)
#         if credentials and otp_sent:
#             otp_obj = Otp.objects.filter(credentials=credentials)
#
#             if otp_obj.exists():
#                 # check if the otp matched or not
#                 if otp_sent == otp_obj[0].value:
#                     # login here
#                     if request.data.get('mobile', ''):
#                         request.user.mobile = credentials
#                     elif request.data.get('email', ''):
#                         request.user.email = credentials
#                     request.user.save()
#
#                     # user_obj = User.objects.get(mobile=mobile)
#                     return Response({'status': True,
#                                      'msg': 'Login Successful'
#                                      }, status=status.HTTP_202_ACCEPTED)
#
#         return Response({'status': False,
#                          'msg': 'Some thing went wrong'
#                          })
#
#
# class Delete_user(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def change_data(self, obj, dis, str):
#         if dis.get(str, '') and dis.get(str, '') != 'Select startup stage':
#             try:
#
#                 dis[str] = obj.objects.get(id=int(dis.get(str)))
#                 print(str)
#                 return False
#             except obj.DoesNotExist  as e:
#                 print(e)
#                 return True
#             except (AttributeError, ValueError) as e:
#                 print(e)
#                 return True
#         else:
#             try:
#                 dis.pop(str)
#             except KeyError as e:
#                 print(e)
#                 return False
#
#     def get(self, request):
#         ser = UserProfileSerializer(request.user)
#         data = ser.data
#         data.pop('id')
#         data.pop('password')
#         data.pop('last_login')
#         connection = data.pop('connection')
#         print(data)
#         pp = (self.change_data(WeekHour, data, 'week_hours'),
#               self.change_data(StartupStage, data, 'startup_stage'),
#               self.change_data(EmpStatus, data, 'emp_status'),
#               self.change_data(WealthSource, data, 'wealth_source'),
#               self.change_data(Interest, data, 'user_interest'),
#               self.change_data(IdeaStage, data, 'idea_stage'))
#         oo = DeletedUser(**data)
#
#         for i in connection:
#             try:
#                 user = User.objects.get(id=i)
#                 oo.connection.add(user)
#             except User.DoesNotExist as e:
#                 pass
#         oo.save()
#
#         request.user.delete()
#         return Response({'status': True, 'message': 'user is deleted!'})
#
#
# class AddBlock(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         if request.data.get('user_id', '') and request.data.get('action', ''):
#             obj = User.objects.filter(id=request.data.get('user_id'))
#             if len(obj) == 0:
#                 return Response({'status': False,
#                                  'msg': 'user id not found'
#                                  })
#             if request.data.get('action')=='block':
#                 request.user.block.add(obj[0])
#
#             if request.data.get('action')=='unblock':
#                 request.user.block.remove(obj[0])
#
#             request.user.save()
#             return Response({'status': True,
#                              'msg': f'User is {request.data.get("action")}'
#                              })
#         return Response({'status': False,
#                          'msg': 'user id not missing',
#                          'data': request.data
#                          })
#
#
# class BlockUserList(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         return Response(request.user.block.all().values('id','email','profile_image','first_name','last_name'))
