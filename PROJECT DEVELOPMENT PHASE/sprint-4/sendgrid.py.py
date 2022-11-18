
import sendgrid
import os
from sendgrid.helpers.mail import *
API_KEY=('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')

sg = sendgrid.SendGridAPIClient(API_KEY)
from_email = Email("d2dpea@gmail.com")
to_email = To("inigokathrin07@gmail.com")
subject = "Alert"
content = Content("text/plain", "limit is reached")
mail = Mail(from_email, to_email, subject, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)