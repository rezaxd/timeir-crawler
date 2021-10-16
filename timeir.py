import requests as req
from bs4 import BeautifulSoup as BS
import json
from datetime import datetime
from persiantools.jdatetime import JalaliDate
from requests.api import request

main_url = "https://www.time.ir/fa/event/list/0"
year = 1400

req_url= "http://localhost:8000/v1/holiday"
years = "1400"

holidays = []

for i in range(12, 13):
    if i == 12:
        for j in range(8, 12):
            print(f"Date: {year}-{i}-{j}")
            _day_event = req.get(f"{main_url}/{year}/{i}/{j}")
            req_text_to_bs = BS(_day_event.text, "html.parser")
            holiday = req_text_to_bs.select(".eventHoliday")
            if len(holiday) != 0:
                title = holiday[0].text
                jalali=JalaliDate(year,i,j).to_gregorian()
                strjalali=jalali.strftime('%Y-%m-%d')
                print(strjalali)
                paramReq={'title':title, 'date':strjalali}
                req.post(f"{req_url}",data=paramReq)
                holidays.append(title)
    if i <= 6:
        for j in range(1, 32):
            print(f"Date: {year}-{i}-{j}")
            _day_event = req.get(f"{main_url}/{year}/{i}/{j}")
            req_text_to_bs = BS(_day_event, "html.parser")
            holiday = req_text_to_bs.select(".eventHoliday")
            if len(holiday) != 0:
                print(holiday[0].text)
                holidays.append(holiday[0].text)
    if i > 6 and i != 12:
        for j in range(1, 31):
            print(f"Date: {year}-{i}-{j}")
            _day_event = req.get(f"{main_url}/{year}/{i}/{j}")
            req_text_to_bs = BS(_day_event.text, "html.parser")
            holiday = req_text_to_bs.select(".eventHoliday")
            if len(holiday) != 0:
                holidays.append(holiday[0].text)



res = json.dumps({"holidays": holidays})

with open(f"holidays-{year}.json", 'w') as f:
    f.write(res)
