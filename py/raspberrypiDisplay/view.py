# -*- coding: utf8 -*-
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import StringProperty
from controller import Decode

import serial
    
# Basic class Float Layout
class MyID(FloatLayout):

    student_id = StringProperty('')
    
    def __init__(self, **kwargs):
        super(MyID, self).__init__(**kwargs)

        # Set the timer for redrawing the screen
        refresh_time = 1/60
        Clock.schedule_interval(self.timer, refresh_time)

    def timer(self, dt):
        # Get data from serial port
        value = ser.readline()
        
        # Instanciate Decode
        decode = Decode(value)
        student_id = decode.get_student_id()

        print(value)
        if student_id:
            self.student_id = str(student_id)

        # More about drawing in Kivy here: http://kivy.org/docs/api-kivy.graphics.html


# Main App class
class TrngMationApp(App):
    def build(self):
        return MyID()

# Main program
if __name__ == '__main__':
    # Connect to serial port first
    try:
        ser = serial.Serial('/dev/ttyACM0', 115200)
    except:
        print ("Failed to connect")
        exit()

    # Launch the app
    TrngMationApp().run()

    # Close serial communication
    ser.close()