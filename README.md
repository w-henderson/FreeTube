![FreeTube Banner](images/banner.png)
[![Run on Repl.it](https://repl.it/badge/github/w-henderson/FreeTube)](https://repl.it/github/w-henderson/FreeTube)

# FreeTube
**FreeTube is currently hosted on my [Repl.it](https://freetube.cooltomato.repl.co/) account, and some of its features are only available when hosted on Repl.it.**
## What is FreeTube?
FreeTube is a limitless, uncensored, unfiltered platform for social media. Whether you live in China and want to watch PewDiePie, or just want to listen to music on YouTube while you're behind your school's filter, FreeTube has you covered.
### How does FreeTube work?
FreeTube runs on Repl.it, a website which allows you to run code and host websites. Using Repl.it as a proxy, FreeTube streams content from multiple social networks straight to your device, so you can enjoy your content anywhere with no limitations. FreeTube also stores your content in Repl.it's RAM rather than storage while you are using it, meaning quicker response times and a snappier interface.
### Is it even legal?
If VPNs are legal in your country, then yes. FreeTube acts similar to a browser-based VPN, redirecting traffic around filters to your device. However, you must not use FreeTube to download music off YouTube, as this is against YouTube's terms of service.
### Why does it exist?
That's a deep question! I made FreeTube in my Computer Science class in high school, because I was bored and wanted to watch YouTube. It's that simple, just a bored nerd wanting to do something productive.
## Known Issues
- [#3](https://github.com/w-henderson/FreeTube/issues/3) **Error 500 when multiple users are streaming YouTube at once.**
  This error occurs due to YouTube temporarily throttling or blocking FreeTube from accessing its videos. This cannot be fixed without multiple proxies. If anyone wants to try and fix this themselves, please open a pull request!
- [#2](https://github.com/w-henderson/FreeTube/issues/2) **Audio-only mode does not use less data than video mode**
  This is because it just puts the video file into the HTML5 `<audio>` tag. At the moment, the only solutions I've found require FFMPEG which isn't compatible with Repl.it.
