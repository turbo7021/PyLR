""" This is Python Latency Recorder (PyLR) made by Arturs Stipnieks
    !!!AUDIO FILES MUST BE ANALYZED BY ONESELF, THE PROGRAM ONLY RECORDS SIGNAL!!!
    Code examples taken and modified from:
            kivy.org/doc/stable
            https://www.geeksforgeeks.org/python-textinput-in-kivy-using-kv-file/
            https://realpython.com/playing-and-recording-sound-python/
    Project will potentionally be finished, for now available as is,
    absolutely no guarantees given, use code as needed.
    Any useful critique is much appreciated."""

import simpleaudio as sa
import time
import sounddevice as sd
from scipy.io.wavfile import write
import threading
import kivy
kivy.require('1.0.7')
from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard 

Builder.load_string('''
<RecordClick>:
    orientation: 'vertical'
    TextInput:
        id: input
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Record test'
        id: mainbutton
        on_press: root.capture()
    Button:
        text: 'Info'
        size_hint_y: None
        height: '48dp'
        on_press: root.info()
''')


filename = 'beep10k16bit.wav'   #audio for test,
                                #incuded 10KHz sine for 8 cycles at 44100 samples

def click():                    #play click function
    global filename             #use the file given at the beginning of code
    time.sleep(0.2) 
    print("click started")
    wave_obj = sa.WaveObject.from_wave_file(filename)   #prepare wave obj
    play_obj = wave_obj.play()  #play
    play_obj.wait_done()        #wait till finished
    print("click done")

def record(title):              #record audio function
    print("record started")     
    fs = 44100          #sample rate
    seconds = 1         #how long to record
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2) #RECORD
    sd.wait()  #wait to finish recording
    timestr = time.strftime("%Y%m%d_%H%M%S")        #timestamp for name
    outputname = (title + '_' + timestr + '.wav')   #take name from textbox
    write(outputname, fs, myrecording)  #save as wav
    print("record done")

class RecordClick(BoxLayout):   
    def capture(self):
        title = self.ids.input.text
        print(title)
        recordthread = threading.Thread(target=record, args=(title,))
        clickthread = threading.Thread(target=click, args=())
        recordthread.start()    #start a new thread for recording
        clickthread.start()     #start a new thread for playing click
    def info(self):
        infotext = """Start by turning on the device to be tested and making
the speakers output whatever signal enters the microphone
after its ran through any porcessing that introduces latnecy.
For best results its advised to EQ the outpu signal so that
its audibly different from the input signal. Turn up the volume
on the device this is being ran on. Keep in mind any safety
percussions, as the signal will be 8 cycles of sine in 10KHz.
Turn up the volume of the device to be tested just before the input
starts to feedback.
In the text box above, enter the name of each test and
name of the file will be <your given file name> + <tiemstamp>.wav.
Afterwards, navigate to the project folder and analyze the file in
any DAW or audio editor that displays time.
Link to source code has been coppied to your clipboard.
"""
        print(infotext)
        self.ids.mainbutton.text = infotext
        Clipboard.copy('https://github.com/turbo7021/PyLR')

class AppWindow(App):   
    def build(self):
        return RecordClick()
    
def main():
    AppWindow().run()   #run the window

main()


