import os

def checkType(url):
	_, extension = os.path.splitext(url)
	if(extension == ".jpg" or extension == ".png" or extension == ".jpeg"):
		return True

test = "https://preview.redd.it/u7e8y7co0ex41.jpg"

if(checkType(test)):
	print("GOOD FILE")
else:
	print("BAD FILE")
