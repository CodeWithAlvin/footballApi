import requests
from bs4 import BeautifulSoup
import os
import datetime

try:
    os.mkdir("logos")
except:
    None

def extract(date:str):
    """
    scrape football fixture data from internet 
    parse it append to a dictonary and return it

    date: yyyyddmm [must be this format]
    
    """
    url = f"https://www.espn.in/football/fixtures/_/date/{date}"
    # date in format yyyyddmm

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'lxml')

    leauge_names = soup.find_all("h2",attrs={"class":"table-caption"})

    for leauge in leauge_names:
        raw_data = leauge.next_sibling.findAll("tr",attrs={"class":["odd","even"]})

        for item in raw_data:
            names = [abbr.get("title") for abbr in item.find_all("abbr")]
            images = [img.get("src") for img in item.find_all("img")]
            for i,name in enumerate(names):
                if not os.path.exists(f"logos/{name}.png"):
                    if images[i] == "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/default-team-logo-500.png&h=25":
                        with open("default.txt","a") as default:
                            default.write(name + "\n")
                    
                    img = requests.get(images[i])
                    name = name.replace("/","")
                    name = name.replace("\\","")
                    with open(f"logos/{name}.png","wb") as f:
                        f.write(img.content)
                        print(name)

d = datetime.datetime(2021,1,1)
delta = datetime.timedelta(days=1)
final = datetime.datetime(2021,12,31)
while d < final:
    extract(d.strftime("%Y%m%d"))
    d +=delta
    