#!/usr/bin/python
import os, sys
import serial
import time
import json
import sqlite3

from sqlite3 import Error
from datetime import date


def create_connection(db_file):
    """ create a database connection to the SQLite database
        spicified by db_file
        
    :param db_file: database file
    :return: Connection objetc or None
    """
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
                
    return conn

def get_student_id(message):
    msg = json.loads(message)
    student_id = msg.get("Payload", None)
    return student_id

def insert_attendance(student_id, conn):
    
    with conn:
        day = date.today().strftime("%Y-%m-%d")
        sql = '''INSERT INTO ATTENDANCE(STUDENT_ID)
                 SELECT ?
             WHERE NOT EXISTS (SELECT ID
                               FROM ATTENDANCE
                               WHERE STUDENT_ID = ?
                               AND DATE(DTTM, 'localtime') = ?
                               AND JULIANDAY('NOW') - JULIANDAY(DTTM) < 0.416
                               )
               '''
        conn.execute(sql, (student_id, student_id, day))
        conn.commit()
        
def show_student_dttm(student_id, conn):
    with conn:
        cur = conn.cursor()
        sql = ''' SELECT STUDENT_ID, DATETIME(MAX(DTTM), 'localtime')
                  FROM ATTENDANCE
                  WHERE STUDENT_ID = ?
              '''
        cur.execute(sql, (student_id,))
        row = cur.fetchone()
        print(f'Matrícula:{row[0]}, Dia y hora:{row[1]}')
        
        
def main():
    
    ser = serial.Serial('/dev/ttyACM0',115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
            xonxoff=False, rtscts=False, stopbits=serial.STOPBITS_ONE,  timeout = 5)    
    
    database = r"/home/pi/Documents/Attendance/db.sqlite"
    
    # create a database connection
    conn = create_connection(database)
    
    student_id = None
    
    # listen for the input, exit if nothing received in timeout period
    while True:
        line = ser.readline()
        if len(line) == 0:
            print("Time out! Exit.\n")
            sys.exit()
        
        try:
            student_id = get_student_id(line)
        except:
            student_id = None
        if student_id and student_id.isdigit():
            insert_attendance(int(student_id), conn)
            show_student_dttm(int(student_id), conn)
        

if __name__ == "__main__":
    main()
