""" Daily Digest Email of Cisco Spark Rooms that had activity during the day. """


import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# User Defined Variables
EMAIL_ADDRESS = ""
EMAIL_PASSWORD = ""
SPARK_PERSONAL_ACCESS_TOKEN = ""
FROM_NAME = ""
TO_EMAIL_ADDRESS = ""

# Email (Gmail) Configuration
smtp = smtplib.SMTP("smtp.gmail.com", 587)
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# Cisco Spark
SPARK_ROOM = requests.get("https://api.ciscospark.com/v1/rooms",
                          headers={'Authorization': 'Bearer ' + SPARK_PERSONAL_ACCESS_TOKEN})

RESULTS = SPARK_ROOM.json()

CURRENT_ROOMS = {}

for room in RESULTS['items']:
    CURRENT_ROOMS.update({room['title']: room['lastActivity']})

TODAY = str(datetime.today().date())

EMAIL_MESSAGE = 'Todays Active Rooms:\n\n'

for room_title, lastActivity in CURRENT_ROOMS.items():
    if TODAY in lastActivity:
        EMAIL_MESSAGE += str('- ' + room_title)
        EMAIL_MESSAGE += '\n'

# Send the Email
body = MIMEText(EMAIL_MESSAGE)
body['Subject'] = 'Cisco Spark Daily Digest'
body['From'] = FROM_NAME
body['To'] = TO_EMAIL_ADDRESS
smtp.sendmail(EMAIL_ADDRESS, TO_EMAIL_ADDRESS, str(body))

smtp.quit()
