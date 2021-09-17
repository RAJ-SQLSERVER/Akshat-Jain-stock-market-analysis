import os
from datetime import date
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient

from environs import Env
env = Env()
env.read_env()


def create_and_send_mail(response_list):
    message = "<head><style>table,th,td {padding: 10px;border: 1px solid black;border-collapse: collapse;}</style></head><body><table><tr><th>Stock Name</th><th>Days since bearish crossover</th><th>RSI</th></tr>"

    for item in response_list:
        stock_name = item['stock_name']
        dsbc = item['days_since_bearish_crossover']
        rsi = round(item['rsi'], 2)
        message += f'<tr><td>{stock_name}</td><td align=center>{dsbc}</td><td>{rsi}</td></tr>'

    message += "</table>"
    send_mail(message)


def send_mail(msg):
    email_sender = env.str('EMAIL_SENDER')
    email_recipients = env.list('EMAIL_RECIPIENTS')
    message = Mail(
        from_email=env.str('EMAIL_SENDER'),
        to_emails=env.list('EMAIL_RECIPIENTS'),
        subject='[Stocks Analysis] Strategy 1:  ' + date.today().strftime("%B %d, %Y"),
        html_content=msg)
    try:
        sendgrid_client = SendGridAPIClient(env.str('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
    except Exception as e:
        print(e)
