from datetime import datetime
import requests, time

def calc_time_elapsed(start, end):
    time_elapsed = end - start

    hours, remainder = divmod(time_elapsed.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    elapsed_time_str = []
    if hours > 0:
        elapsed_time_str.append(f"{hours} hrs")
    if minutes > 0:
        elapsed_time_str.append(f"{minutes} mins")
    if seconds > 0:
        elapsed_time_str.append(f"{seconds} secs")

    formatted_time_elapsed = ' '.join(elapsed_time_str)


    return formatted_time_elapsed

def fetch_page(url, retries = 5, delay = 2):
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 503:
                print(f"{response.status_code} Service Unavailable, retrying {i+1}/{retries}\n\t{url}")
                time.sleep(delay)
                continue
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"an error occured: {e}")
            time.sleep(delay)
    print(f"Failed to retrieve page after {retries} retries.")
    return None