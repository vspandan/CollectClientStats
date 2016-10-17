import smtplib
from Server.Properties import SMTP_SERVER,SMTP_PORT, SMTP_EMAIL_ADDR, SMTP_SENDER_PASSWORD, SMTP_SUCC_MSG, SMTP_ERR_MSG

#Notifies user with a mail
def sendMail (receivers, message):
    try:
        servr = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
        servr.ehlo()
        servr.starttls()
        servr.ehlo()
        servr.login(SMTP_EMAIL_ADDR, SMTP_SENDER_PASSWORD)
        servr.sendmail(SMTP_EMAIL_ADDR, receivers, message)
        servr.quit()
        print(SMTP_SUCC_MSG)
    except smtplib.SMTPException as e:
        print(SMTP_ERR_MSG, e)