import datetime

time_now = datetime.datetime(2021, 8, 9, 10, 0)
min_time = datetime.datetime(2021, 8, 9, 11, 0)
print((time_now - min_time).seconds)
print((min_time - time_now).seconds)
print(time_now < min_time)
