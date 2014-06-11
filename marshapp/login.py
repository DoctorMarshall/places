import requests
import json
import mysql.connector
import hashlib

class Login:
    @staticmethod
    def login(login,password):
        config = {
            'database': 'andmar',
            'user': 'andmar',
            'password': 'G8euWMWW',
            'host': 'mysql.agh.edu.pl',   # Or an IP Address that your DB is hosted on
            'port': 3306,
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("SELECT user FROM users "
                  "WHERE user = %s AND password = %s")

        cursor.execute(query, (login, hashlib.sha1(password).hexdigest()))

        data = cursor.fetchone()

        cursor.close()
        cnx.close()
        
        if data == None:
            return False
        else:
            return True
        
    @staticmethod
    def register(login,password):
        config = {
            'database': 'andmar',
            'user': 'andmar',
            'password': 'G8euWMWW',
            'host': 'mysql.agh.edu.pl',   # Or an IP Address that your DB is hosted on
            'port': 3306,
        }
        
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        query = ("INSERT INTO users "
                  "VALUES ('', %s, %s)")
    
        cursor.execute(query, (login, hashlib.sha1(password).hexdigest()))
    
        cursor.close()
        cnx.close()
        
