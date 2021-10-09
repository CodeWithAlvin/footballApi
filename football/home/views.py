from django.shortcuts import render,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import datetime
import requests
from bs4 import BeautifulSoup

# Create your views here.

# return api view
@api_view(['GET'])
def api(request,slug):
    try:
        if datetime.datetime.strptime(str(slug), '%Y%m%d'):
            return Response( get_fixtures(str(slug)) )

    except:
        return Response("an error occured date must be in format yyyymmdd",status=404)

# return homepage of website
def home(request):
    if request.method == "POST":
        date = request.POST.get("date").replace("-","")
    else:
        date = datetime.date.today().strftime("%Y%m%d")

    return render(request,"index.html",context={"data": get_fixtures(date), "date":f"{date[6:]} {date[4:6]} {date[:4]}'s"})


# function for scraping data
def get_fixtures(date:str):
    """
    scrape football fixture data from internet 
    parse it append to a dictonary and return it

    date: yyyyddmm [must be this format]
    
    """
    url = f"https://www.espn.in/football/fixtures/_/date/{date}"
    # date in format yyyyddmm

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'lxml')

    data={}

    leauge_names = soup.find_all("h2",attrs={"class":"table-caption"})

    for leauge in leauge_names:
        lg_name = leauge.text
        raw_data = leauge.next_sibling.findAll("tr",attrs={"class":["odd","even"]})

        data[lg_name]=[]

        for item in raw_data:
            names = [abbr.get("title") for abbr in item.find_all("abbr")]
            images = [img.get("src") for img in item.find_all("img")]
            timing = [date.get("data-date") for date in item.find_all("td",attrs={"data-behavior":"date_time"})]
            score = [score.text for score in item.find_all("span",attrs={"class":"record"})]
            # checking for live
            if timing == []:
                timing = ["live" for _ in item.find_all("td",attrs={"class":"live"})]
            # checking for TBD
            if timing == []:
                timing = [time.text for time in item.find_all("a",attrs={"name":"&lpos=null:schedule:time"})]

            # checking for postponed
            if timing == []:
                timing = [time.text for time in item.find_all("a",attrs={"name":"&lpos=null:schedule:score"}) if time.text == "Postponed"]

            if names == [] and images == [] and timing == []:
                continue
        
            data[lg_name].append({
                "teams":names,
                "logos":images,
                "timing":timing,
                "score":score,
                })

    return data

