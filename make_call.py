import os
from twilio.rest import Client

account_sid = ''
auth_token = ''

client = Client(account_sid, auth_token)

call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+91',
                        from_='+1'
                    )
                
call = client.calls.create(
                        url='http://demo.twilio.com/docs/voice.xml',
                        to='+91',
                        from_='+1'
                    )

print(call.sid)