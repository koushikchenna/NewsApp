from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from newsapi import NewsApiClient
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .models import hotnews, searchnews, idnews, mynews
from newslist.models import *
import requests, json
import newspaper
from newspaper import Config
import urllib3
from newspaper import Article
from textblob import TextBlob
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
import geocoder
import requests
import sports
total_confirmed = None
new_deaths = None
new_confirmed = None
total_deaths = None
new_recovered = None
total_discovered = None
date = None
location = None
def index(request):
    api = NewsApiClient(api_key='6fb766f0d7ec43c2b412b9a4fc88a64b')
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    myloc = geocoder.ip('me')
    lati = myloc.lat
    longi = myloc.lng
    f_url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + "770fdaded25c020b900de22ab272b41a" + "&lat=" + str(lati) + "&lon=" + str(longi)
    weather_data = requests.get(f_url).json()
    max_temp = weather_data['main']['temp_max']
    max_temp = ((max_temp - 273) * 1.8) + 32
    min_temp = weather_data['main']['temp_min']
    min_temp = ((min_temp - 273) * 1.8) + 32
    temp = weather_data['main']['temp']
    temp = ((temp - 273) * 1.8) + 32
    responses = requests.get("https://api.covid19api.com/summary", verify = False)
    data = responses.json()
    #print(data['Countries'])
    x = 0
    alldata = data['Countries']
    for data in alldata:
        if alldata[x]['Country'] == "United States of America":
            #print(alldata[x]['TotalConfirmed'])
            total_confirmed = alldata[x]['TotalConfirmed']
            new_deaths = alldata[x]['NewDeaths']
            new_confirmed = alldata[x]['NewConfirmed']
            total_deaths = alldata[x]['TotalDeaths']
            new_recovered = alldata[x]['NewRecovered']
            total_recovered = alldata[x]['TotalRecovered']
            date = alldata[x]['Date']
            break
        else:
            x = x + 1
    request.session['name']= weather_data['name']
    hotn = api.get_top_headlines()
    lst_titles = []
    lst_authors = []
    lenval = len(hotn['articles'])
    #print(lenval)
    hotnews.objects.all().delete()
    z = 0
    while z < lenval:
        title = hotn['articles'][z]['title']
        author = hotn['articles'][z]['author']
        source = hotn['articles'][z]['source']['name']
        description = hotn['articles'][z]['description']
        #content = hotn['articles'][z]['content']
        urls = hotn['articles'][z]['url']
        imgurl = hotn['articles'][z]['urlToImage']
        article = Article(url = urls, language='en')
        try:
            article.download()
            article.parse()
            #print(article.text)
            content = article.text
            leaning = TextBlob(content)
            lean = leaning.sentiment.polarity
            polar = leaning.sentiment.subjectivity
            #print(lean)
            #print(polar)
            if (source != "Buzzfeed"):
                new_news = hotnews(title = title, source = source, author = author, description = description, content=content, lean=lean, polar=polar)
                new_news.save()
            #print(source)
            z = z + 1
        except:
            z = z + 1
            continue;
    news = hotnews.objects.get_queryset().order_by('id')
    length = len(news)
    #print(length)
    paginator = Paginator(news, 4)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    all_matches = sports.all_matches()
    baseball = all_matches['basketball']
    print(baseball)
    return render(request, "newslist/index.html", {
        "news": news,
        "max_temp": max_temp,
        "min_temp": min_temp,
        "temp": temp,
        "location": location,
        "new_deaths": new_deaths,
        "new_confirmed": new_confirmed,
        "total_confirmed": total_confirmed,
        "total_deaths": total_deaths,
        "new_deaths": new_deaths,
        "new_recovered": new_recovered,
        "total_recovered": total_recovered,
        "date": date
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "newslist/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "newslist/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "newslist/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "newslist/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "newslist/register.html")

def persnews(request, username):
    api = NewsApiClient(api_key='6fb766f0d7ec43c2b412b9a4fc88a64b')
    allpernews = keyword.objects.all()
    mynews.objects.all().delete()
    for all in allpernews:
        if all.username == username:
            print(all.keyword)
            favnews = api.get_everything(q = all.keyword)
            cnt = 0
            while cnt < 2:
                title = favnews['articles'][cnt]['title']
                author = favnews['articles'][cnt]['author']
                source = favnews['articles'][cnt]['source']['name']
                description = favnews['articles'][cnt]['description']
                urls = favnews['articles'][cnt]['url']
                imgurl = favnews['articles'][cnt]['urlToImage']
                article = Article(url = urls, language='en')
                article.download()
                article.parse()
                content = article.text
                leaning = TextBlob(content)
                lean = leaning.sentiment.polarity
                polar = leaning.sentiment.subjectivity
                print(lean)
                print(polar)
                new_news = mynews(title = title, source = source, author = author, description = description, content=content, imgurl=imgurl, urls=urls, lean=lean, polar=polar)
                new_news.save()
                cnt = cnt + 1
    allnews = mynews.objects.all()
    print(allnews)
    paginator = Paginator(allnews, 5)
    page = request.GET.get('page')
    allnews = paginator.get_page(page)
    myloc = geocoder.ip('me')
    lati = myloc.lat
    longi = myloc.lng
    f_url = "http://api.openweathermap.org/data/2.5/weather?" + "appid=" + "770fdaded25c020b900de22ab272b41a" + "&lat=" + str(lati) + "&lon=" + str(longi)
    weather_data = requests.get(f_url).json()
    max_temp = weather_data['main']['temp_max']
    max_temp = ((max_temp - 273) * 1.8) + 32
    min_temp = weather_data['main']['temp_min']
    min_temp = ((min_temp - 273) * 1.8) + 32
    temp = weather_data['main']['temp']
    temp = ((temp - 273) * 1.8) + 32
    responses = requests.get("https://api.covid19api.com/summary", verify = False)
    data = responses.json()
    print(data['Countries'])
    x = 0
    alldata = data['Countries']
    for data in alldata:
        if alldata[x]['Country'] == "United States of America":
            print(alldata[x]['TotalConfirmed'])
            total_confirmed = alldata[x]['TotalConfirmed']
            new_deaths = alldata[x]['NewDeaths']
            new_confirmed = alldata[x]['NewConfirmed']
            total_deaths = alldata[x]['TotalDeaths']
            new_recovered = alldata[x]['NewRecovered']
            total_recovered = alldata[x]['TotalRecovered']
            date = alldata[x]['Date']
            break
        else:
            x = x + 1
    location = weather_data['name']
    return render(request, "newslist/persnews.html", {
        "persnews": mynews.objects.all(),
        "max_temp": max_temp,
        "min_temp": min_temp,
        "temp": temp,
        "location": location,
        "new_deaths": new_deaths,
        "new_confirmed": new_confirmed,
        "total_confirmed": total_confirmed,
        "total_deaths": total_deaths,
        "new_deaths": new_deaths,
        "new_recovered": new_recovered,
        "total_recovered": total_recovered,
        "date": date
    })

def bytopic(request):
    return render(request, "newslist/bytopic.html", {
        "state": "false"
    })

def bytopicres(request):
    api = NewsApiClient(api_key='6fb766f0d7ec43c2b412b9a4fc88a64b')
    search = request.GET['search']
    print(search)
    searchn = api.get_everything(q = search)
    lennews = len(searchn['articles'])
    searchnews.objects.all().delete()
    idnews.objects.all().delete()
    placeholder = 0
    addcount = 0
    while placeholder < lennews:
        title = searchn['articles'][placeholder]['title']
        author = searchn['articles'][placeholder]['author']
        source = searchn['articles'][placeholder]['source']['name']
        description = searchn['articles'][placeholder]['description']
        #content = hotn['articles'][z]['content']
        urls = searchn['articles'][placeholder]['url']
        article = Article(url = urls, language='en')
        article.download()
        article.parse()
        #print(article.text)
        content = article.text
        leaning = TextBlob(content)
        lean = leaning.sentiment.polarity
        polar = leaning.sentiment.subjectivity
        print(lean)
        print(polar)
        if (len(content) > 750):
            addcount = addcount + 1
            new_news = searchnews(title = title, source = source, author = author, description = description, content=content, urls=urls, lean=lean, polar=polar)
            new_news.save()
            #print(source)
            new_news = idnews(title = title, idtitle = addcount)
            new_news.save()
        placeholder = placeholder + 1
    news = searchnews.objects.all()
    val = idnews.objects.all()
    return render(request, "newslist/bytopic.html", {
        "news": news,
        "state": "true",
        "given_val": search,
        "val": val
    })

@csrf_exempt
def result(request, titlevalue):
    titlevalue = titlevalue.replace("-", " ")
    print(titlevalue)
    #print(uname)
    selected = searchnews.objects.get(title = titlevalue)
    designurl = selected.urls
    article = Article(designurl)
    article.download()
    article.parse()
    article.nlp()
    results = article.keywords
    user = User.objects.all()
    print(titlevalue)
    #txt = "hello"
    return JsonResponse({"txt": results})

def allvals(request):
    lsttitle = {}
    titles = idnews.objects.all()
    for t in titles:
        resp = t.title
        id = t.idtitle
        lsttitle.update({id: resp})
        #print(first_article.keywords)
    print(lsttitle)
    return JsonResponse({"resp": lsttitle})

def addto(request, holdval, uname):
    print(holdval)
    print(uname)
    newvalue = keyword(username = uname, keyword = holdval)
    newvalue.save()
    txt = "submitted"
    return JsonResponse({"txts": txt})

def remove(request, nameedit):
    nameedit = nameedit.replace("-", " ")
    print(nameedit)
    allnews = mynews.objects.all()
    for a in allnews:
        if a.title == nameedit:
            desurl = a.urls
            article = Article(url = desurl, language='en')
            article.download()
            article.parse()
            article.nlp()
            res = article.keywords
            break;
    print(res)
    for r in res:
        keyword.objects.filter(keyword = r).delete()
        rmv = "removed"
    return JsonResponse({"rmv": rmv})
def settings(request):
    allsetting = usersettings.objects.all()
    return render(request, "newslist/settings.html", {
        "setting": allsetting
    })

def corona(request, uname):
    allsetting = usersettings.objects.all()
    print(uname)
    for all in allsetting:
        if all.user == uname:
            if all.setting == "corona":
                print("i made it here")
                usersettings.objects.filter(user = uname, setting = "corona").delete()
                return render(request, "newslist/settings.html", {
                    "setting": allsetting,
                })
            else:
                print("i made it to this add statement")
                usersettings.objects.filter(user = uname, setting = "corona").delete()
                newvalue = usersettings(user = uname, setting = "corona")
                newvalue.save()
    if usersettings.objects.count() == 0:
        newvalue = usersettings(user = uname, setting = "corona")
        newvalue.save()
        print("over here")
    return render(request, "newslist/settings.html", {
        "setting": allsetting,
    })

def sports(request, uname):
    allsetting = usersettings.objects.all()
    print(uname)
    for all in allsetting:
        if all.user == uname:
            if all.setting == "sports":
                print("i made it here")
                usersettings.objects.filter(user = uname, setting = "sports").delete()
                return render(request, "newslist/settings.html", {
                    "setting": allsetting,
                })
            else:
                print("i made it to this add statement")
                usersettings.objects.filter(user = uname, setting = "sports").delete()
                newvalue = usersettings(user = uname, setting = "sports")
                newvalue.save()
    if usersettings.objects.count() == 0:
        newvalue = usersettings(user = uname, setting = "sports")
        newvalue.save()
        print("over here")
    return render(request, "newslist/settings.html", {
        "setting": allsetting,
    })

def weather(request, uname):
    allsetting = usersettings.objects.all()
    print(uname)
    for all in allsetting:
        if all.user == uname:
            if all.setting == "weather":
                print("i made it here")
                usersettings.objects.filter(user = uname, setting = "weather").delete()
                return render(request, "newslist/settings.html", {
                    "setting": allsetting,
                })
            else:
                print("i made it to this add statement")
                usersettings.objects.filter(user = uname, setting = "weather").delete()
                newvalue = usersettings(user = uname, setting = "weather")
                newvalue.save()
    if usersettings.objects.count() == 0:
        newvalue = usersettings(user = uname, setting = "weather")
        newvalue.save()
        print("over here")
    return render(request, "newslist/settings.html", {
        "setting": allsetting,
    })