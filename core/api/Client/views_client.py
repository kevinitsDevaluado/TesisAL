import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from config import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from core.user.models import User
from core.pos.models import Client
from core.api.Client.serializers_client import UserSerializer, ClientSerializer

class ClientViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def list(self,request):
        users_serializer = self.get_serializer(self.queryset, many=True)
        return Response(users_serializer.data, status = status.HTTP_200_OK)

    def create(self,request):
        users_serializer = UserSerializer(data=request.data)
        if users_serializer.is_valid():
            email = request.data['email']
            users_serializer.save()
            id_cli = User.objects.get(id = users_serializer.data['id'])
            id_cli.email = email
            id_cli.save()
            mobile = request.data['mobile']
            address = request.data['address']
            Client.objects.create(user=id_cli,mobile=mobile,address=address)
            self.send_email(id_cli.id)
            return Response({'message':'Usuario creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response( users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_object(self,pk):
        return get_object_or_404(Client, id=pk)
    
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = ClientSerializer(user)
        return Response([user_serializer.data], status = status.HTTP_200_OK)

    def send_email(self, id):
        user = User.objects.get(pk=id)
        to=user.email
        fromemail='alex.lema7059@outlook.com'
        subject='Términos y Condiciones'
        message = MIMEMultipart('alternative')
        message['subject'] = subject
        parameters = {
                    'user': user,
                    #'mainpage': Mainpage.objects.first(),
                # 'link_home': 'http://{}'.format(url),
                    #'link_login': 'http://{}/login'.format(url),
                }
        html = render_to_string('user/email_sign_in.html', parameters)
        content = MIMEText(html, 'html')
        message.attach(content)

        mailserver = smtplib.SMTP('smtp.office365.com',587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()  #again
        mailserver.login('alex.lema7059@outlook.com', 'Alexleo1999lema.')
        mailserver.sendmail(fromemail, to, message.as_string())
        mailserver.quit()
    