from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .tokens import email_verification_token

def send_verification_email(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = email_verification_token.make_token(user)
    
    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )

    subject = "Verify your Email for EcomStore"
    message = f"""
Hi {user.username},

Thank you for registering at EcomStore!

Please verify your email by clicking the link below:
{verification_link}

If you did not sign up, ignore this email.

Best,
EcomStore Team
"""

    send_mail(subject, message, None, [user.email])
