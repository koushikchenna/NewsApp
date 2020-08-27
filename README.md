# NewsApp
A personalized news application with article based bias
- Use pip install newspaper3k to get newspaper python library(get articles)
- This file should be inside this folder but due to GitHub file upload limits cannot be pushed
- Other libraries to include geocoder, Textblob, requests, paginator, render
- There are three api libraries used: 
- For live weather data: http://api.openweathermap.org
- For live covid data: https://api.covid19api.com/summary
- For live news data api = NewsApiClient

My app is called NewsApp, a personalized news source dedicated to giving you personalized news with respect to bias. 
With increasing polarization from news sources all around the world, I want to help give readers an informed source of how much a news article may be biased. 
Instead of a standardard political left versus right bias, I use Natural Language Processing to identify the article content and point out subjectivity and polarity.
Like posts with the "heart" in the search section to get more related news about that topic and use the "thumbsdown" button to see less posts like this.


Things that make my project sufficently different and more advanced in difficulty is because of the "bubble" style organization for the news and the on display block for the text that pops out as an extension.
Additionally, there are roughly 7-8 models that control user data and news data. I have also accessed several API's and parsed several json responses for live time data. I have also used a more complicated and elegent fade in animation for the news to display when the pagination link is clicked.
I also deal with live time data and active location weather data.

In the Newsapp folder: 
- Basic Django settings
In the NewsList folder: 
- Migration files
- JS file and CSS file for design
- HTML templates for webpage
- admin.py
  - register models
- apps.py 
  - define apps 'newslist'
- models.py
  - define models used in the app
- urls.py 
  - define url pathways used in the app
- views.py
  - defines main python code with all the functions 
In the external Newspaper folder: 
  - https://github.com/codelucas/newspaper/
  - based on operating systems, download instructions may vary
  - One issue prevalent in the newspaper library is the fact that paywalled articles do not give the correct response. 
  - The News API also does not allow me to get the article content for free 
