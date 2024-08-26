from datetime import datetime

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