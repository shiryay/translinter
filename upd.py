# This just downloads the updated software
import psutil
import requests

url = 'https://github.com/shiryay/rulesrepo/raw/refs/heads/main/validate.exe'
target_process = 'validate.exe'

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


if __name__ == '__main__':
    try:
        response = requests.get(url)
        # close the updated software
        kill_process(target_process)

        # Verify process is terminated
        if not is_process_running(target_process):
            with open(target_process, 'wb') as file:
                file.write(response.content)
        else:
            print("Could not terminate the existing process")
    except Exception as e:
        print(f"Update failed: {str(e)}")
