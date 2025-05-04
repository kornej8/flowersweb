from telebot import TeleBot
from flowerweb.db.db_connector import DBConnect
from flowerweb.app.core.queries import thirst_flowers
from sqlalchemy import text


class NotificationMessage:
    def __init__(self, token):
        self.body = ''
        self.to_send = False
        self.token = token

    def add_row(self, row):
        self.body += ('\n' + row)

    def send(self, chat_id):
        TeleBot(self.token).send_message(chat_id=chat_id,
                                         text=self.body,
                                         parse_mode='HTML'
                                         )


class SendNotification:
    def __init__(self, id, telebot, url):

        self.db = DBConnect()
        self.telebot = telebot
        self.url = url

        self.ids = [int(id) for id in id.split()]

    def create_link(self, flower_name: str):
        url = f"{self.url}/{flower_name}"
        link_template = '<a href="{url}">{caption}</a>'
        return link_template.format(
            url=url,
            caption=flower_name
        )

    def __call__(self):
        with self.db.connect() as conn:
            msg = NotificationMessage(self.telebot)
            flowers = conn.execute(text(thirst_flowers)).fetchall()
            if flowers:
                msg.to_send = True
                msg.add_row("Пора поливать цветочки 💐:")
                for flower in flowers:
                    flower_name = flower[0]
                    msg.add_row("   " + self.create_link(flower_name))

            if msg.to_send:
                for id in self.ids:
                    msg.send(chat_id=id)
