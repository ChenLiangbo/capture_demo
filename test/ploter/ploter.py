#!user//bin/env/python
# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt

x = [1,2,3,3.5,4,8,16,32]
rate = [1,1,1,1,0.9194,0.4788,0.2991,0.1759]
time = [3.2807,1.6438,1.1154,1.0882,0.9334,0.4837,0.2941,0.1754]
c = [3.4279,1.6933,1.1504,1.1145,1.0336,1.0195,1.0054,1.0073]


print "len(x)= ",len(x)
print "len(rate) = ",len(rate)
plt.plot(x,time,'--or')

ylabel = "Time(s)"
xlabel = "Length(x1024 B)"
title = "Time and Length"

plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)

plt.xlim(0,34)
plt.ylim(0,4)

# plt.show()
plt.grid(True)

plt.savefig('./time.jpg')

print "rate finished"
