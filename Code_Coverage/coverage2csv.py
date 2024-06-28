import os
import pandas as pd

def stuff(time, name):

	try:
		df = pd.read_html(f"<Path to ACV Reports>/index.html")
	except:
		print(f"Couldnt find {name} for {time} secs")
		return (None, None, None)
	else:
		print(f"{time} {name}")
		df = df[0]
		df = df.drop(["Missed","Lines","Missed.1","Methods","Missed.2","Classes"], axis=1)
		totalcov = df.iloc[-1]
		df = df.drop(index=df.index[-1],axis=0)
		df = df.drop(["Ratio"], axis=1)
		try:
			android = df[df.Element.str.contains("^android.|^com.google.|^androidx.")]
		except:
			return (None, None, None)
		else:
			android = android.rename(columns={f"Cov.":f"Cov.({time}-sec)"})
			try:
				not_android = df[~df.Element.str.contains("^android.|^com.google.|^androidx.")]
			except:
				return (None, None, None)
			else:
				not_android = not_android.rename(columns={f"Cov.":f"Cov.({time}-sec)"})
				temp = {totalcov.index[0] : "Total", f"Cov.({time}-sec)" : totalcov.values[2]}
				cov = pd.DataFrame(temp, index=temp)
				cov = cov.drop_duplicates()
				return (android, not_android, cov)

PATH="<Path of the ACV Reports>"

files = os.scandir(PATH)

dirs = []

for f in files:
	if f.is_dir():
		dirs.append(f)
print("len of dirs:", len(dirs))
for d in dirs:

	android = [None]*7
	not_android = [None]*7
	cov = [None]*7

	for i in range(10,80,10):
		temp1, temp2, temp3 = stuff(str(i), d.name)
		android[(i//10)-1] = temp1
		not_android[(i//10)-1] = temp2
		cov[(i//10)-1] = temp3

	net_android = pd.DataFrame(columns = ["Element"])
	net_not_android = pd.DataFrame(columns = ["Element"])
	net_cov = pd.DataFrame(columns = ["Element"])

	for i in range(7):
		if android[i] is not None and not_android[i] is not None and cov[i] is not None:
			net_android = net_android.merge(android[i], on="Element", how="outer")
			net_not_android = net_not_android.merge(not_android[i], on="Element", how="outer")
			net_cov = net_cov.merge(cov[i], on="Element", how="outer")

	if net_android is not None:
		net_android.to_csv("<Output directory>"+d.name+"-Android.csv")
	if net_not_android is not None:
		net_not_android.to_csv("<Output directory>"+d.name+"-NotAndroid.csv")
	if net_cov is not None:
		net_cov.to_csv("<Output directory>"+d.name+"-Total.csv")

