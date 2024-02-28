import tkinter
import customtkinter
import json
from urllib.request import urlopen
from gtts import gTTS
from playsound import playsound
from twilio.rest import Client
from geopy.geocoders import Nominatim
import time
import mysql.connector
from PIL import Image
import os
import cv2 as cv
import pygame
import pygame.camera

myconn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "SOS"
)

print(myconn)
cur = myconn.cursor()
print(cur)

sosify_app = customtkinter.CTk()
sosify_app.geometry("1920x1080")
sosify_app.title("SOS-ify")
sosify_app.config(background = "black")

sosify_title = customtkinter.CTkLabel(master=sosify_app,width=200,height=50,bg_color="black",
                text="SOS-ify",text_color="white",font=("Hanson",40))    
sosify_title.place(relx=0.5,rely=0.125,anchor=tkinter.CENTER)

name_label = customtkinter.CTkLabel(master=sosify_app,text="Enter Name",bg_color="black")
name_label.place(relx=0.5,rely=0.25,anchor=tkinter.CENTER)

name = customtkinter.CTkEntry(master=sosify_app, width=350,height=40,corner_radius=15,border_width=2,
                              placeholder_text="Full Name",placeholder_text_color="Grey")
name.place(relx=0.5,rely=0.30,anchor=tkinter.CENTER)

bloodgroup_label = customtkinter.CTkLabel(master=sosify_app,text="Enter Blood Group",bg_color="black",fg_color="black")
bloodgroup_label.place(relx=0.5,rely=0.35,anchor=tkinter.CENTER)

bloodgroup_select = customtkinter.CTkComboBox(master=sosify_app,values=["Choose Blood Group","A+", "A-","B+", "B-","O+", "O-","AB+", "AB-"],
                                            width=350,height=40,corner_radius=15)
bloodgroup_select.place(relx=0.5,rely=0.40,anchor=tkinter.CENTER)

activeill_label = customtkinter.CTkLabel(master=sosify_app,text="Enter Active Illness",bg_color="black",fg_color="black")
activeill_label.place(relx=0.5,rely=0.45,anchor=tkinter.CENTER)

activeill_entry = customtkinter.CTkEntry(master=sosify_app, width=350, height=40)
activeill_entry.place(relx=0.5,rely=0.5,anchor=tkinter.CENTER)

disability_label = customtkinter.CTkLabel(master=sosify_app,text="Enter Disability",bg_color="black")
disability_label.place(relx=0.5,rely=0.55,anchor=tkinter.CENTER)

disability_entry = customtkinter.CTkEntry(master=sosify_app, width=350, height=40)
disability_entry.place(relx=0.5,rely=0.60,anchor=tkinter.CENTER)

pastill_label = customtkinter.CTkLabel(master=sosify_app,text="Enter Past Illness",bg_color="black")
pastill_label.place(relx=0.5,rely=0.65,anchor=tkinter.CENTER)

pastillness_entry = customtkinter.CTkEntry(master=sosify_app, width=350, height=40)
pastillness_entry.place(relx=0.5,rely=0.70,anchor=tkinter.CENTER)

def submitPressed():
    print(name.get())
    print(bloodgroup_select.get())
    print(activeill_entry.get())
    print(disability_entry.get())
    print(pastillness_entry.get())

    n = name.get()
    b = bloodgroup_select.get()
    a = activeill_entry.get()
    d = disability_entry.get()
    p = pastillness_entry.get()

    sql = "INSERT INTO SOSify (FullName, BloodGroup, ActiveIllness, Disability, PastIllness)\
    VALUES (%s, %s, %s, %s, %s)"
    val = (n,b,a,d,p)

    cur.execute(sql, val)
    myconn.commit()

    sosButton_app = customtkinter.CTk()
    sosButton_app.geometry("200x200")
    sosButton_app.title("SOS-ify: SOS Button")

    account_sid = 'AC5282113049e6afd8321daec0131ac62c'
    auth_token = 'c8a2a5f5602951ddd3fc477be55ac9cc'
    client = Client(account_sid, auth_token)

    data = json.load(urlopen("http://ipinfo.io/json"))
    lat = data['loc'].split('.')[0]
    lon = data['loc'].split('.')[1]

    #geolocator = Nominatim(user_agent="geoApi")
    Latitude = lat
    Longitude = lon
    locstring = "{}, {}".format(lat,lon)
    #location = geolocator.reverse("{}, {}".format(lat,lon))
    sosify_app.geometry("0x0")

    def startSOS():
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)

        print("SOS initiated")
        sosmsg = """ This is an SOS message from SOS-ify

        Sent at: {}

        Sent From:
            Latitude: {}
            Longitude: {}

        by {}

        Details of {}:
            Blood Group: {}
            Active Illness: {}
            Disability: {}
            Past Illness: {}

https://drive.google.com/drive/folders/10wkDQERw2ra9uFtP61Hmtqvs2qFMEn0o?usp=sharing
        """.format(current_time,lat,lon,name.get(),name.get(),bloodgroup_select.get(),activeill_entry.get(),disability_entry.get(),pastillness_entry.get())
        print(sosmsg)

        tts = gTTS("SOS sequence has been initiated")
        tts.save("seqinit.mp3")
        playsound("seqinit.mp3")

        message = client.messages.create(
        body=sosmsg,
        from_='whatsapp:+14155238886',
        to='whatsapp:+919446574962'
        )

        message = client.messages.create(
        body=sosmsg,
        from_='whatsapp:+14155238886',
        to='whatsapp:+919539297703'
        )

        message = client.messages.create(
        body=sosmsg,
        from_='whatsapp:+14155238886',
        to='whatsapp:+919946024593'
        )

        os.system('python make_call.py')

        print(message.sid)

        pygame.camera.init()
        camlist = pygame.camera.list_cameras()
        if camlist:
            cam = pygame.camera.Camera(camlist[0], (640, 480))
            cam.start()
            image = cam.get_image()
            pygame.image.save(image, "sosimage.jpg")
            
        else:
            print("No camera on current device")

        SOSsql = "INSERT INTO SOSifyLog (SOStime, Latitude, Longitude)\
        VALUES (%s, %s, %s)"
        SOSval = (current_time,lat,lon)

        cur.execute(SOSsql, SOSval)
        myconn.commit()

    sos_button = customtkinter.CTkButton(master=sosButton_app, text="SOS", command=startSOS,hover_color="red",
                                     corner_radius=1000,height=100)
    sos_button.place(relx=0.5,rely=0.5,anchor=customtkinter.CENTER)

    sosButton_app.mainloop()

submit_button = customtkinter.CTkButton(master=sosify_app, text="Submit",hover_color="green",corner_radius=10,
                command=submitPressed,width=350,height=40)
submit_button.place(relx=0.5,rely=0.85,anchor=tkinter.CENTER)

sosify_app.mainloop()