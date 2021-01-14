import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

df_reddit = pd.read_csv('csv/all_reddit.csv')
df_meteo = pd.read_csv('csv/meteo_avg.csv')

df = df_reddit.merge(df_meteo, how='outer', on='date')
df = df.sort_values(by=["date"])

df.loc[df["condition"] == "Fair", "condition"] = 0
df.loc[df["condition"] == "Cloudy", "condition"] = 1
df.loc[df["condition"] == "Partly Cloudy", "condition"] = 1
df.loc[df["condition"] == "Mostly Cloudy", "condition"] = 1
df.loc[df["condition"] == "Fog", "condition"] = 1
df.loc[df["condition"] == "Mist", "condition"] = 1
df.loc[df["condition"] == "Light Rain", "condition"] = 1

print(df["condition"].value_counts())
df = df.astype({"condition":"int32"})
df["date"] = pd.to_datetime(df["date"])

print(df.head())

print(df.info())

print(df.describe())

print(df.corr())

heatmap = df.corr()
sns.heatmap(heatmap, cmap= sns.color_palette('viridis'), linewidths=2)
plt.show()

df.hist(figsize=(10,10))
plt.tight_layout()
plt.show()

name1 = 'date'
name2 = 'score'
sc = plt.plot(df[name1], df[name2])
sc = plt.scatter(x=df[name1], y=df[name2], s=100, alpha=1)
plt.xlabel(f"{name1}")
plt.ylabel(f"{name2}")
plt.title(f"{name1} / {name2}")
plt.show()

name1 = 'score'
name2 = 'temperature C'
sc = plt.scatter(x=df[name1], y=df[name2], s=100, alpha=1, c=-df[name2])
#sc = plt.scatter(x=df[name1], y=df["condition"], s=100, alpha=1, c=['red'])
plt.xlabel(f"{name1}")
plt.ylabel(f"{name2}")
plt.title(f"{name1} / {name2}")
plt.grid()
plt.show()

name2 = "humidity %"
sc = plt.scatter(x=df[name1], y=df[name2], s=100, alpha=1, c=-df[name2])
plt.xlabel(f"{name1}")
plt.ylabel(f"{name2}")
plt.title(f"{name1} / {name2}")
plt.grid()
plt.show()

name2 = "condition"
sc = plt.scatter(x=df[name1], y=df[name2], s=100, alpha=1, c=-df[name2])
plt.xlabel(f"{name1}")
plt.ylabel(f"{name2} 0 good 1 bad")
plt.title(f"{name1} / {name2}")
plt.grid()
plt.show()


name1 = 'nb com'
name2 = 'temperature C'
sc = plt.scatter(x=df[name1], y=df[name2], s=100, alpha=1, c=-df[name2])
#sc = plt.scatter(x=df[name1], y=df["condition"], s=100, alpha=1, c=['red'])
plt.xlabel(f"{name1}")
plt.ylabel(f"{name2}")
plt.title(f"{name1} / {name2}")
plt.grid()
plt.show()

name2 = "humidity %"
sc = plt.scatter(x=df[name1], y=df[name2], s=100, alpha=1, c=-df[name2])
plt.xlabel(f"{name1}")
plt.ylabel(f"{name2}")
plt.title(f"{name1} / {name2}")
plt.grid()
plt.show()

name2 = "condition"
sc = plt.scatter(x=df[name1], y=df[name2], s=100, alpha=1, c=-df[name2])
plt.xlabel(f"{name1}")
plt.ylabel(f"{name2} 0 good 1 bad")
plt.title(f"{name1} / {name2}")
plt.grid()
plt.show()
