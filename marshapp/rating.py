import requests
import mysql.connector
import hashlib
from decimal import *

class Rating:
    @staticmethod
    def addRating(login, place, rating):
        config = {
            'database': 'andmar',
            'user': 'andmar',
            'password': 'G8euWMWW',
            'host': 'mysql.agh.edu.pl',   # Or an IP Address that your DB is hosted on
            'port': 3306,
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("INSERT INTO rating VALUES "
                  "('', %s, %s, %s)")

        cursor.execute(query, (login, place, rating))

        #data = cursor.fetchone()

        cursor.close()
        cnx.close()
        
    @staticmethod
    def getRating(login, place):
        config = {
            'database': 'andmar',
            'user': 'andmar',
            'password': 'G8euWMWW',
            'host': 'mysql.agh.edu.pl',   # Or an IP Address that your DB is hosted on
            'port': 3306,
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("SELECT rating FROM rating "
                  "WHERE user = %s AND place_id = %s ORDER BY id DESC")

        cursor.execute(query, (login, place))

        data = cursor.fetchone()

        cursor.close()
        cnx.close()
        
        if data == None:
            return None
        else:
            return data[0]
        
        
    @staticmethod
    def addComment(login, place, comment):
        config = {
            'database': 'andmar',
            'user': 'andmar',
            'password': 'G8euWMWW',
            'host': 'mysql.agh.edu.pl',   # Or an IP Address that your DB is hosted on
            'port': 3306,
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("INSERT INTO comments VALUES "
                  "('', %s, %s, %s)")

        cursor.execute(query, (login, place, comment))

        #data = cursor.fetchone()

        cursor.close()
        cnx.close()
        
    @staticmethod
    def getComments(place):
        config = {
            'database': 'andmar',
            'user': 'andmar',
            'password': 'G8euWMWW',
            'host': 'mysql.agh.edu.pl',   # Or an IP Address that your DB is hosted on
            'port': 3306,
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("SELECT user, text FROM comments "
                  "WHERE place = %s OR place = %s") #WTF???!!!

        cursor.execute(query, (place, place))

        data = cursor.fetchall()

        cursor.close()
        cnx.close()
        
        if data == None:
            return None
        else:
            return data
        
    @staticmethod
    def getAvgRating(place):
        config = {
            'database': 'andmar',
            'user': 'andmar',
            'password': 'G8euWMWW',
            'host': 'mysql.agh.edu.pl',   # Or an IP Address that your DB is hosted on
            'port': 3306,
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("SELECT max(id), rating FROM rating "
                  "WHERE place_id=%s OR place_id=%s GROUP BY user ") 

        cursor.execute(query, (place, place))

        data = cursor.fetchall()

        cursor.close()
        cnx.close()
        
        sum = 0
        count = 0
        for row in data:
            sum += row[1]
            count += 1
        
        if count == 0:
            return 0
        else:
            return Decimal(sum)/count
        
        
        