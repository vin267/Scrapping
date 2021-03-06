from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup)
seven_day = soup.find(id="seven-day-forecast")
#print(seven_day)
forecast_items = seven_day.find_all(class_="tombstone-container")
#print(forecast_items)
tonight = forecast_items[0]
#print(tonight.prettify)
period = tonight.find(class_="period-name").get_text()
short_desc = tonight.find(class_="short-desc").get_text()
temp = tonight.find(class_="temp").get_text()

img = tonight.find("img")
desc = img['title']

period_tags = seven_day.select(".tombstone-container .period-name")
periods = [pt.get_text() for pt in period_tags]

short_descs = [sd.get_text() for sd in seven_day.select(".tombstone-container .short-desc")]
temps = [t.get_text() for t in seven_day.select(".tombstone-container .temp")]
descs = [d["title"] for d in seven_day.select(".tombstone-container img")]

weather = pd.DataFrame({
    "periods": periods,
    "short_descs": short_descs,
    "temp": temps,
    "descs": descs
})
#temp_nums = weather["temp"].str.extract("(?Pd+)", expand=False)
temp_nums = weather["temp"].str.extract("(?P<num>\d+)", expand=False)
weather["temp_num"] = temp_nums.astype('int')
#print(weather["temp_num"])

#mean
#print(weather["temp_num"].mean())

#select rows that happen at night
is_night = weather["temp"].str.contains("Low")
weather["is_night"] = is_night
print(is_night)

