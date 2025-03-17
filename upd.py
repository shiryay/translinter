# This just downloads the updated software
import psutil
import requests

url = 'https://github.com/shiryay/rulesrepo/raw/refs/heads/main/validate.exe'

def kill_process(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == process_name:
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
try:
    response = requests.get(url)
    kill_process('validate.exe')
    with open('validate.exe', 'wb') as file:
        file.write(response.content)
except:
    print("Update failed")