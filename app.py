import os
import requests

from flask import Flask, request, Response
from messenger import Bot
from messenger.const import ATTACHMENT_TYPE_IMAGE
from messenger.models.attachment import Attachment

from const import API_URL

app = Flask(__name__)


VALIDATION_TOKEN = os.environ.get('VALIDATION_TOKEN', 'test')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN', 'test')


class EchoBot(Bot):

    def handle_message(self, messaging_event):
        sender_id = messaging_event["sender"]["id"]
        url = requests.get(API_URL).url
        self.send_attachment(sender_id, Attachment(ATTACHMENT_TYPE_IMAGE, url))


class CatGifBot(Bot):

    def handle_message(self, messaging_event):
        sender_id = messaging_event['sender']['id']
        random_image_url = requests.get(API_URL).url
        self.send_attachment(sender_id, Attachment(ATTACHMENT_TYPE_IMAGE, random_image_url))


chat_bot = CatGifBot(VALIDATION_TOKEN, PAGE_ACCESS_TOKEN)


@app.route("/webhook", methods=["GET", "POST"])
def handle():
    if request.method == "GET":
        verify_token = request.args.get('hub.verify_token')

        response = Response(request.args.get('hub.challenge'), 200)
        if verify_token != VALIDATION_TOKEN:
            response = Response('', 403)

        return response
    else:
        chat_bot.process_message(request.json)
        return Response("", 200)
