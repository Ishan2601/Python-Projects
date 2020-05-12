# Importing Libraries
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

#User Credentials
user_email = str(input("Your Email Id: "))
user_password = str(input("Your Password: "))

#Importing the data of recepients
data = pd.read_csv("Data.csv")
names = data["Names"].tolist()
emails = data["Emails"].tolist()


#Starting the SMTP Server
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(user_email,user_password)

#Creating the Multipart
for i in range(len(emails)):
    mail = MIMEMultipart()
    mail['From'] = user_email
    mail['To'] = emails[i]
    #mail['Cc'] = cc
    #mail['Bcc'] = bcc
    
    #Creating the basic mail content and adding it to mail
    subject = "Personalized Automated Mail"
    body = '''Hello {},
    This is an personalized auto-generated mail.
    Thank You.'''.format(names[i])
          
    mail['Subject'] = subject    
    mail.attach(MIMEText(body, 'plain'))

    #Attaching Files
    filename = '{}.png'.format(names[i])
    file = open(filename,'rb')

    attachment = MIMEBase('application','octet-stream')
    attachment.set_payload((file).read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition',"attachment; filename= "+filename)

    mail.attach(attachment)

    #Final Mail
    final = mail.as_string()

    #Sending the mail
    server.sendmail(user_email,emails[i],final)
    print("Mail sent to "+names[i])

#Quitting the server
server.quit()
print("All mails sent successfully")

