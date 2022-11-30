import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser

con = sqlite3.connect("spy.db")
cur = con.cursor()

cur.execute('select date(time), count(*) from set_changes group by date(time) order by time')
data = cur.fetchall()

dates = []
values = []

for row in data:
    dates.append(parser.parse(row[0]))
    values.append(row[1])

plt.plot_date(dates, values, '-')
plt.show()
