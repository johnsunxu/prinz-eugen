# This file is part of Prinz Eugen.

# Prinz Eugen is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Prinz Eugen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with Prinz
# Eugen. If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import psycopg2
import os
import datetime

class DataPoint():
    def __init__(self, x, y, color): 
        self.x = x 
        self.y = y 
        self.color = color

def extractList(lst, attribute):
    output = []
    for element in lst: 
        if attribute == "x":
           output.append(element.x)
        elif attribute == "y":
            output.append(element.y)
        elif attribute == "c":
            output.append(element.color)
    return output
    

#Database connections
load_dotenv(dotenv_path="./dev.env")
DATABASE_URL = os.getenv('DATABASE_URL')
avrora_db = DATABASE_URL
avrora_conn = psycopg2.connect(avrora_db, sslmode="allow")
avrora_cur = avrora_conn.cursor()


plt.figure(num=1, figsize=(10, 5), dpi=80, facecolor="w", edgecolor="k")

#Get data
avrora_cur.execute("SELECT * FROM avrora_entries WHERE rushername= \'IWaka\' ")
data = avrora_cur.fetchall()
data.sort(key = lambda x : x[2])
# Create data
N = len(data) #number of dots
area = np.pi*8

x = []
y = []

for entry in data: 
    x.append(datetime.datetime.strptime(entry[2][:5], "%H:%M"))
    y.append(5)

dates = matplotlib.dates.date2num(x)
plt.plot_date(dates, y, color = (0,0,0), ms = 2, label = "Report")

#create data for resets
x_reset = ["00:00","12:00", "18:00"]
y_reset = [5,5,5]
for i in range(len(x_reset)):
    x_reset[i] = datetime.datetime.strptime(x_reset[i], "%H:%M")
dates_reset = matplotlib.dates.date2num(x_reset)
plt.plot_date(dates_reset, y_reset, ms = 5, label = "Reset")

ax = plt.gca()
_format = matplotlib.dates.DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(_format)
plt.title('Rushing Analysis of IWaka')
plt.yticks([])
plt.xticks(dates_reset)

plt.gcf().autofmt_xdate()
plt.legend(["Report", "Reset"])


plt.xlabel('Time')
plt.ylabel('')
#plt.show()
plt.savefig("graph.png")
