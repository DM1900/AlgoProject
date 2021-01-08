#!/usr/bin/python

a = "TESTing the Print concat "
b = 123
print(a, b)


txt1 = "My name is {fname}, I'm {age}".format(fname = "John", age = 36)
print(txt1)
txt2 = "My name is {0}, I'm {1}".format("John",36)
txt3 = "My name is {}, I'm {}".format("John",36)

APIkey = "TGF596886H43"
print("Got API key, {key}, now waiting to continue...".format(key = APIkey))

ticker = "TestTicker"
print("{} - Error found, attempting to continue...".format(ticker))
