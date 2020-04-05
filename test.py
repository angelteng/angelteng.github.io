import requests
data = requests.get("http://www.pythonchallenge.com/pc/def/equality.html")
data = data.read()
print("".join(re.findall("[^A-Z][A-Z]{3}([a-z])[A-Z]{3}[^A-Z]", data)))
