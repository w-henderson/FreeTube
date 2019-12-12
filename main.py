# FreeTube
# Developed by William Henderson (https://github.com/w-henderson)

import pafy
import requests
from bs4 import BeautifulSoup
from flask import Flask, send_file
import re

def search(searchQuery,pageNumber):
    doc = requests.get("http://youtube.com/search?q="+searchQuery).content
    searchResults = BeautifulSoup(doc,'html.parser')

    validLinks = []
    for link in searchResults.find_all('a'):
        u = link.get('href')
        if u[0:9] == "/watch?v=" and "&list" not in u:
            validLinks.append(u)

    validLinks = list(dict.fromkeys(validLinks)) # Removed duplicates
    print(validLinks)

    fullSearchResults = []
    for i in range(5):
        #v = pafy.new("https://youtube.com"+validLinks[i+(5*(pageNumber-1))])
        v = requests.get("https://youtube.com"+validLinks[i+(5*(pageNumber-1))]).text
        textTitle = re.search('<title>(.*?)</title>',v).group(1).replace(" - YouTube","")
        fullSearchResults.append([textTitle,validLinks[i+(5*(pageNumber-1))].replace("/watch?v=",""),"{channel withheld for stealth}","{views withheld for stealth}","{description withheld for stealth}"])
        print("PARSED https://youtube.com"+validLinks[i+(5*(pageNumber-1))])
    return fullSearchResults


app = Flask('app')

@app.route('/app/main')
def main():
    return open("pages/app/searchPage.html").read()

@app.route('/discrete/main')
def discreteMain():
    return open("pages/discrete/searchPage.html").read()

@app.route('/')
def verification():
    return open("pages/app/verify.html").read()

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
            returnValue += '<div class="result"><a href="/app/watch/'+result[1]+'">'+result[0]+'</a><br><div class="info"><i><span onclick="window.location=\'/app/audio/'+result[1]+'\'">Click here for an audio-only stream which, depending on your browser, may save data.</span></i></div></div><br>'
        returnValue += "<br><br><br><br></div></div></body></html>"
        return returnValue

@app.route('/discrete/search/<query>/<pageNumber>')
def discreteSearchPage(query,pageNumber):
    if int(pageNumber) <= 0:
        pageNumber = "1"
    returnValue = open("pages/discrete/resultsPage.html").read().replace("{nextPageNumber}",str(int(pageNumber)+1)).replace("{prevPageNumber}",str(int(pageNumber)-1)).replace("{query}",query)
    try:
        v = pafy.new(query)
        return '<html><body><script>window.location="/discrete/watch/'+v.videoid+'"</script>'
    except:
        results = search(query,int(pageNumber))
        for result in results:
            shortenedDesc = (result[4][:264] + '...') if len(result[4]) > 267 else result[4]
            #returnValue += '<div class="result"><a href="/watch/'+result[1]+'">'+result[0]+'</a><br><div class="info">'+result[2]+' | '+result[3]+' views</div>'+shortenedDesc+'</div><br>'
            returnValue += '<a href="/discrete/watch/'+result[1]+'">'+result[0]+'</a><br>'
        returnValue += "</div><div class=\"keypressFinder\"></div></body></html>"
        return returnValue

@app.route('/app/twitter/<profile>')
def twitter(profile):
	tweetData = requests.get("https://twitter.com/"+profile)
	tweetsText = ""
	html = BeautifulSoup(tweetData.text, 'html.parser')
	timeline = html.select('#timeline li.stream-item')
	for tweet in timeline:
		tweet_id = tweet['data-item-id']
		tweet_text = tweet.select('p.tweet-text')[0].get_text(separator='').replace("https://"," https://").replace("http://"," http://").replace("pic.twitter.com"," pic.twitter.com").replace("\n","<br>").strip()
		if tweet.select('span.js-retweet-text'):
			tweetsText += "<div class='tweet'><img src='/icon/retweet'><b>Retweet from "+tweet.select('strong.fullname')[0].get_text()+"</b>:<br>"+tweet_text+"</div><hr>"
		else:
			tweetsText += "<div class='tweet'><img src='/icon/twitter'>"+tweet_text+"</div><hr>"
	
	page = open("pages/app/twitterPage.html").read()
	return page.replace("{profileName}",profile).replace("{tweets}",tweetsText)

@app.route('/app/watch/<video>')
def watch(video):
    v = pafy.new(video)
    page = open("pages/app/videoPage.html").read()
    return page.replace("{videoTitle}",v.title).replace("{videoViews}",str(v.viewcount)).replace("{videoAuthor}",v.author).replace("{videoDescription}",v.description.replace("\n","<br>")).replace("{videoSource}","/content/"+video)

@app.route('/app/audio/<video>')
def audioOnly(video):
    v = pafy.new(video)
    page = open("pages/app/videoPage.html").read()
    return page.replace("{videoTitle}",v.title).replace("{videoViews}",str(v.viewcount)).replace("{videoAuthor}",v.author).replace("{videoDescription}",v.description.replace("\n","<br>")).replace("{videoSource}","/content/"+video).replace("<video ","<audio ").replace("</video>","</audio>")

@app.route('/discrete/watch/<video>')
def discreteWatch(video):
    v = pafy.new(video)
    page = open("pages/discrete/videoPage.html").read()
    return page.replace("{videoTitle}",v.title).replace("{videoViews}",str(v.viewcount)).replace("{videoAuthor}",v.author).replace("{videoSource}","/content/"+video)+"</div><div class=\"keypressFinder\"></div></body></html>"

@app.route('/content/<video>')
def content(video):
    v = pafy.new(video)
    s = v.getbest(preftype="mp4")
    u = s.url
    return requests.get(u).content

@app.route('/app/twitch/<channel>')
def twitch(channel):
    page = open("pages/app/twitchPage.html").read()
    return page.replace("{channelName}",channel)

@app.route('/app/instagram/<username>')
def instagram(username):
    false = False
    true = True
    null = 0
    page = open("pages/app/instaPage.html").read()
    userData = eval(requests.get("https://www.instagram.com/"+username+"/?__a=1").text)["graphql"]["user"]
    posts = [post["node"]["shortcode"] for post in userData["edge_owner_to_timeline_media"]["edges"]]
    imageString = ""
    for i in range(len(posts)):
        imageString += "<a href='/app/instagramPhoto/"+username+"/"+str(i)+"'><img class='photo' src='/instagramContent/"+posts[i]+"/0'></a>"
    if userData["is_private"]:
        imageString = "Private Account"
    return page.replace("{username}",username).replace("{fullname}",userData["full_name"]).replace("{followers}",str(userData["edge_followed_by"]["count"])).replace("{bio}",userData["biography"]).replace("{posts}",imageString).encode("utf-16","ignore")

@app.route('/instagramContent/<photoID>/<hd>')
def instaContent(photoID,hd):
    if hd == "1":
        return requests.get("https://instagram.com/p/"+photoID+"/media?size=l").content
    else:
        return requests.get("https://instagram.com/p/"+photoID+"/media").content

@app.route('/app/instagramPhoto/<username>/<photoNumber>')
def instaPhoto(username,photoNumber):
    false = False
    true = True
    null = 0
    page = open("pages/app/instaPhotoPage.html").read()
    userData = eval(requests.get("https://www.instagram.com/"+username+"/?__a=1").text)["graphql"]["user"]
    posts = [post["node"] for post in userData["edge_owner_to_timeline_media"]["edges"]]
    selectedPost = posts[int(photoNumber)]
    location = ""
    if selectedPost["location"] != 0:
        location = " | "+selectedPost["location"]["name"]
    return page.replace("{imageURL}","/instagramContent/"+selectedPost["shortcode"]+"/1").replace("{username}",username).replace("{description}",selectedPost["edge_media_to_caption"]["edges"][0]["node"]["text"].replace("\n","<br>")).replace("{likes}",str(selectedPost["edge_liked_by"]["count"])).replace("{location}",location).encode("utf-16","ignore")

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
    return open("pages/app/errorPage.html","r").read().replace("{errorInfo}","The error code for this error was 500, meaning that something went wrong between a social network and us. This could be because of a mis-typed Instagram or Twitch username, or because YouTube returned no results for a search. If this problem continues, please contact the developer."), 500

@app.route('/konami.js')
def konami():
    return 'var allowedKeys={37:"left",38:"up",39:"right",40:"down",65:"a",66:"b"},konamiCode=["up","up","down","down","left","right","left","right","b","a"],konamiCodePosition=0;document.addEventListener("keydown",function(o){allowedKeys[o.keyCode]==konamiCode[konamiCodePosition]?++konamiCodePosition==konamiCode.length&&(konamiComplete(),konamiCodePosition=0):konamiCodePosition=0});'

app.run(host='0.0.0.0', port=8080)
