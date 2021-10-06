import requests, os, shutil, nice_prompts

n = nice_prompts.NicePrompt()

term = input("Enter a search term: ")
size = n.number(int, start=10)


vals = []

try:
	shutil.rmtree("out")
except:
	pass
os.mkdir("out")

"""

ll = -1

for i in range(0, int(size/50)):
	if len(vals) == ll:
		break
	else:
		ll = len(vals)
	querystring = {"q": term,"pageNumber":str(i),"pageSize": "50","autoCorrect":"false","safeSearch":"false"}

	headers = {
		'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
		'x-rapidapi-key': "4T18ZkeUlQmshxea6M24N3sb8wxHp1Wm9QijsnnqXiGRcq4qy7"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)

	for i in response.json()["value"]:
		vals.append(i["url"])
	print(len(vals))
"""

ID = "005146048857925457595:-bsanu4k_hq"
key = "AIzaSyAQkjdVis0sBNf2wNqJxO0T33-d-yyFmf0"

url = "https://www.googleapis.com/customsearch/v1"

num = size

from pprint import pprint
last = []

print("Select a SafeSearch level")
s = n.selection({"No filtering": "off", "Enable SafeSerach filtering": "active"})
for i in range(0, int(num), 10):
	r = requests.get(url, params={
		'key': key,
		'cx': ID,
		'q': term,
		'searchType': 'image',
		'start': i,
		'safe': s
	})
	try:
		print(str(i) + str(r.json() == last) + str(len(r.json()['items'])))
		last = r.json()
		r.raise_for_status()
		for i in r.json()['items']:
			vals.append(i["link"])
	except Exception as e:
		pprint(r.json())
		print(e)
		



print("Made Request")

images = []

for i in vals:
	try:
		r = requests.get(i, stream=True)
	except:
		continue
	if r.status_code != 200:
		print(r.url + "      " + str(r.status_code))
		continue
	filename = "out/" + i.split("/")[-1].split("?")[0]
	try:
		with open(filename, "wb+") as f:
			for i in r.iter_content(1024):
				f.write(i)
	except:
		pass
	images.append(filename)

images.reverse()

print("Got Images")

from moviepy.editor import *
full = []
for i in images:
	try:
		image = ImageClip(i).resize(newsize=(1080, 720)).set_duration(1)
		image.close()
		del image
	except:
		images.remove(i)
num = len(images)
print("start creating video")
title = TextClip(f"Top {num} {term}",fontsize=70,color='white')
print("resize title")
title = title.resize(newsize=(1080, 720))
print("set duration")
title = title.set_duration(5)
full.append(title)
for i in images:
	try:
		image = ImageClip(i).resize(newsize=(1080, 720)).set_duration(3)
	except:
		continue
	full.append(TextClip(f"Number {num}",fontsize=70,color='white').resize(newsize=(1080, 720)).set_duration(3))
	full.append(image)
	print("loaded " + i)
	num -= 1

final = concatenate_videoclips([*[i.crossfadein(1.5).crossfadeout(1.5) for i in full], ImageClip("./outro.png").resize(newsize=(1080, 720)).set_duration(10).crossfadein(1.5)], method="compose")

dur = final.duration

print(dur)

matched = 0
from itertools import cycle
audios = cycle(["./music/" + str(i) + ".webm.mp3" for i in range(23)])

bgm = []

while matched < dur:
	song = next(audios)
	print("load song " + song)
	mus = AudioFileClip(song)
	matched += mus.duration
	bgm.append(mus)

final = final.set_audio(concatenate_audioclips(bgm).set_duration(dur))
print(final.duration)
final.write_videofile("output.mp4", fps=24)