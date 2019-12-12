![FreeTube Banner](images/banner.png)

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
## FreeTube's Features
### What is Discrete Mode?
Discrete Mode is ideal for usage in school. Just select *Discrete Mode* in *More Options*, paste in any website link you want it to be disguised as, type in the title for the tab, and FreeTube will run in the background of that website. To access FreeTube in Discrete Mode, click once in the bottom-left corner of the webpage, then press `Left CTRL` on your keyboard. A small box will pop up in the bottom left, and you can use FreeTube like that. Simply press `Left CTRL` again to close it.
### Why does it require verification?
FreeTube's verification system is in place solely so non-developers cannot use it. You're on GitHub, so you're probably smart enough to look at the code and immediately find out how it works, and how to get in. However, I don't want irresponsible people getting my software banned on my school's WiFi! If you can't work out how to get in, and you think you should be able to, [send me an email](mailto:william-henderson@outlook.com) and I'll hit you up with a verification code.
## Known Issues
- **UNFIXABLE: Twitch is blocked on some networks.**
  Unfortunately there is no work-around or fix for this issue. Twitch encrypts livestreams so they can only be seen on the Twitch.tv website, so the best I can do is embed a player.
- **#3 Error 500 when multiple users are streaming YouTube at once.**
  This error occurs due to YouTube temporarily throttling or blocking FreeTube from accessing its videos. This cannot be fixed without multiple layers of proxies. If anyone wants to try and fix this themselves, please open a pull request!
- **#2 Audio-only mode does not use less data than video mode**
  This is because it just puts the video file into the HTML5 `<audio>` tag. At the moment, the only solutions I've found require FFMPEG which isn't compatible with Repl.it.
