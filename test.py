import datetime

time_now = datetime.datetime(2021, 8, 9, 10, 0)
min_time = datetime.datetime(2021, 8, 9, 11, 0)
last_time = datetime.datetime(2021, 8, 7, 11, 0)
night = True
if (min_time - time_now).days >= 1 and (time_now - last_time).days >= 1 and (
        (23 <= time_now.hour or time_now.hour <= 6) and night or 6 < time_now.hour < 23):
    print("1 day")
elif (min_time - time_now).seconds + (min_time - time_now).days * 3600 * 24 <= 60 * 60 and (
        time_now - last_time).seconds + (
        time_now - last_time).days * 3600 * 24 >= 60 * 30 and (
        (23 <= time_now.hour or time_now.hour <= 6) and night or 6 < time_now.hour < 23):
    print("30 minutes")
elif (min_time - time_now).seconds + (min_time - time_now).days * 3600 * 24 <= 60 * 60 * 5 and (
        time_now - last_time).seconds + (
        time_now - last_time).days * 3600 * 24 >= 60 * 60 and (
        (23 <= time_now.hour or time_now.hour <= 6) and night or 6 < time_now.hour < 23):
    print("1 hour")
elif (min_time - time_now).seconds + (min_time - time_now).days * 3600 * 24 <= 60 * 60 * 12 and (
        time_now - last_time).seconds + (
        time_now - last_time).days * 3600 * 24 >= 60 * 60 * 3 and (
        (23 <= time_now.hour or time_now.hour <= 6) and night or 6 < time_now.hour < 23):
    print("3 hours")
elif (min_time - time_now).days == 0 and (time_now - last_time).seconds + (
        time_now - last_time).days * 3600 * 24 >= 60 * 60 * 6 and (
        (23 <= time_now.hour or time_now.hour <= 6) and night or 6 < time_now.hour < 23):
    print("6 hours")
