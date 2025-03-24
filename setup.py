# This just downloads the updated software
import os
import psutil
import requests

exe_url = 'https://github.com/shiryay/rulesrepo/raw/refs/heads/main/validate.exe'
version_url = 'https://raw.githubusercontent.com/shiryay/rulesrepo/refs/heads/main/version.txt'
rules_url = 'https://raw.githubusercontent.com/shiryay/rulesrepo/refs/heads/main/rules.json'
cleanup_url = 'https://raw.githubusercontent.com/shiryay/rulesrepo/refs/heads/main/cleanup'
target_process = 'validate.exe'
file_list = ('validate.exe', 'rules.json', 'version.txt')

def is_process_running(process_name):
    return any(proc.info['name'] == process_name for proc in psutil.process_iter(['name']))

def kill_process(process_name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] == process_name:
                proc.kill()
                proc.wait(timeout=5)  # Wait up to 5 seconds for the process to terminate
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            pass

def update_exe():
    try:
        response = requests.get(exe_url)
        # close the updated software
        kill_process(target_process)

        # Verify process is terminated
        if not is_process_running(target_process):
            with open(target_process, 'wb') as file:
                file.write(response.content)
        else:
            print("Could not terminate the existing process")
    except Exception as e:
        print(f"Failed to update program: {str(e)}")

def update_version_txt():
    try:
        response = requests.get(version_url)
        with open('version.txt', 'w') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Failed to update version.txt: {str(e)}")

def fetch_file(file_name):
    if file_name == 'validate.exe':
        update_exe()
    elif file_name == 'rules.json':
        response = requests.get(rules_url)
        with open(file_name, 'wb') as file:
            file.write(response.content)
    elif file_name == 'version.txt':
        update_version_txt()
    else:
        return

def cleanup_required() -> bool:
    try:
        response = requests.head(cleanup_url)
        return response.status_code == 200
    except Exception:
        return False

if __name__ == '__main__':
    # Cleanup
    if cleanup_required():
        for file in file_list:
            if os.path.exists(file):
                os.remove(file)

    # Download missing files
    for file in file_list:
        if not os.path.exists(file):
            fetch_file(file)
    
    update_exe()
    update_version_txt()
