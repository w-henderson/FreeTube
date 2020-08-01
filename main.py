# FreeTube
# Developed by William Henderson (https://github.com/w-henderson)

import pafy
import requests
from bs4 import BeautifulSoup
from flask import Flask, send_file
import re
from youtube_dl import YoutubeDL
import uyts #(https://github.com/w-henderson/Unlimited-YouTube-Search/)

def search(searchQuery,pageNumber):
    searchResults = uyts.Search(searchQuery).results
    fullSearchResults = []
    for result in searchResults:
        if result.resultType != "video":
            continue
        fullSearchResults.append([result.title,result.id,result.author,result.views,"{description not yet supported}"])

    #for i in range(5 if len(validLinks) >= 5 else len(validLinks)):
    #    v = requests.get("https://www.youtube.com/oembed?url=https://youtube.com"+validLinks[i+(5*(pageNumber-1))],timeout=5).json()
    #    fullSearchResults.append([v["title"],validLinks[i+(5*(pageNumber-1))].replace("/watch?v=",""),v["author_name"],"{views withheld for stealth}","{description withheld for stealth}"])
    #    print("PARSED https://youtube.com"+validLinks[i+(5*(pageNumber-1))])
    return fullSearchResults


app = Flask('app')

@app.route('/')
def main():
    return open("pages/app/searchPage.html").read()

@app.route('/font_bold.ttf')
def boldFont():
    return send_file("fonts/font_bold.ttf")

@app.route('/font_normal.ttf')
def normalFont():
    return send_file("fonts/font_normal.ttf")

@app.route('/icon.ico')
def icon():
    return open("images/freetube_icon.ico","rb").read()

@app.route('/app/search/<query>/<pageNumber>')
def searchPage(query,pageNumber):
    if int(pageNumber) <= 0:
        pageNumber = "1"
    returnValue = open("pages/app/results.html").read().replace("{nextPageNumber}",str(int(pageNumber)+1)).replace("{prevPageNumber}",str(int(pageNumber)-1)).replace("{query}",query)
    try:
        v = pafy.new(query)
        return '<html><body><script>window.location="/app/watch/'+v.videoid+'"</script>'
    except:
        results = search(query,int(pageNumber))
        for result in results:
            shortenedDesc = (result[4][:264] + '...') if len(result[4]) > 267 else result[4]
            #returnValue += '<div class="result"><a href="/watch/'+result[1]+'">'+result[0]+'</a><br><div class="info">'+result[2]+' | '+result[3]+' views</div>'+shortenedDesc+'</div><br>'
            returnValue += '<div class="result"><a href="/app/watch/'+result[1]+'">'+result[0]+'</a><br><div class="info">'+result[2]+' | '+result[3]+'</div></div><br>'
        returnValue += "<br><br><br><br></div></div></body></html>"
        return returnValue

@app.route('/app/watch/<video>')
def watch(video):
    #v = pafy.new(video)
    page = open("pages/app/videoPage.html").read()
    #return page.replace("{videoTitle}",v.title).replace("{videoViews}",str(v.viewcount)).replace("{videoAuthor}",v.author).replace("{videoDescription}",v.description.replace("\n","<br>")).replace("{videoSource}","/content/"+video)
    with YoutubeDL() as ydl:
      info = ydl.extract_info(video,download=False)
      return page.replace("{videoTitle}",info["title"]).replace("{videoViews}",str(info["view_count"])).replace("{videoAuthor}",info["uploader"]).replace("{videoDescription}",info["description"].replace("\n","<br>")).replace("{videoSource}","/content/"+video)

@app.route('/app/audio/<video>')
def audioOnly(video):
    v = pafy.new(video)
    page = open("pages/app/videoPage.html").read()
    return page.replace("{videoTitle}",v.title).replace("{videoViews}",str(v.viewcount)).replace("{videoAuthor}",v.author).replace("{videoDescription}",v.description.replace("\n","<br>")).replace("{videoSource}","/content/"+video).replace("<video ","<audio ").replace("</video>","</audio>")

@app.route('/content/<video>')
def content(video):
    v = pafy.new(video)
    s = v.getbest(preftype="mp4")
    u = s.url
    return requests.get(u).content

@app.route('/loading.gif')
def loading():
    return open("images/loading.gif","rb").read()

@app.route('/freetube.png')
def freetube():
    return open("images/freetube.png","rb").read()

@app.route('/icon/<name>')
def searchIcon(name):
    return send_file("images/"+name+".png")

@app.errorhandler(404)
def error404(e):
    return open("pages/app/errorPage.html","r").read().replace("{errorInfo}","The error code for this error was 404, meaning that the page you were looking for wasn't found. You may have spelt something wrong in the address bar if you manually copied a link. Check the address and try again. If that fails, make sure to contact the developer."), 404

@app.errorhandler(500)
def error500(e):
    return open("pages/app/errorPage.html","r").read().replace("{errorInfo}","The error code for this error was 500, meaning that something went wrong between a social network and us. This could be because of a mis-typed URL, or because YouTube returned no results for a search. If this problem continues, please contact the developer."), 500

@app.route('/konami.js')
def konami():
    return 'var allowedKeys={37:"left",38:"up",39:"right",40:"down",65:"a",66:"b"},konamiCode=["up","up","down","down","left","right","left","right","b","a"],konamiCodePosition=0;document.addEventListener("keydown",function(o){allowedKeys[o.keyCode]==konamiCode[konamiCodePosition]?++konamiCodePosition==konamiCode.length&&(konamiComplete(),konamiCodePosition=0):konamiCodePosition=0});'

app.run(host='0.0.0.0', port=8080)
