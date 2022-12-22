
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = 'smtpselnox@gmail.com'
EMAIL_HOST_PASSWORD = 'ahbfjyjsviaflwgq'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

import smtplib
# from Product.models import Product
import random
# from sweede.settings import EMAIL_HOST_USER,EMAIL_HOST_PASSWORD,EMAIL_PORT,EMAIL_HOST
otp=random.randint(1000, 9999)
# from_email='smtpselnox@gmail.com'

def send_OneToOneMail(from_email='',to_emails=''):
    # assert isinstance(to_emails,list)
    server=smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    Subject="Selnox"
    Text="Your One Time Password is "  + str(otp)
    
    msg='Subject: {}\n\n{}'.format(Subject, Text)
    server.sendmail(from_email,to_emails,msg)
    server.quit()

def send_OneToManyMail(from_email='',to_emails=[]):
    assert isinstance(to_emails,list)
    server=smtplib.SMTP(EMAIL_HOST,EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)
    Subject="Selnox"
    Text="You add the new Product " 
    
    msg='Subject: {}\n\n{}'.format(Subject, Text)
    server.sendmail(from_email,to_emails,msg)
    server.quit()
    
send_OneToOneMail(from_email='smtpselnox@gmail.com',to_emails='selnox94@gmail.com')
# send_OneToManyMail(to_emails=['selnox94@gmail.com','selnox93@gmail.com'])
