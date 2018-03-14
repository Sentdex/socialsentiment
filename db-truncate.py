'''
Run as a cronjob to keep database size under control
'''
import time
import sqlite3

conn = sqlite3.connect('twitter.db', check_same_thread=False)
c = conn.cursor()

HM_DAYS_KEEP = 3
current_ms_time = time.time()*1000
one_day = 86400 * 1000
del_to = int(current_ms_time - (HM_DAYS_KEEP*one_day))

sql = "DELETE FROM sentiment_fts WHERE rowid IN (SELECT id FROM sentiment WHERE unix <  {})".format(del_to)
c.execute(sql)

sql = "DELETE FROM sentiment WHERE unix < {}".format(del_to)
c.execute(sql)

# you will need to vacuum if you ever to a bulk delete.
#c.execute("VACUUM")
conn.commit()
conn.close()
