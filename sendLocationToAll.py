from twilio.rest import Client
import json

TWILIO_PHONE = "+18084950241"
TWILIO_AUTH = "bc38678b11c47aead44085a58a50078c"
TWILIO_SID = "AC119e5af08dfa814c741f03bae66623b9"


def sendTwilioSms(to_number, body):
    client = Client(TWILIO_SID, TWILIO_AUTH)
    message = client.messages.create(
        body=body,
        from_=TWILIO_PHONE,
        to=to_number
    )
    return message.sid


def sendLocation(location: str):
    with open("db\\contacts.json", 'r') as f:
        data = json.load(f)
        
        authorityPhones = data['authorities']
        trustedPhones = data['trusted']
        
        for phone in authorityPhones:
            try:
                sendTwilioSms(phone, location)
            except:
                pass
        
        for phone in trustedPhones:
            try:
                sendTwilioSms(phone, location)
            except:
                pass