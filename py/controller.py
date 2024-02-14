import json

from model import Database


class Decode():
    
    def __init__(self, message):
        self.message = message
        
    def get_student_id(self):
        store = Store()
        try:
            msg = json.loads(self.message)
            student_id = msg.get("Payload", None)
            store.insert_attendance(student_id)
            return student_id
        #except:
            #return None
        except Exception as e:
            print(e)
    

class Store():
    
    def __init__(self):
        self.db = Database()
        self.conn = self.db.create_connection()
        
    def insert_attendance(self, student_id):
        self.db.insert_attendance(student_id, self.conn)
        
    