#!/usr/bin/python

import sqlite3
from sqlite3 import Error
import time
import sys
from datetime import date
import datetime


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def convert_mmol(mgdl):
	return mgdl * 0.0555


def get_real_bg_readings(conn, min_epoch, max_epoch):
	cur = conn.cursor()
	cur.execute("SELECT dg_mgdl, timestamp FROM BgReadings WHERE dg_mgdl > 0 AND timestamp > " + str(min_epoch) + " AND timestamp < " + str(max_epoch))

	rows = cur.fetchall()

	return rows

def print_help():
	print("Help:")
	print("--help : This message.")
	print("--database : Database file. DEFAULT: 'xdrip.sqlite'")
	print("--start_timestamp : Epoch/Unix timestamp from where to start counting. DEFAULT: Start of current day.")
	print("--end_timestamp : Epoch/Unix timestamp from where to stop counting. DEFAULT: End of current day.")

def main():

	database = "xdrip.sqlite"
	start_ts = int(time.mktime(datetime.datetime.strptime(date.today().strftime("%d/%m/%Y"), "%d/%m/%Y").timetuple())) #Copied and edited from SO, probably inefficient af lol.
	end_ts   = start_ts + 86400

	if len(sys.argv) < 2:
		print_help()
		exit()


	for arg in sys.argv:
		if arg.startswith("--help"):
			print_help()
			exit()
		elif arg.startswith("--start_timestamp"):
			start_ts = int(sys.argv[sys.argv.index(arg) + 1])
		elif arg.startswith("--stop_timestamp"):
			end_ts = int(sys.argv[sys.argv.index(arg) + 1])
		elif arg.startswith("--database"):
			database = sys.argv[sys.argv.index(arg) + 1]



    # create a database connection
	conn = create_connection(database)
	with conn:
		data = get_real_bg_readings(conn, start_ts * 1000, end_ts * 1000)
		#data = get_real_bg_readings(conn, 0, int(time.time()))

		total_delta = 0
		previous = 0
		for dat in data:
			if previous == 0:
				previous = dat[0]

			delta = dat[0] - previous
			previous = dat[0]

			if delta < 0:
				delta = delta * -1

			total_delta += delta

		print(convert_mmol(total_delta))



if __name__ == '__main__':
    main()
