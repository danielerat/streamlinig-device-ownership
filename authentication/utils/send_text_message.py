import requests


def send_text_message_welcome(phone, names="Dear"):
    if phone != "":
        url = "https://www.intouchsms.co.rw/api/sendsms/.json"
        data = {
            "username": "danielerat",
            "password": "GUcR@.xY59VypWh",
            "senderid": "25228",
            "recipients": phone,
            "message": "Hi, {}. Welcome at Streamlining. let's Get Started Registering your Devices".format(names),
        }

        return requests.post(url, data=data)
