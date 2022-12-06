import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser

con = sqlite3.connect("spy.db")
cur = con.cursor()

cur.execute("""
    select date(time), count(*) from set_changes
    where change='added'
    group by date(time)
   order by time
""")
added = cur.fetchall()

cur.execute("""
    select date(time), count(*) from set_changes
    where change='removed'
    group by date(time)
   order by time
""")
removed = cur.fetchall()

dates = []
values = []

for row in added:
    dates.append(parser.parse(row[0]))
    values.append(row[1])

plt.plot_date(dates, values, '-')

dates = []
values = []

for row in removed:
    dates.append(parser.parse(row[0]))
    values.append(row[1])

plt.plot_date(dates, values, '-')

plt.show()
