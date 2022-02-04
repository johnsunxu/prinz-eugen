# This file is part of Prinz Eugen.

# Prinz Eugen is free software: you can redistribute it and/or modify it under the terms
# of the GNU Affero General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# Prinz Eugen is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License along with Prinz
# Eugen. If not, see <https://www.gnu.org/licenses/>.

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json",scope)
client = gspread.authorize(creds)

sheet = client.open("Azur Lane Avrora PvP Exercise log").worksheet("Avrora")
print(sheet.cell(27,2).value.strip())
print(sheet.cell(28,2).value.strip())
print(sheet.cell(27,2).value.strip() == sheet.cell(28,2).value.strip())








#timeValues = sheet.col_values(3)
#dateValues = sheet.col_values(4)

# for i in range(len(timeValues)):
#     if i >= 17:
#         doubleDigitHour = False
#         #check hour time
#         hours = timeValues[i][0]
#         if timeValues[i][1] != ":":
#             hours+=timeValues[i][1]
#             doubleDigitHour = True

#         hours = int(hours)
#         #Check if it will go back to next day
#         if hours-15 < 0:
#             if doubleDigitHour:
#                 sheet.update_cell(i+1,9, str(24+(hours-15))+timeValues[i][2:])
#             else:
#                 sheet.update_cell(i+1,9,str(24+(hours-15)) + timeValues[i][1:])
#             newDate = int(dateValues[i][0:2])-1
#             sheet.update_cell(i+1, 10, str(newDate)+dateValues[i][2:])
#         else:

#             sheet.update_cell(i+1,9, str(hours-15) +timeValues[i][2:] )
#             sheet.update_cell(i+1, 10, dateValues[i])

#test = sheet.get_all_records()
#for i in range(len(playerName)):
#    if playerName[i] == "ZokeEstafarm":
#        print(sheet.row_values(i+1))
