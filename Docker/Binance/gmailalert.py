import smtplib, ssl

class GmailAlert():
    def __init__(self, sender, password, receiver):
        self.smtp_server = 'smtp.gmail.com'
        self.port = 465
        self.sender = sender
        self.password = password
        self.receiver = receiver

    def notify(self, tokens, release_date):
        subject = f'Subject: New Binance releases - {tokens}'
        message = f'{subject}\n\nBinance will list cryptocurrency pairs {tokens} on {release_date}.'

        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receiver, message)
        except Exception as e:
            print(e)