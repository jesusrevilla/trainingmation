import sqlite3

from sqlite3 import Error
from datetime import date


class Database():
    
    def __init__(self):
        #self.path = r"/home/pi/Documents/Attendance/db.sqlite"
        self.path = r"/home/pi/Documents/Attendance/trainingmation/py/raspberrypiDisplay/db.sqlite"

        
    def create_connection(self):
        """ create a database connection to the SQLite database
            spicified by db_file
            
        :return: Connection objetc or None
        """
        
        conn = None
        try:
            conn = sqlite3.connect(self.path)
        except Error as e:
            print(e)
                    
        return conn

    def insert_attendance(self, student_id, conn):
        
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
