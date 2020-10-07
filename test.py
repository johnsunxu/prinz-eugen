from datetime import datetime
import pytz

serverTime = datetime.now(pytz.timezone("US/Pacific"))
print(serverTime)
#serverTime = datetime.timezone(timeDelta(hours=-7))
#time = datetime.now(serverTime).strftime("%H:%M:%S")
#date = datetime.now(serverTime).strftime("%d/%m/%Y")