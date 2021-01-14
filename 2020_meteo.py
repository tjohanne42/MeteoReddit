from bs4 import BeautifulSoup
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import atexit
import random
import concurrent.futures

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

def get_soup_weather_underground(browser, url, time_wait=5, fails_max=10, display=False):
	fails = 0
	done = False
	# load the url with selenium while we can't access to htlm loaded with js
	while not done:
		if display:
			print(f"loading {url} ...")
		if fails >= fails_max:
			if display:
				print(f"too much fails : {fails}")
			return False
		browser.get(url)
		try:
			wait = WebDriverWait(browser, time_wait)
			element = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="mat-sort-header-button mat-focus-indicator ng-tns-c149-14"]')))
			try:
				soup = BeautifulSoup(browser.page_source, "lxml")
			except:
				soup = BeautifulSoup(browser.page_source, "html.parser")
			tab = soup.find("tbody", attrs={"role":"rowgroup"})
			rows = tab.find_all("tr", attrs={"role":"row"})
			done = True
		except:
			delay = random.uniform(1, 2)
			fails += 1
			if display:
				print("fail")
				print(f"waiting {delay} sec until next attempt")
			time.sleep(delay)
	if display:
		print("success")
	return soup


def scrap_meteo_from_url(browser, date, url, display=False):
	# getting the soup from the url
	soup = get_soup_weather_underground(browser, url, display=display)
	dic = 	{
			"date": [],
			"time" : [],
			"temperature" : [],
			"humidity %" : [],
			"condition" : []
			}
	if not soup:
		df = pd.DataFrame(data=dic)
		return df
	
	tab = soup.find("tbody", attrs={"role":"rowgroup"})
	rows = tab.find_all("tr", attrs={"role":"row"})
	# saving the meteo data in dic
	for row in rows:
		columns = row.find_all("td")
		i = 0
		while i < len(columns):
			if i == 0:
				time_value = columns[i].find("span", attrs={"class":"ng-star-inserted"})
				dic["time"].append(time_value.text)
				dic["date"].append(date)
			elif i == 1:
				temp = columns[i].find("span", attrs={"class":"wu-value wu-value-to"})
				temp = int(temp.text)
				temp = (temp - 32) * 5/9
				dic["temperature"].append(temp)
			elif i == 3:
				humid = columns[i].find("span", attrs={"class":"wu-value wu-value-to"})
				dic["humidity %"].append(int(humid.text))
			elif i == 9:
				cond = columns[i].find("span", attrs={"class":"ng-star-inserted"})
				dic["condition"].append(cond.text)
			i += 1
	# create df from dic
	df = pd.DataFrame(data=dic)
	return df

def scrap_meteo_from_date(browser, date, display=False):
	# getting meteo data for 4 locations in France
	orly_url = "https://www.wunderground.com/history/daily/fr/paray-vieille-poste/LFPO/date/" + date
	toulon_url = "https://www.wunderground.com/history/daily/fr/hy%C3%A8res/LFTH/date/" + date
	strasbourg_url = "https://www.wunderground.com/history/daily/fr/entzheim/LFST/date/" + date
	pleurtuit_url = "https://www.wunderground.com/history/daily/fr/pleurtuit/LFRD/date/" + date
	dfs = []

	# concurrent future threadpoolexecutor makes our four scrap silmutanuous
	f1 = concurrent.futures.ThreadPoolExecutor().submit(scrap_meteo_from_url, browser, date, toulon_url, display)
	time.sleep(random.uniform(0.5, 1.5))

	f2 = concurrent.futures.ThreadPoolExecutor().submit(scrap_meteo_from_url, browser, date, pleurtuit_url, display)
	time.sleep(random.uniform(0.5, 1.5))

	f3 = concurrent.futures.ThreadPoolExecutor().submit(scrap_meteo_from_url, browser, date, strasbourg_url, display)
	time.sleep(random.uniform(0.5, 1.5))

	f4 = concurrent.futures.ThreadPoolExecutor().submit(scrap_meteo_from_url, browser, date, orly_url, display)

	# save meteo data of the four location in a df
	df = pd.concat([f1.result(), f2.result(), f3.result(), f4.result()], ignore_index=True)
	return df

def scrap_meteo_from_dates(browser, dates, display=False):
	# getting df of meteo data for all dates
	dfs = []
	for date in dates:
		dfs.append(scrap_meteo_from_date(browser, date, display))
	return dfs

time_temp = time.time()
browser = init_selenium()

# load reddit data
path = "csv"
try:
	df_reddit = pd.read_csv(path + "/all_reddit.csv")
except:
	print("no reddit data fount in", path)
	exit()
dates = df_reddit["date"]

dates = []
# y m d
m = 1
while m <= 12:
	d = 1
	if m == 2:
		d_max = 28
	elif m % 2 == 1:
		d_max = 31
	else:
		d_max = 30
	while d <= d_max:
		dates.append("2019-" + str(m) + "-" + str(d))
		d += 1
	m += 1
# scrap meteo for each subreddit in the csv
dfs = scrap_meteo_from_dates(browser, dates, display=True)

dic = 	{
		"date":[],
		"temperature C":[],
		"humidity %":[],
		"condition":[]
		}

# making average of data collected
for df in dfs:
	dic["date"].append(df["date"][0])
	dic["temperature C"].append(df["temperature"].mean())
	dic["humidity %"].append(df["humidity %"].mean())
	dic["condition"].append(df["condition"].value_counts().index[0])

print(f"\ndone in {time.time() - time_temp} sec")

# save data in csv
df_avg = pd.DataFrame(data=dic)
df_avg.to_csv(path + '/meteo_2019_avg.csv', index=False)
print(df_avg)

print("save done in{" + path + "/meteo_2019_avg.csv}")
