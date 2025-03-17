# This just downloads the updated software
import requests

url = 'https://raw.githubusercontent.com/shiryay/translinter/refs/heads/master/validate.exe'

response = requests.get(url)
with open('validate.exe', 'wb') as file:
    file.write(response.content)
