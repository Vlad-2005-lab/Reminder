import datetime

t = datetime.datetime(2021, 8, 8, 11, 0)
print(datetime.datetime.fromtimestamp(t.timestamp() - 3 * 60 * 60))
