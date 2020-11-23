from datetime import datetime
import pytz

import os
import psycopg2
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json",scope)
client = gspread.authorize(creds)

sheet = client.open("Azur Lane Avrora PvP Exercise log").worksheet("Avrora")

timeValues = sheet.col_values(3)
print(timeValues[0])
#serverTime = datetime.timezone(timeDelta(hours=-7))
#time = datetime.now(serverTime).strftime("%H:%M:%S")
#date = datetime.now(serverTime).strftime("%d/%m/%Y")
