import requests
import json
import io

#Get the ship database
j = requests.get('https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/ships.json').content
skills = json.loads(j)
f = open("data/ships.json", "w")
f.write(json.dumps(skills))
f.close()
del f

#Get the ship type database
j = requests.get('https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/types.json').content
types = json.loads(j)
f = open("data/types.json", "w")
f.write(json.dumps(types))
f.close()
del f

#Get the ship retrofit database
content = requests.get('https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/retrofit.json').content
f = open("data/retrofit.json", "w")
f.write(content.decode('utf-8'))
f.close()
del f


#Get the ship skill database
j = requests.get('https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/skills.json').content
skills = json.loads(j)
f = open("data/skills.json", "w")
f.write(json.dumps(skills))
f.close()
del f

#Get the ship nickname database
## TODO: Change github host location
content = requests.get('https://raw.githubusercontent.com/Drakomire/Perseus.py/main/data/nicknames.py').content
f = open("classes/nicknames.py", "w")
f.write(content.decode('utf-8'))
f.close()
del f

#Get the ship lookup table
content = requests.get('https://raw.githubusercontent.com/Drakomire/perseus-data/master/dist/lookup_table.json').content
f = open("data/lookup_table.json", "w")
f.write(content.decode('utf-8'))
f.close()
del f
