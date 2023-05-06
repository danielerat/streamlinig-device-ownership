import requests
from dotenv import load_dotenv
import os
load_dotenv()


def send_text_message_welcome(phone, names="Dear"):
    if phone != "":
        url = os.environ.get("INTOUCH_URL")
        data = {
            "username":  os.environ.get("INTOUCH_USERNAME"),
            "password":  os.environ.get("INTOUCH_PASSWORD"),
            "senderid": os.environ.get("INTOUCH_USERID"),
            "recipients": phone,
            "message": "Hi, {}. Welcome at Streamlining. let's Get Started Registering your Devices".format(names),
        }

        return requests.post(url, data=data)
