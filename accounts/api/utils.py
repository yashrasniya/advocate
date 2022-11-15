from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
import os, re, random,requests


# sending otp functions
def sendOtpToPhNo(phone: str, otp: int) -> bool:
    """
    Takes Phone No and sends otp and returns True for success and False on failure
    """
    api_key = '9fe14c8c-c86e-11ea-9fa5-0200cd936042'
    # api_key2 = 'a2b2f8f1-567c-11ec-b710-0200cd936042'
    api_key2 = '8c806792-9ea0-11ec-a4c2-0200cd936042'
    template_name = 'GuliGuli'
    template_name2 = 'groupick'

    url = f'http://2factor.in/API/V1/{api_key2}/SMS/{phone}/{otp}/{template_name2}'
    req = requests.get(url)
    print(req.text)
    return req.status_code == 200


def sendOtpToEmail(email_id: str, otp: int) -> bool:
    """
    Takes Email and sends otp and returns True for success and False on failure
    """
    email = EmailMessage(
        subject='Otp For Signup',
        body=f'Otp: \t{otp}',
        from_email='info@coihub.co',
        to=[email_id]
    )
    try:
        email.send()
    except Exception as e:
        return False
    return True


def sendOtp(credentials: str) -> bool:
    """
    Takes credentails as input and sends otp to it. Credentials can phone number or email
    """
    otp = random.randint(999, 9999)
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # return otp#for development only
    if re.fullmatch(email_regex, credentials):
        return otp if sendOtpToEmail(credentials, otp) else False
    else:
        return otp if sendOtpToPhNo(credentials, otp) else False


# manual auth token generation
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
