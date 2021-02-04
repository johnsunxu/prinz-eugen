import numpy as np
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import psycopg2
import os

#Database connections
load_dotenv(dotenv_path="./dev.env")
DATABASE_URL = os.getenv('DATABASE_URL')
avrora_db = DATABASE_URL
avrora_conn = psycopg2.connect(avrora_db, sslmode="allow")
avrora_cur = avrora_conn.cursor()

#Get data
avrora_cur.execute("SELECT * FROM avrora_entries WHERE rushername= \'IWaka\' ")
data = avrora_cur.fetchall()
data.sort(key = lambda x : x[2])
# Create data
N = len(data) #number of dots

x = []
y = []
for entry in data: 
    x.append(entry[2][:5])
    y.append(5)
colors = (0, 0, 0)
area = np.pi*3

# Plot
plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.title('Rushing Analysis of IWaka')
plt.xlabel('Time')
plt.ylabel('')
plt.show()
