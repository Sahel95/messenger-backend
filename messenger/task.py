from __future__ import absolute_import, unicode_literals
# from celery.decorators import task
from messenger.celery import app
from user.models import Users
from django.core.mail import send_mail
from messenger.settings import BASE_URL



@app.task
def Bye():
    print ('----------------------------------------------------------------BYE BYE')

@app.task
def send_email(data):

    verification_url = BASE_URL+'/user/verify/username/'+data['username']+'/validate/token/'+data['token']+'/'
    send_mail(
        'Confirm mail',
        verification_url,
        'test@sorooshkhodami.ir',
        ['test@sorooshkhodami.ir'],
        # [data['email']],
        fail_silently=False,
    )