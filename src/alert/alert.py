class Alert:
    def __init__(self, smtp_server, senderEmail, senderPassword, receiverEmail, port=465):
        self.smtp_server = 'UNKNOWN_SERVER'
        self.port = port
        self.senderEmail = "UNKNOWN_SENDER"
        self.senderPassword = "UNKNOWN_PASSWORD"
        self.receiverEmail = "UNKNOWN_RECEIVER"

    def notify(self, release_dates):
        pass