from django.urls import path
from . import views

urlpatterns = [

    # Authentication APIs
    # path('validate-email/', views.ValidateEmail.as_view(), name="validate_email_api"),
    # path('validate-otp-email/', views.ValidateOtpEmail.as_view(), name="validate_otp_email_api"),

    path('validate-phoneno/', views.ValidatePhoneNo.as_view(), name="validate_phone_no_register_api"),
    path('validate-otp-phoneno/', views.ValidateOtpPhoneNo.as_view(), name="validate_otp_phoneno_api"),

    # path('login-email/', views.UserLoginView.as_view(), name="login_api"),
    path('complete-registeration/', views.CompleteRegisteration.as_view(), name="complete_registeration_api"),



    # path('get-interest/', views.GetInterestView.as_view(), name="get_interest_api"),
    # path('get-interest/filter/', views.AllInterestWithUser.as_view(), name="get_interest_api"),
    # path('get-interest/filter/<int:interest_id>/', views.AllInterestWithUser.as_view(), name="get_interest_api"),
    # path('get-interest/filter/<int:interest_id>/<int:number>/', views.AllInterestWithUser.as_view(), name="get_interest_api"),

    # path('get-wealth-source/', views.GetWealthSourceView.as_view(), name="get_wealth_source_api"),
    # path('get-week-hour/', views.GetWeekHourView.as_view(), name="get_week_hours_api"),

    # path('change-password/', views.UserChangePasswordView.as_view(), name="change_password_api"),
    # path('send-reset-password-email/', views.UserSendResetPasswordViewEmail.as_view(),
    #      name="send_reset_password_email_api"),
    # path('reset-password/<uid>/<token>/', views.UserResetPasswordView.as_view(), name="reset_password_api"),
    path('profile/', views.UserProfileView.as_view(), name="profile_api"),
    path('profile/update/', views.CompleteRegisteration.as_view(), name="profile_update"),

    # Home Page Api
    # path('all_profile/', views.AllProfileView.as_view(), name='all profile'),
    path('profile/<int:id>/', views.GetProfileById.as_view(), name='all profile'),
    path('all_profile/auth/', views.GetAllProfileBy.as_view(), name='all profile'),
    # path('all_connections_list/', views.AllConnectionsList.as_view(), name='AllConnectionsList'),
    # path('profile_link/', views.create_profile_share_link.as_view(), name='profile_link'),
    # path('profile_link/<int:user_id>/', views.create_profile_share_link.as_view(), name='profile_link'),
    # path('profile_link/code-<code>/', views.profile_link_redirect, name='profile_link'),

    # path('profile_link/change/', views.ChangeMobileNumber_getOtp.as_view(), name='profile_link'),
    # path('profile_link/change/varify/', views.ChangeMobileNumber_varifyOtp.as_view(), name='profile_link'),
    #
    # path('delete_user/', views.Delete_user.as_view(), name='profile_link'),
    # path('block_user/', views.AddBlock.as_view(), name='AddBlock'),
    # path('block_user/list/', views.BlockUserList.as_view(), name='BlockUserList'),



]
