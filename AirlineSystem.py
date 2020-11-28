from tkinter import *
from tkcalendar import *
from tkinter import messagebox
from PIL import ImageTk, Image, ImageFile
import pymongo
import bcrypt
import re
import pytz
import datetime
from dateutil import tz
import random
from string import ascii_uppercase
import string
import keyring
import yagmail

ImageFile.LOAD_TRUNCATED_IMAGES = True

# intialize DB
mongoDB = pymongo.MongoClient(
    "mongodb+srv://Eyuwankg:{0}@mern.kvhji.mongodb.net/OOAD?retryWrites=true&w=majority".format(
        keyring.get_password("mongoDB", "mongoPassword")
    )
)
db = mongoDB["OOAD"]
profileCollection = db["profiles"]
flightCollection = db["flights"]

# Intialize Home Page for all Frames
Home = Tk()
IndexPageImage = ImageTk.PhotoImage(Image.open("./HomePage.jpg"))


# Profile Page
class Profile:
    # function to cancel a ticket
    def cancelTicket(self, ticket, deptTime):
        self.user["bookedSeats"].remove(ticket)
        profileCollection.update_one(
            {"email": self.user["email"]},
            {"$set": {"bookedSeats": self.user["bookedSeats"]}},
        )
        k = flightCollection.find({"date": deptTime.strftime("%Y-%m-%d")})
        data = []
        for i in k:
            print(i["date"])
            data = i["data"]
            break
        flightIndex = -1
        for (index, i) in enumerate(data):
            if (
                i["departure"]["airport"] == ticket["departure"]["airport"]
                and i["departure"]["timezone"] == ticket["departure"]["timezone"]
                and i["departure"]["iata"] == ticket["departure"]["iata"]
                and i["departure"]["departureUTCTime"]
                == ticket["departure"]["departureUTCTime"]
                and i["arrival"]["airport"] == ticket["arrival"]["airport"]
                and i["arrival"]["timezone"] == ticket["arrival"]["timezone"]
                and i["arrival"]["iata"] == ticket["arrival"]["iata"]
                and i["arrival"]["arrivalUTCTime"]
                == ticket["arrival"]["arrivalUTCTime"]
                and i["travelTime"] == ticket["travelTime"]
                and i["airlineName"] == ticket["airlineName"]
                and i["flightNumber"] == ticket["flightNumber"]
            ):
                flightIndex = index
                break
        for i in ticket["bookedSeats"]:
            data[flightIndex]["seatsGraph"][ascii_uppercase.index(i["row"])][
                i["column"]
            ] = 1
        flightCollection.update_one(
            {"date": deptTime.strftime("%Y-%m-%d")}, {"$set": {"data": data}}
        )
        messagebox.showinfo("Cancelled", "Ticket Cancelled")
        self.app.destroy()
        self.showBookingHistroy()

    # function to send ticket to email
    def sendTicketToEmail(self, ticket, deptTime, arrTime):
        # send ticket to email
        emailClient = yagmail.SMTP(
            "messikarthik13@gmail.com",
            keyring.get_password("gmail", "messikarthik13@gmail.com"),
        )
        subjects = "Ticket for {0} on {1}".format(
            ticket["airlineName"], deptTime.strftime("%d/%m/%Y %H:%M:%S")
        )
        contents = "                        {0}               \n  Your Booking ID : {1}\n  Departure : \n     Airport : {2}\n     Code : {3}\n     Terminal : {4}\n     Gate : {5}\n     Time : {6}\n  Arrival   : \n     Airport : {7}\n     Code : {8}\n     Terminal : {9}\n     Gate : {10}\n     Time : {11}\n  Flight Number : {12}\n  Cost : {13}".format(
            ticket["airlineName"],
            ticket["bookingID"],
            ticket["departure"]["airport"],
            ticket["departure"]["iata"],
            ticket["departure"]["terminal"],
            ticket["departure"]["gate"],
            deptTime.strftime("%d/%m/%Y  %H:%M:%S"),
            ticket["arrival"]["airport"],
            ticket["arrival"]["iata"],
            ticket["arrival"]["terminal"],
            ticket["arrival"]["gate"],
            arrTime.strftime("%d/%m/%Y  %H:%M:%S"),
            ticket["flightNumber"],
            ticket["cost"],
        )
        seatGraphForEmail = []
        for i in ticket["bookedSeats"]:
            seatGraphForEmail.append(
                "\n  {0}      {1}     {2}\n".format(
                    i["row"] + str(i["column"]), i["name"], i["age"]
                )
            )
        contents += "".join(seatGraphForEmail)
        contents += "\n  Phone Number : {0}\n".format(ticket["phoneNumber"])
        try:
            emailClient.send(self.checkEmailInput.get(), subjects, contents)
            messagebox.showinfo(
                title="Success!!!",
                message="Check {0} for Ticket".format(self.checkEmailInput.get()),
            )
        except:
            messagebox.showerror(title="Error", message="Error Sending Email")
        self.ticketCheck.destroy()

    # function to check email for sending ticket
    def checkEmailForTicketSending(self, ticket, deptTime, arrTime):
        try:
            self.ticketCheck.destroy()
        except:
            pass
        self.ticketCheck = Tk()
        self.ticketCheck.title("Check Email")
        self.ticketCheck.configure(bg="#55423d", padx=30, pady=15)
        self.checkEmailLabel = Label(
            self.ticketCheck,
            text="Send Ticket to : ",
            bg="#55423d",
            fg="#fff",
            font="havetica 12 bold",
        )
        self.checkEmailLabel.grid(row=0, column=0, padx=5, pady=5)
        self.checkEmailInput = Entry(self.ticketCheck)
        self.checkEmailInput.configure(
            justify=CENTER,
            width=40,
            bg="#271c19",
            relief=FLAT,
            fg="#fff",
            font="havetica 12 bold",
        )
        self.checkEmailInput.insert(0, ticket["email"])
        self.checkEmailInput.grid(row=0, column=1, padx=10, pady=20)
        self.sendTicketButton = Button(
            self.ticketCheck,
            text=" Send ",
            bg="#ffc0ad",
            fg="#271c19",
            font="havetica 12 bold",
            command=lambda t=ticket, dt=deptTime, at=arrTime: self.sendTicketToEmail(
                t, dt, at
            ),
        )
        self.sendTicketButton.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.ticketCheck.mainloop()

    # function to update profile in DB
    def updateProfile(self):
        self.user["name"] = self.nameInput.get()
        self.user["gender"] = "Male" if self.genderVar.get() == 1 else "Female"
        self.user["dob"] = self.dobVar.get()
        self.user["phonenumber"] = self.phoneNumberInput.get()
        profileCollection.update_one(
            {"email": self.user["email"]},
            {
                "$set": {
                    "name": self.user["name"],
                    "gender": self.user["gender"],
                    "dob": self.user["dob"],
                    "phonenumber": self.user["phonenumber"],
                }
            },
        )

    # function to re-render datePicker button
    def getDate(self):
        self.calendarFrame.destroy()
        self.dobVar.set(self.calendar.get_date())
        self.dobInput.destroy()
        self.dobInput = Button(
            self.profileFrame,
            text=self.dobVar.get(),
            bg="#f582ae",
            fg="#000",
            activebackground="#8bd3dd",
            activeforeground="#001858",
            padx=5,
            pady=3,
            font="Havetica 10 bold",
            command=self.datePicker,
            relief=FLAT,
        )
        self.dobInput.grid(row=4, column=1, pady=5)

    # Calendar
    def datePicker(self):
        self.calendarFrame = Tk()
        self.calendarFrame.title("Date Picker")
        self.calendarFrame.configure(bg="#fef6e4")
        self.calendar = Calendar(self.calendarFrame)
        self.calendar.pack()
        self.calendarButton = Button(
            self.calendarFrame,
            text="OK",
            activebackground="#f582ae",
            activeforeground="#001858",
            bg="#8bd3dd",
            fg="#001858",
            font="Havetica 10 bold",
            command=self.getDate,
            padx=5,
            pady=3,
            relief=FLAT,
        )
        self.calendarButton.pack()

    def goBack(self):
        self.profileWindow.destroy()
        self.search = SearchPage(self.parent, self.user)

    # show ticket info
    def showTicketInfo(self, ticket, deptTime, arrTime, index):
        try:
            if self.app:
                self.app.destroy()
        except:
            pass
        self.app = Tk()
        self.app.geometry("490x450")
        self.app.title(ticket["airlineName"])
        self.canvasTicket = Canvas(self.app, width=400, bg="#8ecae6")
        self.scrollBarTicket = Scrollbar(
            self.app, orient=VERTICAL, command=self.canvasTicket.yview
        )
        self.ticketFrame = Frame(
            self.canvasTicket, bg="#8ecae6", padx=20, width=410, pady=20
        )
        self.canvasTicket.create_window((0, 0), window=self.ticketFrame, anchor="nw")
        self.ticketFrame.configure(bg="#232946")
        # ------------------------------------------------S
        Label(
            self.ticketFrame,
            text="Your Ticket",
            padx=50,
            pady=20,
            font="havetica 12 bold",
            bg="#232946",
            fg="#fffffe",
        ).grid(row=0, column=0, columnspan=2)
        # Booking ID--------------------------------------S
        self.bookingIDLabel = Label(
            self.ticketFrame,
            text="Booking ID : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.bookingIDLabel.grid(row=1, column=0, padx=20, pady=20)
        self.bookingIDShowLabel = Label(
            self.ticketFrame,
            text=ticket["bookingID"],
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.bookingIDShowLabel.grid(row=1, column=1, padx=40, pady=20)
        # Booking ID--------------------------------------E
        # Email-------------------------------------------S
        self.emailLabel = Label(
            self.ticketFrame,
            text="Email : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.emailLabel.grid(row=2, column=0, padx=20, pady=20)
        self.emailShowLabel = Label(
            self.ticketFrame,
            text=ticket["email"],
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.emailShowLabel.grid(row=2, column=1, padx=40, pady=20)
        # Email-------------------------------------------E
        # Phone Number------------------------------------S
        self.phoneNumberLabel = Label(
            self.ticketFrame,
            text="Phone Number : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.phoneNumberLabel.grid(row=3, column=0, padx=20, pady=20)
        self.phoneNumberShowLabel = Label(
            self.ticketFrame,
            text=ticket["phoneNumber"],
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.phoneNumberShowLabel.grid(row=3, column=1, padx=40, pady=20)
        # Phone Number------------------------------------E
        # Airlines----------------------------------------S
        self.airlineLabel = Label(
            self.ticketFrame,
            text="Airlines : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.airlineLabel.grid(row=4, column=0, padx=20, pady=20)
        self.airlineShowLabel = Label(
            self.ticketFrame,
            text=ticket["airlineName"],
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.airlineShowLabel.grid(row=4, column=1, padx=40, pady=20)
        # Airlines----------------------------------------E
        # Flight Number-----------------------------------S
        self.flightNumberLabel = Label(
            self.ticketFrame,
            text="Flight Number : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.flightNumberLabel.grid(row=5, column=0, padx=20, pady=20)
        self.flightNumberShowLabel = Label(
            self.ticketFrame,
            text=ticket["flightNumber"],
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.flightNumberShowLabel.grid(row=5, column=1, padx=40, pady=20)
        # Flight Number-----------------------------------E
        # Departure---------------------------------------S
        Label(
            self.ticketFrame,
            text="Departure : ",
            padx=50,
            pady=20,
            font="havetica 12 bold",
            bg="#232946",
            fg="#fffffe",
        ).grid(row=6, column=0, columnspan=2)
        # Departure Airport-------------------------------S
        self.departureLabel = Label(
            self.ticketFrame,
            text="Airport : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.departureLabel.grid(row=7, column=0, padx=20, pady=20)
        self.departureShowLabel = Label(
            self.ticketFrame,
            text=ticket["departure"]["airport"],
            bg="#232946",
            fg="#fffffe",
        )
        self.departureShowLabel.grid(row=7, column=1, padx=40, pady=20)
        # Departure Airport-------------------------------E
        # Departure Airport Code--------------------------S
        self.departureAirportCodeLabel = Label(
            self.ticketFrame,
            text="Airport Code : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.departureAirportCodeLabel.grid(row=8, column=0, padx=20, pady=20)
        self.departureAirportCodeShowLabel = Label(
            self.ticketFrame,
            text=ticket["departure"]["iata"],
            bg="#232946",
            fg="#fffffe",
        )
        self.departureAirportCodeShowLabel.grid(row=8, column=1, padx=40, pady=20)
        # Departure Airport Code--------------------------E
        # Departure Time----------------------------------S
        self.departureTimeLabel = Label(
            self.ticketFrame,
            text="Date & Time : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.departureTimeLabel.grid(row=9, column=0, padx=20, pady=20)
        self.departureTimeShowLabel = Label(
            self.ticketFrame,
            text=deptTime.strftime("%Y/%m/%d %H:%M:%S"),
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.departureTimeShowLabel.grid(row=9, column=1, padx=40, pady=20)
        # Departure Time----------------------------------E
        # Departure Airport Terminal----------------------S
        self.departureAirportTerminalLabel = Label(
            self.ticketFrame,
            text="Terminal : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.departureAirportTerminalLabel.grid(row=10, column=0, padx=20, pady=20)
        self.departureAirportTerminalShowLabel = Label(
            self.ticketFrame,
            text=ticket["departure"]["terminal"],
            bg="#232946",
            fg="#fffffe",
        )
        self.departureAirportTerminalShowLabel.grid(row=10, column=1, padx=40, pady=20)
        # Departure Airport Terminal----------------------E
        # Departure Airport Gate--------------------------S
        self.departureAirportGateLabel = Label(
            self.ticketFrame,
            text="Gate : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.departureAirportGateLabel.grid(row=11, column=0, padx=20, pady=20)
        self.departureAirportGateShowLabel = Label(
            self.ticketFrame,
            text=ticket["departure"]["gate"],
            bg="#232946",
            fg="#fffffe",
        )
        self.departureAirportGateShowLabel.grid(row=11, column=1, padx=40, pady=20)
        # Departure Airport Gate--------------------------E
        # Departure---------------------------------------E
        # Arrival-----------------------------------------S
        # Arrival Airport---------------------------------S
        Label(
            self.ticketFrame,
            text="Arrival : ",
            padx=50,
            pady=20,
            font="havetica 12 bold",
            bg="#232946",
            fg="#fffffe",
        ).grid(row=12, column=0, columnspan=2)
        # Arrival Airport---------------------------------S
        self.arrivalLabel = Label(
            self.ticketFrame,
            text="Airport : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalLabel.grid(row=13, column=0, padx=20, pady=20)
        self.arrivalShowLabel = Label(
            self.ticketFrame,
            text=ticket["arrival"]["airport"],
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalShowLabel.grid(row=13, column=1, padx=40, pady=20)
        # Arrival Airport---------------------------------E
        # Arrival Airport Code----------------------------S
        self.arrivalAirportCodeLabel = Label(
            self.ticketFrame,
            text="Airport Code : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalAirportCodeLabel.grid(row=14, column=0, padx=20, pady=20)
        self.arrivalAirportCodeShowLabel = Label(
            self.ticketFrame,
            text=ticket["arrival"]["iata"],
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalAirportCodeShowLabel.grid(row=14, column=1, padx=40, pady=20)
        # Arrival Airport Code----------------------------E
        # Arrival Time------------------------------------S
        self.arrivalTimeLabel = Label(
            self.ticketFrame,
            text="Date & Time : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.arrivalTimeLabel.grid(row=15, column=0, padx=20, pady=20)
        self.arrivalTimeShowLabel = Label(
            self.ticketFrame,
            text=arrTime.strftime("%Y/%m/%d %H:%M:%S"),
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.arrivalTimeShowLabel.grid(row=15, column=1, padx=40, pady=20)
        # Arrival Time------------------------------------E
        # Arrival Airport Terminal------------------------S
        self.arrivalAirportTerminalLabel = Label(
            self.ticketFrame,
            text="Terminal : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalAirportTerminalLabel.grid(row=16, column=0, padx=20, pady=20)
        self.arrivalAirportTerminalShowLabel = Label(
            self.ticketFrame,
            text=ticket["arrival"]["terminal"],
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalAirportTerminalShowLabel.grid(row=16, column=1, padx=40, pady=20)
        # Arrival Airport Terminal------------------------E
        # Arrival Airport Gate----------------------------S
        self.arrivalAirportGateLabel = Label(
            self.ticketFrame,
            text="Gate : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalAirportGateLabel.grid(row=17, column=0, padx=20, pady=20)
        self.arrivalAirportGateShowLabel = Label(
            self.ticketFrame,
            text=ticket["arrival"]["gate"],
            bg="#232946",
            fg="#fffffe",
        )
        self.arrivalAirportGateShowLabel.grid(row=17, column=1, padx=40, pady=20)
        # Arrival Airport Gate----------------------------E
        # Arrival-----------------------------------------E
        # Travel Time-------------------------------------S
        self.travelTimeLabel = Label(
            self.ticketFrame,
            text="Travel Time : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.travelTimeLabel.grid(row=18, column=0, padx=20, pady=20)
        self.travelTimeShowLabel = Label(
            self.ticketFrame,
            text=str(ticket["travelTime"]["hours"])
            + "hrs "
            + str(ticket["travelTime"]["minutes"])
            + "mins",
            bg="#232946",
            fg="#fffffe",
        )
        self.travelTimeShowLabel.grid(row=18, column=1, padx=40, pady=20)
        # Travel Time-------------------------------------E
        # Show Seat Details-------------------------------S
        Label(
            self.ticketFrame,
            text="Seat Allotment : ",
            padx=50,
            pady=20,
            font="havetica 12 bold",
            bg="#232946",
            fg="#fffffe",
        ).grid(row=19, column=0, columnspan=2)
        self.showSeatDetailsFrame = Frame(self.ticketFrame, padx=30, width=410, pady=20)
        self.showSeatDetailsFrame.config(bg="#eebbc3")
        for (seatIndex, seatInfo) in enumerate(ticket["bookedSeats"]):
            # Seat Number---------------------------------S
            self.seatNumberLabel = Label(
                self.showSeatDetailsFrame,
                text=seatInfo["row"] + str(seatInfo["column"]),
                padx=10,
                pady=10,
                bg="#eebbc3",
            )
            self.seatNumberLabel.grid(
                row=seatIndex,
                column=0,
                padx=20,
                pady=10,
            )
            # Seat Number---------------------------------E
            # Name----------------------------------------S
            self.seatNameLabel = Label(
                self.showSeatDetailsFrame,
                wraplength=150,
                padx=10,
                pady=10,
                bg="#eebbc3",
                text=seatInfo["name"],
            )
            self.seatNameLabel.grid(
                row=seatIndex,
                column=1,
                padx=20,
                pady=10,
            )
            # Name----------------------------------------E
            # Age-----------------------------------------S
            self.seatAgeLabel = Label(
                self.showSeatDetailsFrame,
                wraplength=150,
                padx=10,
                pady=10,
                bg="#eebbc3",
                text=seatInfo["age"],
            )
            self.seatAgeLabel.grid(
                row=seatIndex,
                column=2,
                padx=20,
                pady=10,
            )
            # Age-----------------------------------------E
        self.showSeatDetailsFrame.grid(row=20, column=0, columnspan=2, pady=20)
        # Show Seat Details-------------------------------E
        # Toatl Cost--------------------------------------S
        self.costLabel = Label(
            self.ticketFrame,
            text="Cost : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.costLabel.grid(row=21, column=0, pady=20)
        self.individualCostLabel = Label(
            self.ticketFrame,
            text=str(len(ticket["bookedSeats"])) + " x " + str(ticket["cost"]),
            bg="#232946",
            fg="#fffffe",
        )
        self.individualCostLabel.grid(row=21, column=1, pady=20)
        self.totalCostLabel = Label(
            self.ticketFrame,
            text=str(len(ticket["bookedSeats"]) * ticket["cost"]),
            bg="#232946",
            fg="#fffffe",
        )
        self.totalCostLabel.grid(row=21, column=2, pady=20)
        # Total Cost--------------------------------------E
        # Cancel Ticket-----------------------------------S
        self.cancelTicketButton = Button(
            self.ticketFrame,
            text="Cancel Ticket",
            bg="#d34745",
            fg="#fff",
            padx=20,
            pady=10,
            command=self.cancelTicket,
        )
        self.cancelTicketButton.grid(row=22, column=1, pady=20, columnspan=2)
        # Cancel Ticket-----------------------------------E
        # Send Ticket To Email----------------------------S
        self.sendTicketToEmailButton = Button(
            self.ticketFrame,
            text="Send Ticket to Email",
            bg="#eebbc3",
            fg="#000",
            padx=20,
            pady=10,
            command=lambda t=ticket, dt=deptTime, at=arrTime: self.checkEmailForTicketSending(
                t, dt, at
            ),
        )
        self.sendTicketToEmailButton.grid(row=22, column=0, pady=20, padx=30)
        # Send Ticket To Email----------------------------E
        # ------------------------------------------------E
        self.scrollBarTicket.pack(side=RIGHT, fill=Y)
        self.canvasTicket.pack(fill=BOTH, expand=1, side=LEFT)
        self.canvasTicket.configure(yscrollcommand=self.scrollBarTicket.set)
        self.canvasTicket.bind(
            "<Configure>",
            lambda e: self.canvasTicket.configure(
                scrollregion=self.canvasTicket.bbox("all")
            ),
        )

        self.app.mainloop()

    # show booking histroy
    def showBookingHistroy(self):
        self.ticketHistroyFrame = Frame(
            self.profileFrame, width=550, padx=70, pady=20, bg="#fef6e4"
        )
        bgColor = "#f582ae"
        fgColor = "#000"
        for (index, ticket) in enumerate(self.user["bookedSeats"]):
            self.containerFrame = Frame(
                self.ticketHistroyFrame,
                bg=bgColor,
                padx=30,
                pady=20,
                highlightbackground="#001858",
                highlightthickness=3,
            )
            # row0 ---------------------------------------S
            self.emptySpace1 = Label(
                self.containerFrame,
                text="                                 ",
                bg=bgColor,
            )
            self.emptySpace1.grid(row=0, column=0, pady=0)

            # airline Name
            self.airlineName = Label(
                self.containerFrame,
                text=ticket["airlineName"],
                font="Helvetica 12 bold",
                bg=bgColor,
                fg=fgColor,
            )
            self.airlineName.grid(row=0, column=1, pady=0)

            self.emptySpace2 = Label(
                self.containerFrame,
                text="                                 ",
                bg=bgColor,
            )
            self.emptySpace2.grid(row=0, column=2, pady=0)
            # row0 ---------------------------------------E
            # row1 ---------------------------------------S
            self.departureAirport = Label(
                self.containerFrame,
                text=ticket["departure"]["airport"],
                bg=bgColor,
                fg=fgColor,
                wraplength=150,
            )
            self.departureAirport.grid(row=1, column=0)
            self.emptySpaceOne = Label(
                self.containerFrame, text=" ", fg=fgColor, bg=bgColor, padx=100, pady=10
            )
            self.emptySpaceOne.grid(row=1, column=1)
            self.arrivalAirport = Label(
                self.containerFrame,
                text=ticket["arrival"]["airport"],
                bg=bgColor,
                fg=fgColor,
                wraplength=150,
            )
            self.arrivalAirport.grid(row=1, column=2)
            # row1 ---------------------------------------E
            # row2 ---------------------------------------S
            # ---------calculate Departure Time-----------S
            self.convertDepartureTime = datetime.datetime(
                *ticket["departure"]["departureUTCTime"]
            )
            self.convertDepartureTime = self.convertDepartureTime.replace(
                tzinfo=tz.gettz("UTC")
            )
            self.convertDepartureTime = self.convertDepartureTime.astimezone(
                tz.tzlocal()
            )
            # ---------calculate Departure Time-----------E
            # ---------calculate Arrival Time-------------S
            self.convertArrivalTime = datetime.datetime(
                *ticket["arrival"]["arrivalUTCTime"]
            )
            self.convertArrivalTime = self.convertArrivalTime.replace(
                tzinfo=tz.gettz("UTC")
            )
            self.convertArrivalTime = self.convertArrivalTime.astimezone(tz.tzlocal())
            # ---------calculate Arrival Time-------------E
            self.departureTime = Label(
                self.containerFrame,
                text=self.convertDepartureTime.strftime("%Y/%m/%d  %H:%M:%S"),
                bg=bgColor,
                fg=fgColor,
                wraplength=150,
            )
            self.departureTime.grid(row=2, column=0)
            self.emptySpaceTwo = Label(
                self.containerFrame, text=" ", fg=fgColor, bg=bgColor, padx=100, pady=10
            )
            self.emptySpaceTwo.grid(row=2, column=1)
            self.arrivalTime = Label(
                self.containerFrame,
                text=self.convertArrivalTime.strftime("%Y/%m/%d  %H:%M:%S"),
                bg=bgColor,
                fg=fgColor,
                wraplength=150,
            )
            self.arrivalTime.grid(row=2, column=2)
            # row2 ---------------------------------------E
            # row3 ---------------------------------------S
            self.ticketCount = Label(
                self.containerFrame,
                text=str(len(ticket["bookedSeats"])) + " ticket",
                bg=bgColor,
                fg=fgColor,
                wraplength=150,
            )
            self.ticketCount.grid(row=3, column=0)
            self.emptySpaceThree = Label(
                self.containerFrame, text=" ", fg=fgColor, bg=bgColor, padx=100, pady=10
            )
            self.emptySpaceThree.grid(row=3, column=1)
            self.totalCost = Label(
                self.containerFrame,
                text=len(ticket["bookedSeats"]) * ticket["cost"],
                bg=bgColor,
                fg=fgColor,
                wraplength=150,
            )
            self.totalCost.grid(row=3, column=2)
            # row3 ---------------------------------------E
            self.containerFrame.pack()
            self.ticket = ticket
            # add click listerner-------------------------S
            self.containerFrame.bind(
                "<Button-1>",
                lambda event, i=index: self.showTicketInfo(
                    self.ticket,
                    self.convertDepartureTime,
                    self.convertArrivalTime,
                    i,
                ),
            )
            # add click listerner-------------------------E
        self.ticketHistroyFrame.grid(row=8, column=0, columnspan=3)

    def __init__(self, user, parent):
        self.user = user
        self.parent = parent
        self.profileWindow = Tk()
        self.profileWindow.geometry("758x500")
        self.profileWindow.title(self.user["name"])
        self.canvas = Canvas(
            self.profileWindow,
            width=550,
            # bg="#eff0f3"
            bg="#000",
        )
        self.scrollBar = Scrollbar(
            self.profileWindow, orient=VERTICAL, command=self.canvas.yview
        )
        # default Colors----------------------------------S
        bgColor = "#fef6e4"
        fgColor = "#000"
        inputBgColor = "#f3d2c1"
        # default Colors----------------------------------E
        self.profileFrame = Frame(self.canvas, bg=bgColor, padx=50, width=550, pady=20)
        self.canvas.create_window((0, 0), window=self.profileFrame, anchor="nw")
        # display profile---------------------------------S
        # Back Button ------------------------------------S
        Button(
            self.profileFrame,
            text="Back",
            padx=10,
            pady=5,
            bg="#f582ae",
            fg="#000",
            activebackground="#8bd3dd",
            activeforeground="#001858",
            command=self.goBack,
        ).grid(
            row=0,
            column=0,
        )
        # Back Button ------------------------------------E
        # name label -------------------------------------S
        self.nameLabel = Label(
            self.profileFrame, text="Name : ", bg=bgColor, fg=fgColor, font="bold"
        )
        self.nameLabel.grid(row=1, column=0, padx=30, pady=20)
        # name label -------------------------------------E
        # name Input -------------------------------------S
        self.nameInput = Entry(self.profileFrame)
        self.nameInput.configure(
            justify=CENTER,
            bg=inputBgColor,
            fg=fgColor,
            font="bold",
            relief=FLAT,
        )
        self.nameInput.insert(0, self.user["name"])
        self.nameInput.grid(row=1, column=1)
        # name Input -------------------------------------E
        # email label -------------------------------------S
        self.emailLabel = Label(
            self.profileFrame, text="Email : ", bg=bgColor, fg=fgColor, font="bold"
        )
        self.emailLabel.grid(row=2, column=0, padx=30, pady=20)
        # email label -------------------------------------E
        # email Input -------------------------------------S
        self.emailInput = Label(self.profileFrame, text=self.user["email"])
        self.emailInput.configure(
            justify=CENTER,
            bg=bgColor,
            fg=fgColor,
            font="bold",
            relief=FLAT,
        )
        self.emailInput.grid(row=2, column=1)
        # email Input -------------------------------------E
        # gender label ------------------------------------S
        self.genderLabel = Label(
            self.profileFrame, text="Gender : ", bg=bgColor, fg=fgColor, font="bold"
        )
        self.genderLabel.grid(row=3, column=0, padx=0, pady=20)
        # gender label ------------------------------------E
        # gender Input ------------------------------------S
        self.genderVar = IntVar()
        self.genderVar.set(1 if self.user["gender"] == "Male" else 0)
        self.maleButton = Radiobutton(
            self.profileFrame,
            text="Male",
            variable=self.genderVar,
            value=1,
            selectcolor="#fff",
            bg="#f3d2c1",
            fg="#000",
            font="Havetica 10 bold",
        )
        self.femaleButton = Radiobutton(
            self.profileFrame,
            text="Female",
            variable=self.genderVar,
            value=2,
            selectcolor="#fff",
            bg="#f3d2c1",
            fg="#000",
            font="Havetica 10 bold",
        )
        self.maleButton.grid(row=3, column=1)
        self.femaleButton.grid(row=3, column=2)
        # gender Input -----------------------------------E
        # DOB label --------------------------------------S
        self.dobLabel = Label(
            self.profileFrame, text="DOB : ", bg=bgColor, fg=fgColor, font="bold"
        )
        self.dobLabel.grid(row=4, column=0, padx=30, pady=20)
        # DOB label --------------------------------------E
        # DOB Input --------------------------------------S
        self.dobVar = StringVar()
        self.dobVar.set(self.user["dob"])
        self.dobInput = Button(
            self.profileFrame,
            text=self.dobVar.get(),
            bg="#f582ae",
            fg="#000",
            activebackground="#8bd3dd",
            activeforeground="#001858",
            padx=5,
            pady=3,
            font="Havetica 10 bold",
            command=self.datePicker,
            relief=FLAT,
        )
        self.dobInput.grid(row=4, column=1)
        # DOB Input --------------------------------------E
        # Phone Number label------------------------------S
        self.phoneNumberLabel = Label(
            self.profileFrame,
            text="Phone Number : ",
            bg=bgColor,
            fg=fgColor,
            font="bold",
        )
        self.phoneNumberLabel.grid(row=5, column=0, padx=30, pady=20)
        # Phone Number label------------------------------E
        # Phone Number Input------------------------------S
        self.phoneNumberInput = Entry(self.profileFrame)
        self.phoneNumberInput.configure(
            justify=CENTER,
            bg=inputBgColor,
            fg=fgColor,
            font="bold",
            relief=FLAT,
        )
        self.phoneNumberInput.insert(0, self.user["phonenumber"])
        self.phoneNumberInput.grid(row=5, column=1)
        # Phone Number Input------------------------------E
        # Update Profile Button---------------------------S
        self.updateProfileButton = Button(
            self.profileFrame,
            text="Update Profile",
            padx=5,
            pady=3,
            font="havetica 10 bold",
            bg="#8bd3dd",
            fg="#000",
            activebackground="#f582ae",
            activeforeground="#001858",
            command=self.updateProfile,
        )
        self.updateProfileButton.grid(row=6, column=0, columnspan=2, pady=20)
        # Update Profile Button---------------------------E
        # Show Booked Histroy---------------------------S
        Label(
            self.profileFrame,
            text="Booking Histroy",
            bg="#f3d2c1",
            font="havetica 12 bold",
            padx=100,
            pady=10,
        ).grid(row=7, column=0, columnspan=3, pady=30)
        self.showBookingHistroy()
        # Show Booked Histroy---------------------------E
        # display profile---------------------------------E
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(fill=BOTH, expand=1, side=LEFT)
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.profileWindow.mainloop()


# Search Page
class SearchPage:
    allFlights = {}
    date = []
    departure = set()
    arrival = set()

    def finishBooking(self, data, deptTime, arrTime, cost, index):
        # update seat locally
        seats = []
        for (index, seat) in enumerate(self.bookedSeats):
            data["seatsGraph"][ascii_uppercase.index(seat["row"])][seat["column"]] = 0
            seats.append(
                {
                    "row": seat["row"],
                    "column": seat["column"],
                    "name": self.infoOfBookedSeats[index][0].get(),
                    "age": self.infoOfBookedSeats[index][1].get(),
                }
            )
        self.allFlights[self.selectedDate.get()][index] = data
        # update booked seats in DB
        flightCollection.update_one(
            {"date": self.selectedDate.get()},
            {"$set": {"data": self.allFlights[self.selectedDate.get()]}},
        )
        # update tickets in User Profile
        updateBookingData = {
            "departure": data["departure"],
            "arrival": data["arrival"],
            "travelTime": data["travelTime"],
            "airlineName": data["airlineName"],
            "flightNumber": data["flightNumber"],
            "bookedSeats": seats,
            "email": self.emailInput.get(),
            "phoneNumber": self.phoneNumberInput.get(),
            "bookingID": "".join(
                random.choices(string.ascii_uppercase + string.digits, k=9)
            ),
            "cost": cost,
        }
        self.user["bookedSeats"].append(updateBookingData)
        profileCollection.update_one(
            {"_id": self.user["_id"]},
            {"$set": {"bookedSeats": self.user["bookedSeats"]}},
        )
        # send ticket to email
        emailClient = yagmail.SMTP(
            "messikarthik13@gmail.com",
            keyring.get_password("gmail", "messikarthik13@gmail.com"),
        )
        subjects = "Ticket for {0} on {1}".format(
            updateBookingData["airlineName"],
            str(updateBookingData["departure"]["departureUTCTime"][2])
            + "/"
            + str(updateBookingData["departure"]["departureUTCTime"][1])
            + "/"
            + str(updateBookingData["departure"]["departureUTCTime"][0])
            + "   "
            + str(updateBookingData["departure"]["departureUTCTime"][3])
            + ":"
            + str(updateBookingData["departure"]["departureUTCTime"][4]),
        )
        contents = "                        {0}               \n  Your Booking ID : {1}\n  Departure : \n     Airport : {2}\n     Code : {3}\n     Terminal : {4}\n     Gate : {5}\n     Time : {6}\n  Arrival   : \n     Airport : {7}\n     Code : {8}\n     Terminal : {9}\n     Gate : {10}\n     Time : {11}\n  Flight Number : {12}\n  Cost : {13}".format(
            updateBookingData["airlineName"],
            updateBookingData["bookingID"],
            updateBookingData["departure"]["airport"],
            updateBookingData["departure"]["iata"],
            updateBookingData["departure"]["terminal"],
            updateBookingData["departure"]["gate"],
            deptTime.strftime("%d/%m/%Y  %H:%M:%S"),
            updateBookingData["arrival"]["airport"],
            updateBookingData["arrival"]["iata"],
            updateBookingData["arrival"]["terminal"],
            updateBookingData["arrival"]["gate"],
            arrTime.strftime("%d/%m/%Y  %H:%M:%S"),
            updateBookingData["flightNumber"],
            updateBookingData["cost"],
        )
        seatGraphForEmail = []
        for i in seats:
            seatGraphForEmail.append(
                "\n  {0}      {1}     {2}\n".format(
                    i["row"] + str(i["column"]), i["name"], i["age"]
                )
            )
        contents += "".join(seatGraphForEmail)
        contents += "\n  Phone Number : {0}\n".format(updateBookingData["phoneNumber"])
        emailClient.send(self.emailInput.get(), subjects, contents)
        # show confirm booked messagex
        messagebox.showinfo(
            "Success",
            "Booking Confirmed , Check {0} for Ticket".format(self.emailInput.get()),
        )

    def confirmBooking(self, data, deptTime, arrTime, cost, index):
        try:
            if self.app:
                self.app.destroy()
        except:
            pass
        self.app = Tk()
        self.app.geometry("450x450")
        self.canvasTwo = Canvas(self.app, width=400, bg="#8ecae6")
        self.scrollBarTwo = Scrollbar(
            self.app, orient=VERTICAL, command=self.canvasTwo.yview
        )
        self.confirmBookingFrame = Frame(
            self.canvasTwo,
            bg="#8ecae6",
            padx=10,
            width=410,
        )
        self.canvasTwo.create_window(
            (0, 0), window=self.confirmBookingFrame, anchor="nw"
        )
        self.confirmBookingFrame.configure(bg="#232946")
        backButton = Button(
            self.confirmBookingFrame,
            text="Back",
            bg="#eebbc3",
            padx=10,
            pady=5,
            relief="flat",
            command=lambda d=data, dT=deptTime, aT=arrTime, c=cost, i=index: self.showFlightInfo(
                d, dT, aT, c, i
            ),
        )
        backButton.grid(row=0, column=0, pady=20, padx=20)
        Label(
            self.confirmBookingFrame,
            text="Confirm Your Booking",
            font="Halvetica 12 bold",
            fg="#fffffe",
            bg="#232946",
        ).grid(row=1, column=0, columnspan=4, pady=50)
        # Show Details-------------------------------
        # Departure----------------------------------
        self.confirmDepartureLabel = Label(
            self.confirmBookingFrame,
            text="Depature Airport : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.confirmDepartureLabel.grid(row=3, column=0, padx=20, pady=20)
        self.confirmDeparture = Label(
            self.confirmBookingFrame,
            text=data["departure"]["airport"],
            bg="#232946",
            fg="#fffffe",
        )
        self.confirmDeparture.grid(row=3, column=1, padx=40, pady=20)
        # Departure----------------------------------
        # Arrival------------------------------------
        self.confirmArrivalLabel = Label(
            self.confirmBookingFrame,
            text="Arrival Airport  : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.confirmArrivalLabel.grid(row=4, column=0, padx=20, pady=20)
        self.confirmArrival = Label(
            self.confirmBookingFrame,
            text=data["arrival"]["airport"],
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.confirmArrival.grid(row=4, column=1, padx=40, pady=20)
        # Arrival------------------------------------
        # Airlines-----------------------------------
        self.confirmAirlineLabel = Label(
            self.confirmBookingFrame,
            text="Airlines : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.confirmAirlineLabel.grid(row=5, column=0, padx=20, pady=20)
        self.confirmAirline = Label(
            self.confirmBookingFrame,
            text=data["airlineName"],
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.confirmAirline.grid(row=5, column=1, padx=40, pady=20)
        # Airlines-----------------------------------
        # Departure Time-----------------------------
        self.confirmDepartureTimeLabel = Label(
            self.confirmBookingFrame,
            text="Date & Time : ",
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.confirmDepartureTimeLabel.grid(row=6, column=0, padx=20, pady=20)
        self.confirmDepartureTime = Label(
            self.confirmBookingFrame,
            text=deptTime.strftime("%Y/%m/%d %H:%M:%S"),
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.confirmDepartureTime.grid(row=6, column=1, padx=40, pady=20)
        # Departure Time----------------------------
        # Show Email--------------------------------
        self.emailLabel = Label(
            self.confirmBookingFrame,
            text="Email : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.emailLabel.grid(row=7, column=0)
        self.emailInput = Entry(
            self.confirmBookingFrame,
        )
        self.emailInput.insert(0, self.user["email"])
        self.emailInput.grid(row=7, column=1, padx=40, pady=30)
        # Show Email--------------------------------
        # Get Name and age of all seats-------------
        self.containerFrameForSeatEntry = Frame(
            self.confirmBookingFrame, padx=10, width=410, pady=20
        )
        self.containerFrameForSeatEntry.config(bg="#eebbc3")
        self.infoOfBookedSeats = []
        for (index, seat) in enumerate(self.bookedSeats):

            self.seatLabel = Label(
                self.containerFrameForSeatEntry,
                text=seat["row"] + " " + str(seat["column"]),
                padx=10,
                pady=10,
                bg="#eebbc3",
            )
            self.seatLabel.grid(
                row=index,
                column=0,
                padx=20,
                pady=10,
            )
            self.infoOfBookedSeats.append(
                [
                    Entry(
                        self.containerFrameForSeatEntry,
                        justify=CENTER,
                        relief=RIDGE,
                    ),
                    Entry(
                        self.containerFrameForSeatEntry,
                        justify=CENTER,
                        relief=RIDGE,
                    ),
                ]
            )
            self.infoOfBookedSeats[-1][0].insert(0, "Enter Name")
            self.infoOfBookedSeats[-1][0].grid(row=index, column=1)
            Label(
                self.containerFrameForSeatEntry,
                text="    ",
                bg="#eebbc3",
            ).grid(row=index, column=2, padx=20, pady=10)
            self.infoOfBookedSeats[-1][1].insert(0, "Enter Age")
            self.infoOfBookedSeats[-1][1].grid(row=index, column=3)

        self.containerFrameForSeatEntry.grid(
            row=8,
            column=0,
            columnspan=2,
        )

        # Get Name and age of all seats-------------
        # Get Number--------------------------------
        self.phoneNumberLabel = Label(
            self.confirmBookingFrame,
            text="Phone Number : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.phoneNumberLabel.grid(row=9, column=0, padx=40, pady=20)
        self.phoneNumberInput = Entry(self.confirmBookingFrame)
        self.phoneNumberInput.insert(0, self.user["phonenumber"])
        self.phoneNumberInput.grid(row=9, column=1)
        # Get Number--------------------------------
        # Confirm Booking Button--------------------
        self.confirmBookingButton = Button(
            self.confirmBookingFrame,
            text="Book Tickets",
            padx=20,
            pady=10,
            bg="#eebbc3",
            relief=RAISED,
            activebackground="#b8c1ec",
            command=lambda d=data, dt=deptTime, at=arrTime, c=cost, i=index: self.finishBooking(
                d, dt, at, cost, i
            ),
        )
        self.confirmBookingButton.grid(row=10, column=0, columnspan=2, padx=40, pady=20)
        # Confirm Booking Button-----  ---------------
        self.scrollBarTwo.pack(side=RIGHT, fill=Y)
        self.canvasTwo.pack(fill=BOTH, expand=1, side=LEFT)
        self.canvasTwo.configure(yscrollcommand=self.scrollBarTwo.set)
        self.canvasTwo.bind(
            "<Configure>",
            lambda e: self.canvasTwo.configure(scrollregion=self.canvasTwo.bbox("all")),
        )

        self.app.mainloop()

    def updateSeatBookings(self, data, index, col):
        check = {"row": ascii_uppercase[index], "column": col}
        if check not in self.bookedSeats:
            if len(self.bookedSeats) == 10:
                messagebox.showerror("Error", "Maximum 10 seats can be selected")
            else:
                self.bookedSeats.append(check)
        else:
            self.bookedSeats.remove(check)
        self.showSeatGraph(data)

    def showSeatGraph(self, data):
        try:
            if self.seatLayoutContainer:
                self.seatLayoutContainer.destroy()
        except:
            pass
        seatWidth = 2
        padYAxis = 7
        padXAxis = 10
        backgroundSeat = "#8bd3dd"
        fgSeats = "#001858"
        # selectedSeat = "#abd1c6"
        selectedSeat = "#f582ae"
        self.seatLayoutContainer = Frame(self.containerFrameOne, bg="#f3d2c1")
        for (index, char) in enumerate(ascii_uppercase):
            self.seatZero = Button(
                self.seatLayoutContainer,
                text="0",
                width=seatWidth,
                fg=fgSeats,
                bg=selectedSeat
                if {"row": char, "column": 0} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][0] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][0] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 0),
            )
            self.seatZero.grid(row=index, column=0, pady=padYAxis, padx=padXAxis)
            self.seatOne = Button(
                self.seatLayoutContainer,
                text="1",
                width=seatWidth,
                fg=fgSeats,
                bg=selectedSeat
                if {"row": char, "column": 1} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][1] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][1] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 1),
            )
            self.seatOne.grid(row=index, column=1, pady=padYAxis, padx=padXAxis)
            self.seatTwo = Button(
                self.seatLayoutContainer,
                text="2",
                width=seatWidth,
                fg=fgSeats,
                bg=selectedSeat
                if {"row": char, "column": 2} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][2] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][2] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 2),
            )
            self.seatTwo.grid(row=index, column=2, pady=padYAxis, padx=padXAxis)
            seatIdLabel = Label(
                self.seatLayoutContainer,
                text=char,
                fg="#000",
                bg="#f3d2c1",
            )
            seatIdLabel.grid(row=index, column=3, pady=padYAxis, padx=padXAxis)
            self.seatThree = Button(
                self.seatLayoutContainer,
                text="3",
                width=seatWidth,
                fg=fgSeats,
                bg=selectedSeat
                if {"row": char, "column": 3} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][3] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][3] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 3),
            )
            self.seatThree.grid(row=index, column=4, pady=padYAxis, padx=padXAxis)
            self.seatFour = Button(
                self.seatLayoutContainer,
                text="4",
                width=seatWidth,
                fg=fgSeats,
                bg=selectedSeat
                if {"row": char, "column": 4} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][4] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][4] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 4),
            )
            self.seatFour.grid(row=index, column=5, pady=padYAxis, padx=padXAxis)
            self.seatFive = Button(
                self.seatLayoutContainer,
                text="5",
                width=seatWidth,
                fg=fgSeats,
                bg=selectedSeat
                if {"row": char, "column": 5} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][5] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][5] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 5),
            )
            self.seatFive.grid(row=index, column=6, pady=padYAxis, padx=padXAxis)
            self.seatLayoutContainer.grid(row=11, column=0, columnspan=4, pady=10)
        # row11--------------------------------------------------

    def showFlightInfo(self, data, deptTime, arrTime, cost, index):
        print(self.user)
        try:
            if self.app:
                self.app.destroy()
        except:
            pass
        self.app = Tk()
        self.app.geometry("450x400")
        self.bookedSeats = []
        self.canvasOne = Canvas(self.app, width=450, bg="#fef6e4")
        self.scrollBarOne = Scrollbar(
            self.app, orient=VERTICAL, command=self.canvasOne.yview
        )
        self.containerFrameOne = Frame(self.canvasOne, padx=10, width=380, bg="#fef6e4")
        self.canvasOne.create_window((0, 0), window=self.containerFrameOne, anchor="nw")
        self.scrollBarOne.pack(side=RIGHT, fill=Y)
        self.canvasOne.pack(fill=BOTH, expand=1, side=LEFT)
        self.canvasOne.configure(yscrollcommand=self.scrollBarOne.set)
        self.canvasOne.bind(
            "<Configure>",
            lambda e: self.canvasOne.configure(scrollregion=self.canvasOne.bbox("all")),
        )
        # row0---------------------------------------------------
        emptySpaceOne1 = Label(self.containerFrameOne, text="", width=15, bg="#fef6e4")
        emptySpaceOne1.grid(row=0, column=0)
        departureLabelOne = Label(
            self.containerFrameOne, text="Departure", width=20, bg="#fef6e4"
        )
        departureLabelOne.grid(row=0, column=1, pady=20)
        arrivalLabelOne = Label(
            self.containerFrameOne, text="Arrival", width=20, bg="#fef6e4"
        )
        arrivalLabelOne.grid(row=0, column=2)
        # row0---------------------------------------------------
        # row1---------------------------------------------------
        airportOne = Label(
            self.containerFrameOne, text="Airport", width=18, bg="#fef6e4"
        )
        airportOne.grid(row=1, column=0)
        aiportDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["airport"],
            width=20,
            height=4,
            wraplength=100,
            bg="#fef6e4",
        )
        aiportDepartureOne.grid(row=1, column=1, pady=7)
        airportArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["airport"],
            width=20,
            bg="#fef6e4",
            height=4,
            wraplength=100,
        )
        airportArrivalOne.grid(row=1, column=2)
        # row1---------------------------------------------------
        # row2---------------------------------------------------
        airportCodeOne = Label(
            self.containerFrameOne, text="Airport Code", width=18, bg="#fef6e4"
        )
        airportCodeOne.grid(row=2, column=0)
        airportCodeDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["iata"],
            width=20,
            height=4,
            wraplength=100,
            bg="#fef6e4",
        )
        airportCodeDepartureOne.grid(row=2, column=1, pady=7)
        airportCodeArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["iata"],
            width=20,
            bg="#fef6e4",
            wraplength=100,
        )
        airportCodeArrivalOne.grid(row=2, column=2)
        # row2---------------------------------------------------

        # row3---------------------------------------------------
        cityOne = Label(self.containerFrameOne, text="City", width=18, bg="#fef6e4")
        cityOne.grid(row=3, column=0)
        cityDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["timezone"],
            width=20,
            height=4,
            wraplength=100,
            bg="#fef6e4",
        )
        cityDepartureOne.grid(row=3, column=1, pady=7)
        cityArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["timezone"],
            width=20,
            bg="#fef6e4",
            wraplength=100,
        )
        cityArrivalOne.grid(row=3, column=2)
        # row3---------------------------------------------------
        # row4---------------------------------------------------
        terminalOne = Label(
            self.containerFrameOne, text="Terminal", width=18, bg="#fef6e4"
        )
        terminalOne.grid(row=4, column=0)
        terminalDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["terminal"],
            width=20,
            height=4,
            wraplength=100,
            bg="#fef6e4",
        )
        terminalDepartureOne.grid(row=4, column=1, pady=7)
        terminalArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["terminal"],
            width=20,
            bg="#fef6e4",
            wraplength=100,
        )
        terminalArrivalOne.grid(row=4, column=2)
        # row4---------------------------------------------------
        # row5---------------------------------------------------
        timeOne = Label(self.containerFrameOne, text="Time", width=18, bg="#fef6e4")
        timeOne.grid(row=5, column=0)
        timeDepartureOne = Label(
            self.containerFrameOne,
            text=deptTime.strftime("%d/%m/%Y  %H:%M:%S"),
            width=20,
            height=4,
            wraplength=100,
            bg="#fef6e4",
        )
        timeDepartureOne.grid(row=5, column=1, pady=7)
        timeArrivalOne = Label(
            self.containerFrameOne,
            text=arrTime.strftime("%d/%m/%Y  %H:%M:%S"),
            width=20,
            bg="#fef6e4",
            wraplength=100,
        )
        timeArrivalOne.grid(row=5, column=2)
        # row5---------------------------------------------------
        # row6---------------------------------------------------
        gateOne = Label(self.containerFrameOne, text="Gate", width=18, bg="#fef6e4")
        gateOne.grid(row=6, column=0)
        gateDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["gate"],
            width=20,
            height=4,
            wraplength=100,
            bg="#fef6e4",
        )
        gateDepartureOne.grid(row=6, column=1, pady=7)
        gateArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["gate"],
            width=20,
            bg="#fef6e4",
            wraplength=100,
        )
        gateArrivalOne.grid(row=6, column=2)
        # row6---------------------------------------------------
        # row7---------------------------------------------------
        travelTimeLabelOne = Label(
            self.containerFrameOne,
            text="Travel Time",
            width=18,
            bg="#fef6e4",
        )
        travelTimeLabelOne.grid(row=7, column=0)
        travelTimeOne = Label(
            self.containerFrameOne,
            text=str(data["travelTime"]["hours"])
            + "hrs  "
            + str(data["travelTime"]["minutes"])
            + "mins",
            font="Halevtia 12",
            width=20,
            height=4,
            wraplength=100,
            bg="#fef6e4",
        )
        travelTimeOne.grid(row=7, column=1, pady=7, columnspan=2)
        # row7---------------------------------------------------
        # row8---------------------------------------------------
        airlineLabelOne = Label(
            self.containerFrameOne, text="Airline", width=18, bg="#fef6e4"
        )
        airlineLabelOne.grid(row=8, column=0)
        airlineOne = Label(
            self.containerFrameOne,
            text=data["airlineName"],
            width=20,
            height=4,
            font="Halevtia 12",
            wraplength=100,
            bg="#fef6e4",
        )
        airlineOne.grid(row=8, column=1, pady=7, columnspan=2)
        # row8---------------------------------------------------
        # row9---------------------------------------------------
        flightNumberLabelOne = Label(
            self.containerFrameOne, text="Flight Number", width=18, bg="#fef6e4"
        )
        flightNumberLabelOne.grid(row=9, column=0)
        flightNumberOne = Label(
            self.containerFrameOne,
            text=data["flightNumber"],
            width=20,
            height=4,
            font="Halevtia 12",
            wraplength=100,
            bg="#fef6e4",
        )
        flightNumberOne.grid(row=9, column=1, pady=7, columnspan=2)
        # row9---------------------------------------------------
        # row10--------------------------------------------------
        selectSeatLabel = Label(
            self.containerFrameOne,
            text="Select your Seat",
            bg="#fef6e4",
            font="Halevtia 12 bold",
        )
        selectSeatLabel.grid(row=10, column=0, columnspan=3, pady=10)
        # row10--------------------------------------------------
        # row11--------------------------------------------------
        # display all the seats----------------------------------
        self.showSeatGraph(data)
        self.bookTickets = Button(
            self.containerFrameOne,
            text="Book Your Tickets",
            bg="#f3d2c1",
            fg="#001858",
            font="Halvetica 8 bold",
            command=lambda d=data, dT=deptTime, aT=arrTime, c=cost, i=index: self.confirmBooking(
                d, dT, aT, c, i
            ),
            padx=10,
            pady=5,
        )
        self.bookTickets.grid(row=12, column=0, columnspan=3, rowspan=2, pady=20)
        self.app.mainloop()

    def displayFlights(self):
        if self.intVar.get() == 0:
            self.scrollFrame.destroy()
        self.scrollFrame = Frame(
            self.searchPage,
            width=450,
            bg="#55423d",
            padx=20,
            pady=20,
        )
        self.intVar.set(0)
        self.canvas = Canvas(self.scrollFrame, width=450, bg="#55423d")
        self.scrollBar = Scrollbar(
            self.scrollFrame, orient=VERTICAL, command=self.canvas.yview
        )
        self.containerFrame = Frame(
            self.canvas, padx=10, width=450, pady=10, bg="#ffc0ad"
        )
        self.canvas.create_window((0, 0), window=self.containerFrame, anchor="nw")
        # set flag for no flights
        flag = 0
        # display flights
        for (index, flightData) in enumerate(self.allFlights[self.selectedDate.get()]):
            # ---------calculate Departure Time-----------
            self.convertDepartureTime = datetime.datetime(
                *flightData["departure"]["departureUTCTime"]
            )
            self.convertDepartureTime = self.convertDepartureTime.replace(
                tzinfo=tz.gettz("UTC")
            )
            self.convertDepartureTime = self.convertDepartureTime.astimezone(
                tz.tzlocal()
            )
            # -------------------------------------------
            # ---------calculate Arrival Time------------
            self.convertArrivalTime = datetime.datetime(
                *flightData["arrival"]["arrivalUTCTime"]
            )
            self.convertArrivalTime = self.convertArrivalTime.replace(
                tzinfo=tz.gettz("UTC")
            )
            self.convertArrivalTime = self.convertArrivalTime.astimezone(tz.tzlocal())
            # -------------------------------------------
            # check for current date
            if (
                (
                    self.selectedDate.get()
                    != self.convertDepartureTime.strftime("%Y-%m-%d")
                )
                or (self.departureSelected.get() != flightData["departure"]["timezone"])
                or (self.arrivalSelected.get() != flightData["arrival"]["timezone"])
            ):
                continue
            flag = 1
            self.flightDisplayFrame = Frame(
                self.containerFrame,
                bg="#271c19",
                padx=20,
                pady=10,
                width=180,
            )
            # row0 ----------------------------------------
            self.emptySpace1 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#271c19",
            )
            self.emptySpace1.grid(row=0, column=0, pady=10)

            # airline Name
            self.airlineName = Label(
                self.flightDisplayFrame,
                text=flightData["airlineName"],
                font="Helvetica 12 bold",
                bg="#271c19",
                fg="#fff",
            )
            self.airlineName.grid(row=0, column=1, pady=10)

            self.emptySpace2 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#271c19",
            )
            self.emptySpace2.grid(row=0, column=2, pady=10)
            # row0 ----------------------------------------
            # row1 ----------------------------------------
            # Airport Departure
            self.airportDeparture = Label(
                self.flightDisplayFrame,
                text=flightData["departure"]["airport"],
                bg="#271c19",
                font="Helvetica 9 bold",
                wraplength=150,
                fg="#fff",
            )
            self.airportDeparture.grid(row=1, column=0, pady=10)

            self.emptySpace3 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#271c19",
            )
            self.emptySpace3.grid(row=1, column=1, pady=10)

            # Airport Arrival
            self.airportArrival = Label(
                self.flightDisplayFrame,
                text=flightData["arrival"]["airport"],
                bg="#271c19",
                font="Helvetica 9 bold",
                wraplength=100,
                fg="#fff",
            )
            self.airportArrival.grid(row=1, column=2, pady=10)
            # row1 ----------------------------------------

            # row2 ----------------------------------------
            # timezone Departure
            self.timezoneDeparture = Label(
                self.flightDisplayFrame,
                text=flightData["departure"]["timezone"],
                bg="#271c19",
                font="Helvetica 8 bold",
                wraplength=150,
                fg="#fff",
            )
            self.timezoneDeparture.grid(row=2, column=0, pady=10)

            self.emptySpace4 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#271c19",
            )
            self.emptySpace4.grid(row=2, column=1, pady=10)

            # timezone Arrival
            self.timezoneArrival = Label(
                self.flightDisplayFrame,
                text=flightData["arrival"]["timezone"],
                bg="#271c19",
                font="Helvetica 8 bold",
                wraplength=130,
                fg="#fff",
            )
            self.timezoneArrival.grid(row=2, column=2, pady=10)
            # row2 ----------------------------------------

            # row3 ----------------------------------------
            # time Departure
            self.departureTime = Label(
                self.flightDisplayFrame,
                text=self.convertDepartureTime.strftime("%Y/%m/%d  %H:%M:%S"),
                bg="#271c19",
                font="Helvetica 8 bold",
                wraplength=100,
                fg="#fff",
            )
            self.departureTime.grid(row=3, column=0, pady=10)

            self.emptySpace5 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#271c19",
            )
            self.emptySpace5.grid(row=3, column=1, pady=10)

            # time Arrival
            self.arrivalTime = Label(
                self.flightDisplayFrame,
                text=self.convertArrivalTime.strftime("%Y/%m/%d  %H:%M:%S"),
                bg="#271c19",
                font="Helvetica 8 bold",
                wraplength=100,
                fg="#fff",
            )
            self.arrivalTime.grid(row=3, column=2, pady=10)
            # row3 ----------------------------------------

            # row4 ----------------------------------------
            self.emptySpace6 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#271c19",
            )
            self.tripCost = random.randint(20000, 35000)
            self.emptySpace6.grid(row=4, column=0, pady=10)
            self.totalCost = Label(
                self.flightDisplayFrame,
                text="Cost : " + str(self.tripCost),
                font="Helvetica 12 bold",
                bg="#271c19",
                fg="#fff",
            )
            self.emptySpace7 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#271c19",
            )
            self.totalCost.grid(row=4, column=1, pady=10)
            self.emptySpace7.grid(row=4, column=2, pady=10)

            # row4 ----------------------------------------
            self.details = flightData
            self.flightDisplayFrame.pack(fill=BOTH, pady=10)
            self.flightDisplayFrame.bind(
                "<Button-1>",
                lambda event: self.showFlightInfo(
                    self.details,
                    self.convertDepartureTime,
                    self.convertArrivalTime,
                    self.tripCost,
                    index,
                ),
            )
        if flag == 0:
            x = Label(
                self.containerFrame,
                bg="#271c19",
                padx=20,
                pady=10,
                width=35,
                height=10,
                fg="#fff",
                text="No Flights, Sorry!!!",
                font="bold",
            )
            x.pack(fill=BOTH, expand=1, side=TOP)
        self.scrollBar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(fill=BOTH, expand=1, side=LEFT)
        self.canvas.configure(yscrollcommand=self.scrollBar.set)
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.scrollFrame.pack(fill=BOTH, expand=1)

    def getFromDate(self):
        self.departure = set()
        self.arrival = set()
        for i in self.allFlights[self.selectedDate.get()]:
            self.departure.add(i["departure"]["timezone"])
            self.arrival.add(i["arrival"]["timezone"])
        self.departureSelected = StringVar()
        self.departureSelected.set("From")
        self.arrivalSelected = StringVar()
        self.arrivalSelected.set("To")

        try:
            if self.departureOption:
                self.departureOption.destroy()
        except:
            pass
        try:
            if self.arrivalOption:
                self.arrivalOption.destroy()
        except:
            pass
        try:
            if self.searchButton:
                self.searchButton.destroy()
        except:
            pass

        # depature list
        self.departureOption = OptionMenu(
            self.frameForPack, self.departureSelected, *self.departure
        )
        self.departureOption.pack(side=LEFT, padx=4)
        # arrival list
        self.arrivalOption = OptionMenu(
            self.frameForPack, self.arrivalSelected, *self.arrival
        )
        self.arrivalOption.pack(side=RIGHT, padx=4)
        # search button
        self.searchButton = Button(
            self.frameForPack,
            text="Search",
            activebackground="#333945",
            activeforeground="#fff",
            bg="#d34745",
            fg="#fff",
            relief=RAISED,
            bd=4,
            padx=5,
            pady=3,
            command=self.displayFlights,
        )
        self.searchButton.pack()

    def __init__(self, parent, user):
        self.parent = parent
        self.user = user
        self.intVar = IntVar()
        self.intVar.set(1)
        self.searchPage = Frame(
            self.parent, bg="#271c19", padx=30, pady=30, width=450, height=400
        )
        # TODO: implement Porfile Page Button
        self.flightData = flightCollection.find()
        self.searchPage.pack(fill=BOTH, expand=1)
        for flight in self.flightData:
            self.allFlights[flight["date"]] = flight["data"]
            self.date.append(flight["date"])
        # profile page link
        self.frameForProfile = Frame(self.searchPage, bg="#000aaa", padx=20, pady=20)
        self.profileButton = Button(
            self.frameForProfile, text=self.user["name"], padx=20, pady=20
        )
        self.frameForProfile.pack(fill=BOTH, expand=1)
        # frame for date
        self.frameForPack = Frame(self.searchPage, bg="#ffc0ad", padx=20, pady=20)
        # date list
        self.selectedDate = StringVar()
        self.selectedDate.set("Select Date")
        self.dateOption = OptionMenu(self.frameForPack, self.selectedDate, *self.date)
        self.dateOption.pack()
        self.getFromTo = Button(
            self.frameForPack,
            text="Get",
            activebackground="#e78fb3",
            activeforeground="#fff",
            bg="#271c19",
            fg="#fff",
            relief=RAISED,
            bd=4,
            padx=3,
            pady=2,
            command=self.getFromDate,
        )
        self.getFromTo.pack(padx=10, pady=10)
        self.frameForPack.pack(fill=BOTH, expand=1)


# SignIn
class SignIn:
    def siginUser(self):
        self.emailValidation = re.match(
            "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", self.emailInput.get()
        )
        if self.emailValidation == None:
            messagebox.showerror("Error", "Please Enter Valid Email Address")
            return

        self.user = profileCollection.find_one({"email": self.emailInput.get()})

        if self.user == None:
            messagebox.showerror("Error", "User Does not exists")
            return

        if (
            bcrypt.checkpw(
                bytes(self.passwordInput.get(), "utf-8"), self.user["password"]
            )
            == False
        ):
            messagebox.showerror("Error", "Password does not match")
            return
        self.signInPage.destroy()
        self.search = SearchPage(self.parent, self.user)

    def goBack(self):
        self.signInPage.destroy()
        self.index = IndexPage(self.parent)

    def __init__(self, parent):
        self.parent = parent
        self.signInPage = Frame(
            self.parent,
            bg="#232946",
            padx=100,
            pady=100,
        )

        # Email
        self.emailLabel = Label(self.signInPage, text="Email", bg="#232946", fg="#fff")
        self.emailLabel.grid(row=0, column=0)
        self.emailInput = Entry(self.signInPage)
        self.emailInput.grid(row=0, column=1)

        # Password
        self.passwordLabel = Label(
            self.signInPage, text="Password", bg="#232946", padx=10, fg="#fff"
        )
        self.passwordLabel.grid(row=1, column=0)
        self.passwordInput = Entry(self.signInPage, show="*")
        self.passwordInput.grid(row=1, column=1, pady=5)

        # Signin Button
        self.signInButton = Button(
            self.signInPage,
            text="Sign In",
            activebackground="#b8c1ec",
            activeforeground="#121629",
            bg="#eebbc3",
            fg="#000",
            relief=RAISED,
            bd=4,
            command=self.siginUser,
        )
        self.signInButton.grid(row=2, column=1, columnspan=1, pady=20)
        # Back Button
        self.back = Button(
            self.signInPage,
            text="Back",
            activebackground="#eebbc3",
            bg="#b8c1ec",
            fg="#000",
            relief=RAISED,
            bd=4,
            command=self.goBack,
        )
        self.back.grid(row=2, column=2, pady=20)
        self.signInPage.grid(row=0, column=0)


# Register
class Register:
    def getDate(self):
        self.calendarFrame.destroy()
        self.var1.set(self.calendar.get_date())
        self.DOBInput.destroy()
        self.DOBInput = Button(
            self.registerPage,
            text=self.var1.get(),
            command=self.datePicker,
            bg="#ff8906",
            fg="#fffffe",
        )
        self.DOBInput.grid(row=3, column=1, pady=5)

    # Calendar
    def datePicker(self):
        self.calendarFrame = Tk()
        self.calendarFrame.title("Date Picker")
        self.calendar = Calendar(self.calendarFrame)
        self.calendar.pack()
        self.calendarButton = Button(
            self.calendarFrame,
            text="OK",
            activebackground="#d34745",
            activeforeground="#fff",
            bg="#31449E",
            fg="#fff",
            command=self.getDate,
        )
        self.calendarButton.pack()

    # Go Back
    def goBack(self):
        self.registerPage.destroy()
        self.index = IndexPage(self.parent)

    # Register User
    def registerUser(self):
        self.emailValidation = re.match(
            "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+", self.emailInput.get()
        )
        self.phoneNumberValidation = re.match(
            "^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$", self.numberInput.get()
        )
        if self.genderVar.get() == 0:
            messagebox.showerror("Error", "Please Select a Gender")
            return
        if self.phoneNumberValidation == None:
            messagebox.showerror("Error", "Please Enter Valid Phone Number")
            return
        if self.emailValidation == None:
            messagebox.showerror("Error", "Please Enter Valid Email Address")
            return
        if self.var1.get() == "Select":
            messagebox.showerror("Error", "Select DOB")
            return
        userDetails = {
            "name": self.nameInput.get(),
            "email": self.emailInput.get(),
            "password": bcrypt.hashpw(
                bytes(self.passwordInput.get(), "utf-8"), bcrypt.gensalt()
            ),
            "dob": self.var1.get(),
            "gender": "Male" if self.genderVar.get() == 1 else "Female",
            "phonenumber": self.numberInput.get(),
            "bookedSeats": [],
        }
        key = profileCollection.find_one({"email": userDetails["email"]})
        if key == None:
            profileCollection.insert_one(userDetails)
            messagebox.showinfo("Information", "Registred Successfully")
        else:
            messagebox.showinfo("Information", "Email Already Registered")
        self.registerPage.destroy()
        self.siginpage = SignIn(self.parent)

    def __init__(self, parent):
        self.parent = parent
        self.registerPage = Frame(
            self.parent,
            bg="#0f0e17",
            padx=100,
            pady=100,
        )
        self.registerPage.grid(row=0, column=0)
        # Name
        self.nameLabel = Label(
            self.registerPage,
            text="Name",
            bg="#0f0e17",
            fg="#fff",
            padx=10,
        )
        self.nameLabel.grid(row=0, column=0)
        self.nameInput = Entry(self.registerPage)
        self.nameInput.grid(row=0, column=1, pady=5)
        # Email
        self.emailLabel = Label(
            self.registerPage, text="Email", bg="#0f0e17", fg="#fff"
        )
        self.emailLabel.grid(row=1, column=0)
        self.emailInput = Entry(self.registerPage)
        self.emailInput.grid(row=1, column=1)
        # Password
        self.passwordLabel = Label(
            self.registerPage, text="Password", bg="#0f0e17", padx=10, fg="#fff"
        )
        self.passwordLabel.grid(row=2, column=0)
        self.passwordInput = Entry(self.registerPage, show="*")
        self.passwordInput.grid(row=2, column=1, pady=5)
        # DOB
        self.var1 = StringVar()
        self.var1.set("Select")
        self.DOBLabel = Label(
            self.registerPage, text="DOB", bg="#0f0e17", padx=10, fg="#fff"
        )
        self.DOBLabel.grid(row=3, column=0)
        self.DOBInput = Button(
            self.registerPage,
            text=self.var1.get(),
            bg="#ff8906",
            fg="#fffffe",
            command=self.datePicker,
        )
        self.DOBInput.grid(row=3, column=1, pady=5)
        # Gender
        self.genderLabel = Label(
            self.registerPage, text="Gender", bg="#0f0e17", padx=10, fg="#fff"
        )
        self.genderLabel.grid(column=0, row=4, pady=10)
        self.genderVar = IntVar()
        self.maleButton = Radiobutton(
            self.registerPage,
            text="Male",
            variable=self.genderVar,
            value=1,
        )
        self.femaleButton = Radiobutton(
            self.registerPage,
            text="Female",
            variable=self.genderVar,
            value=2,
        )
        self.maleButton.grid(row=4, column=1, pady=10)
        self.femaleButton.grid(row=4, column=2, pady=10)
        # Phone Number
        self.numberLabel = Label(
            self.registerPage, text="Phone Number", bg="#0f0e17", padx=10, fg="#fff"
        )
        self.numberLabel.grid(column=0, row=5)
        self.numberInput = Entry(self.registerPage)
        self.numberInput.grid(row=5, column=1)
        # Register Button
        self.registerButton = Button(
            self.registerPage,
            text="Register",
            activebackground="#f25f4c",
            activeforeground="#fffffe",
            bg="#ff8906",
            fg="#fff",
            relief=RAISED,
            bd=4,
            command=self.registerUser,
        )
        self.registerButton.grid(row=6, column=1, pady=20)
        # Back Button
        self.back = Button(
            self.registerPage,
            text="Back",
            # activebackground="#403835",
            activebackground="#e53170",
            activeforeground="#fff",
            bg="#f25f4c",
            fg="#fff",
            relief=RAISED,
            bd=4,
            command=self.goBack,
        )
        self.back.grid(row=6, column=2, pady=20)


# Index page
class IndexPage:
    def __init__(self, parent):
        self.parent = parent
        # self.index = Frame(self.parent, bg="#38447C")
        self.index = Frame(self.parent, bg="#232946")
        Label(self.index, image=IndexPageImage).grid(
            row=0, column=0, padx=10, pady=10, columnspan=2
        )
        self.register = Button(
            self.index,
            text="Register",
            activebackground="#31449E",
            activeforeground="#fff",
            bg="#d34745",
            fg="#fff",
            relief=RAISED,
            bd=4,
            padx=7,
            pady=3,
            command=self.directToRegister,
        )
        self.register.grid(row=1, column=0, pady=10)
        self.signIn = Button(
            self.index,
            text="Sign In",
            activebackground="#31449E",
            activeforeground="#fff",
            bg="#d34745",
            fg="#fff",
            relief=RAISED,
            bd=4,
            command=self.directToSignIn,
            padx=7,
            pady=3,
        )
        self.signIn.grid(row=1, column=1, pady=10)
        self.index.grid(row=0, column=0)

    def directToSignIn(self):
        self.index.destroy()
        self.page = SignIn(self.parent)

    def directToRegister(self):
        self.index.destroy()
        self.page = Register(self.parent)


# Container for all Frames
class Container:
    def __init__(self, parent):
        self.parent = parent
        self.indexObject = IndexPage(self.parent)


Home.title("Airline Ticket Reservation Sytem")
container = Container(Home)
Home.mainloop()
# dt = datetime.datetime(2020, 11, 5, 0, 20)
# a = pytz.timezone("Australia/Melbourne")
# print(a.localize(dt))
# utc = pytz.timezone("UTC")
# print(utc.normalize(a.localize(dt)))

# py = datetime.datetime(2020, 11, 4, 13, 20)
# py = py.replace(tzinfo=tz.gettz("UTC"))
# print(py.astimezone(tz.tzlocal()))
