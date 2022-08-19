import smtplib
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
to='paulmariscal1@gmail.com'
fromname='kevinits'
fromemail='kevin.alvarado8502@hotmail.com'
subject='Términos y Condiciones'
body='this is the message body'
message = MIMEMultipart('alternative')
message['subject'] = subject
parameters = {
            #'user': user,
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
mailserver.login('kevin.alvarado8502@hotmail.com', 'kevinpaul1997')
mailserver.sendmail(fromemail, to, message.as_string())
mailserver.quit()