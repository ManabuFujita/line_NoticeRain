#!/usr/local/bin/python3.7
print("Content-Type: text/html\n")
print("Hello Python!")


import datetime

print("---\n")
print("<br>")


now = datetime.datetime.now()
timeFrom = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=7, minute=0, second=0)
timeTo = datetime.datetime(year=now.year, month=now.month, day=now.day, hour=21, minute=0, second=0)

print(now)
print("<br>")
print(timeFrom)
print("<br>")
print(timeTo)
print("<br>")
print("---\n")
print("<br>")
print(timeFrom < now)
print("<br>")
print(now < timeTo)
print("<br>")


