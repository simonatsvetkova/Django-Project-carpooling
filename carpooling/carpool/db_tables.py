# import sqlite3
# #
# # conn = sqlite3.connect('db.sqlite3')
# # cursor = conn.execute("SELECT * FROM sofia_districts ORDER BY District ASC")
# # rows = cursor.fetchall()
# #
# # districts = list(rows)
# # print(districts)
#
# from django.db import connection
# db = sqlite3.connect('development')
# cursor = db.cursor()
#
# # cursor = connection.cursor()
# cursor.execute("SELECT * FROM sofia_districts ORDER BY District ASC")
# districts = [row[0] for row in cursor.fetchall()]
# db.close()
# # rows = cursor.fetchall()
# # districts = list(rows)


import csv


CSV_PATH = 'Sofia_districts.csv'      # Csv file path


with open(CSV_PATH, 'r') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar=';')
    districts = list(rows)
    flat_list = [item for sublist in districts[1:] for item in sublist]
    print(flat_list)
    DISTRICTS = [(dist, dist) for dist in flat_list]
    print(DISTRICTS)

