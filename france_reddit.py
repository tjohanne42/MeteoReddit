import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import praw
from datetime import datetime
import random
import atexit

def user_agent():
	tab = ["Mozilla/5.0", "Linux", "Android 8.0.0", "Pixel 2 XL", "Build/OPD1.170816.004",
	"AppleWebKit/537.36", "(KHTML, like Gecko)", "Chrome/67.0.3396.87", "Mobile Safari/537.36"]
	return tab[random.randint(0, len(tab) - 1)]

def init_selenium():
	# chose a user agent
	useragent = user_agent()
	firefoxOptions = Options()
	# select headless option
	firefoxOptions.add_argument("-headless")
	profile = webdriver.FirefoxProfile()
	profile.set_preference("general.useragent.override", useragent)
	# try to load geckodriver
	try:
		browser = webdriver.Firefox(firefox_profile=profile, executable_path="geckodriver", options=firefoxOptions)
	except:
		# if geckodriver fails, try to add it to PATH
		print("selenium is not configure with geckodriver")
		done = False
		while not done:
			try:
				x = str(input("you must add geckodriver to your PATH, we can do it for you\ny/n\n"))
				if x == "y":
					path = os.getcwd() + "/bin"
					os.system("set PATH=%PATH%;" + path)
					os.system(f'export PATH="$' + path + ':$PATH"')
					done = True
				elif x == "n":
					exit()
			except:
				pass
		try:
			# retry to load geckodriver
			browser = webdriver.Firefox(firefox_profile=profile, executable_path="geckodriver", options=firefoxOptions)
		except:
			print("an error occured")
			exit()
	# atexit we unload geckodriver
	atexit.register(browser.quit)
	return browser

def webscroll():
	SCROLL_PAUSE_TIME = 2
	# Get scroll height
	last_height = browser.execute_script("return document.body.scrollHeight")
	while True:
		# Scroll down to bottom
		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)
		# Calculate new scroll height and compare with last scroll height
		new_height = browser.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height

browser = init_selenium()
#url = "https://www.reddit.com/r/france/search/?q=Mercredi%2BTech&sort=new&restrict_sr=on&type=link"
url = "https://www.reddit.com/search/?q=r%2Ffrance"

# getting all div of subreddit of a research on reddit
# try to get it 5 times so get the good numbers of div
attempts = 0
done = False
max_len = 0
while not done:
	browser.get(url)
	webscroll()
	soup = BeautifulSoup(browser.page_source, 'lxml')
	#blbl = soup.find_all("div", attrs={"class":"_1Y6dfr4zLlrygH-FLmr8x-"})
	blbl = soup.find_all("div", attrs={"class":"_1poyrkZ7g36PawDueRza-J"})
	if attempts >= 5:
		if len(blbl) >= max_len:
			done = True
	elif len(blbl) > max_len:
		max_len = len(blbl)
	attempts += 1
	print("attempt", attempts)

"""
# for each div we get the link to the subreddit
# only get link from "mercredi tech" subreddit
links = []
for x in blbl:
	not_valid = False
	aSQn = x.find_all("a", attrs={"class":"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
	for i in aSQn:
		title = i.find("span").text
		if title.find("Mercredi Tech") == -1:
			not_valid = True
	if not not_valid:
		a_3j = x.find_all("a", attrs={"class":"_3jOxDPIQ0KaOWpzvSQo-1s"})
		for i in a_3j:
			links.append(i["href"])
"""

# for each div we get the link to the subreddit
# only get link from "mercredi tech" subreddit
links = []
for x in blbl:
	not_valid = False
	#r_backslash = x.find("a", attrs={"class":"_3ryJoIoycVkA88fy40qNJc _1L0pdcPf58t25Jy6ljHIKR"}).text
	#if r_backslash == "r/france":
	i = x.find("a", attrs={"class":"SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"})
	links.append("https://www.reddit.com" + i["href"])

print(f"loading links done: {len(links)}")

# init praw to scrap reddit
reddit = praw.Reddit(client_id='xuvYAAO_XUjgAw', 
					 client_secret='gVbYLagT4DIjBmEv1ovqhUuQ1hgQTA', 
					 user_agent='soupy1', 
					 username='blblsoupy3', 
					 password='blblsoupy3')

sub =   {
        "date": [],
        "name": [],
        "score": [],
        "nb com": []
        }

dfs = []

x = 0
# for each link we get date name score and nb com
# only get info on links from chuckMauriceFacts user
for link in links:
    submission = reddit.submission(url=link)
    #if submission.author != "ChuckMauriceFacts":
    #    continue
    sub_comment =   {
                    "score":[],
                    "date":[]
                    }
    nb_com = 0
    date = datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d')
    sub["date"].append(date)
    sub["score"].append(submission.score)
    title = submission.title
    pos = title.find("/")
    if pos != -1:
        lst = list(title)
        lst[pos] = ' '
        title = ''.join(lst)
    sub["name"].append(title)
    for s in submission.comments:
        try:
            sub_comment["score"].append(s.score)
            date = datetime.utcfromtimestamp(s.created_utc).strftime('%Y-%m-%d')
            sub_comment["date"].append(date)
            nb_com = nb_com + 1
        except:
            print("type more comment found")
    sub["nb com"].append(nb_com)
    dfs.append(pd.DataFrame(data=sub_comment))
    print(f"link {x} done")
    x += 1

# save datas in csv
path = "csv"
try:
    listdir = os.listdir(path)
except:
    os.mkdir(path)
try:
    listdir = os.listdir(path + "/france_comment_reddit")
except:
    os.mkdir(path + "/france_comment_reddit")
df_sub = pd.DataFrame(data=sub)
print(df_sub)
df_sub.to_csv(path + "/france_all_reddit.csv", index=False)
x = 0
for df in dfs:
    df.to_csv(path + "/comment_reddit/" + sub["name"][x] + ".csv", index=False)
    x += 1

print("save done in{" + path + "/france_all_reddit.csv}")
