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

ImageFile.LOAD_TRUNCATED_IMAGES = True

# intialize DB
mongoDB = pymongo.MongoClient(
    "mongodb+srv://Eyuwankg:eyuwankg@mern.kvhji.mongodb.net/OOAD?retryWrites=true&w=majority"
)
db = mongoDB["OOAD"]
profileCollection = db["profiles"]
flightCollection = db["flights"]

# Intialize Home Page for all Frames
Home = Tk()
IndexPageImage = ImageTk.PhotoImage(Image.open("./HomePage.jpg"))

# Search Page
class SearchPage:
    allFlights = {}
    date = []
    departure = set()
    arrival = set()

    def confirmBooking(self, data, deptTime, arrTime, cost):
        try:
            if self.app:
                self.app.destroy()
        except:
            pass
        print(
            data,
            deptTime.strftime("%Y/%m/%d %H:%M:%S"),
            arrTime.strftime("%Y/%m/%d %H:%M:%S"),
            cost,
            self.bookedSeats,
            self.user,
            sep="\n",
        )
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
            command=lambda d=data, dT=deptTime, aT=arrTime, c=cost: self.showFlightInfo(
                d, dT, aT, c
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
        self.userEmailVar = StringVar()
        self.userEmailVar.set(self.user["email"])
        self.emailLabel = Label(
            self.confirmBookingFrame,
            text="Email : ",
            bg="#232946",
            fg="#fffffe",
        )
        self.emailLabel.grid(row=7, column=0)
        self.emailInput = Entry(
            self.confirmBookingFrame, textvariable=self.userEmailVar
        )
        self.emailInput.grid(row=7, column=1, padx=40, pady=30)
        # Show Email--------------------------------
        # Get Name and age of all seats-------------
        self.containerFrameForSeatEntry = Frame(
            self.confirmBookingFrame, padx=10, width=410, pady=20
        )
        self.containerFrameForSeatEntry.config(bg="#eebbc3")
        self.infoOfBookedSeats = []
        for (index, seat) in enumerate(self.bookedSeats):
            self.infoOfBookedSeats.append([StringVar(), IntVar()])
            self.infoOfBookedSeats[index][0].set("Enter Name")
            self.infoOfBookedSeats[index][1].set("Enter Age")
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
            self.seatNameEntry = Entry(
                self.containerFrameForSeatEntry,
                textvariable=self.infoOfBookedSeats[index][0],
                justify=CENTER,
                relief=RIDGE,
            )
            self.seatNameEntry.grid(row=index, column=1)
            Label(
                self.containerFrameForSeatEntry,
                text="    ",
                bg="#eebbc3",
            ).grid(row=index, column=2, padx=20, pady=10)
            self.seatAgeEntry = Entry(
                self.containerFrameForSeatEntry,
                textvariable=self.infoOfBookedSeats[index][1],
                justify=CENTER,
                relief=RIDGE,
            )
            self.seatAgeEntry.grid(row=index, column=3)

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
        self.phoneNumberVar = IntVar()
        self.phoneNumberInput = Entry(
            self.confirmBookingFrame, textvariable=self.phoneNumberVar
        )
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
        backgroundSeat = "#f9bc60"
        selectedSeat = "#abd1c6"
        self.seatLayoutContainer = Frame(self.containerFrameOne, bg="#004643")
        for (index, char) in enumerate(ascii_uppercase):
            self.seatZero = Button(
                self.seatLayoutContainer,
                text="0",
                width=seatWidth,
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
                bg=selectedSeat
                if {"row": char, "column": 2} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][2] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][2] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 2),
            )
            self.seatTwo.grid(row=index, column=2, pady=padYAxis, padx=padXAxis)
            seatIdLabel = Label(
                self.seatLayoutContainer, text=char, fg="#fff", bg="#004643"
            )
            seatIdLabel.grid(row=index, column=3, pady=padYAxis, padx=padXAxis)
            self.seatThree = Button(
                self.seatLayoutContainer,
                text="3",
                width=seatWidth,
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
                bg=selectedSeat
                if {"row": char, "column": 5} in self.bookedSeats
                else (backgroundSeat if data["seatsGraph"][index][5] else "#e16162"),
                state=NORMAL if data["seatsGraph"][index][5] else DISABLED,
                command=lambda d=data, i=index: self.updateSeatBookings(data, i, 5),
            )
            self.seatFive.grid(row=index, column=6, pady=padYAxis, padx=padXAxis)
            self.seatLayoutContainer.grid(row=11, column=0, columnspan=4, pady=10)
        # row11--------------------------------------------------

    def showFlightInfo(self, data, deptTime, arrTime, cost):
        try:
            if self.app:
                self.app.destroy()
        except:
            pass
        self.app = Tk()
        self.app.geometry("450x400")
        self.bookedSeats = []
        self.canvasOne = Canvas(self.app, width=450, bg="#8ecae6")
        self.scrollBarOne = Scrollbar(
            self.app, orient=VERTICAL, command=self.canvasOne.yview
        )
        self.containerFrameOne = Frame(self.canvasOne, padx=10, width=380, bg="#8ecae6")
        self.canvasOne.create_window((0, 0), window=self.containerFrameOne, anchor="nw")
        self.scrollBarOne.pack(side=RIGHT, fill=Y)
        self.canvasOne.pack(fill=BOTH, expand=1, side=LEFT)
        self.canvasOne.configure(yscrollcommand=self.scrollBarOne.set)
        self.canvasOne.bind(
            "<Configure>",
            lambda e: self.canvasOne.configure(scrollregion=self.canvasOne.bbox("all")),
        )
        # row0---------------------------------------------------
        emptySpaceOne1 = Label(self.containerFrameOne, text="", width=15, bg="#8ecae6")
        emptySpaceOne1.grid(row=0, column=0)
        departureLabelOne = Label(
            self.containerFrameOne, text="Departure", width=20, bg="#8ecae6"
        )
        departureLabelOne.grid(row=0, column=1, pady=20)
        arrivalLabelOne = Label(
            self.containerFrameOne, text="Arrival", width=20, bg="#8ecae6"
        )
        arrivalLabelOne.grid(row=0, column=2)
        # row0---------------------------------------------------
        # row1---------------------------------------------------
        airportOne = Label(
            self.containerFrameOne, text="Airport", width=18, bg="#8ecae6"
        )
        airportOne.grid(row=1, column=0)
        aiportDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["airport"],
            width=20,
            height=4,
            wraplength=100,
            bg="#8ecae6",
        )
        aiportDepartureOne.grid(row=1, column=1, pady=7)
        airportArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["airport"],
            width=20,
            bg="#8ecae6",
            height=4,
            wraplength=100,
        )
        airportArrivalOne.grid(row=1, column=2)
        # row1---------------------------------------------------
        # row2---------------------------------------------------
        airportCodeOne = Label(
            self.containerFrameOne, text="Airport Code", width=18, bg="#8ecae6"
        )
        airportCodeOne.grid(row=2, column=0)
        airportCodeDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["iata"],
            width=20,
            height=4,
            wraplength=100,
            bg="#8ecae6",
        )
        airportCodeDepartureOne.grid(row=2, column=1, pady=7)
        airportCodeArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["iata"],
            width=20,
            bg="#8ecae6",
            wraplength=100,
        )
        airportCodeArrivalOne.grid(row=2, column=2)
        # row2---------------------------------------------------

        # row3---------------------------------------------------
        cityOne = Label(self.containerFrameOne, text="City", width=18, bg="#8ecae6")
        cityOne.grid(row=3, column=0)
        cityDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["timezone"],
            width=20,
            height=4,
            wraplength=100,
            bg="#8ecae6",
        )
        cityDepartureOne.grid(row=3, column=1, pady=7)
        cityArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["timezone"],
            width=20,
            bg="#8ecae6",
            wraplength=100,
        )
        cityArrivalOne.grid(row=3, column=2)
        # row3---------------------------------------------------
        # row4---------------------------------------------------
        terminalOne = Label(
            self.containerFrameOne, text="Terminal", width=18, bg="#8ecae6"
        )
        terminalOne.grid(row=4, column=0)
        terminalDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["terminal"],
            width=20,
            height=4,
            wraplength=100,
            bg="#8ecae6",
        )
        terminalDepartureOne.grid(row=4, column=1, pady=7)
        terminalArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["terminal"],
            width=20,
            bg="#8ecae6",
            wraplength=100,
        )
        terminalArrivalOne.grid(row=4, column=2)
        # row4---------------------------------------------------
        # row5---------------------------------------------------
        timeOne = Label(self.containerFrameOne, text="Time", width=18, bg="#8ecae6")
        timeOne.grid(row=5, column=0)
        timeDepartureOne = Label(
            self.containerFrameOne,
            text=deptTime.strftime("%d/%m/%Y  %H:%M:%S"),
            width=20,
            height=4,
            wraplength=100,
            bg="#8ecae6",
        )
        timeDepartureOne.grid(row=5, column=1, pady=7)
        timeArrivalOne = Label(
            self.containerFrameOne,
            text=arrTime.strftime("%d/%m/%Y  %H:%M:%S"),
            width=20,
            bg="#8ecae6",
            wraplength=100,
        )
        timeArrivalOne.grid(row=5, column=2)
        # row5---------------------------------------------------
        # row6---------------------------------------------------
        gateOne = Label(self.containerFrameOne, text="Gate", width=18, bg="#8ecae6")
        gateOne.grid(row=6, column=0)
        gateDepartureOne = Label(
            self.containerFrameOne,
            text=data["departure"]["gate"],
            width=20,
            height=4,
            wraplength=100,
            bg="#8ecae6",
        )
        gateDepartureOne.grid(row=6, column=1, pady=7)
        gateArrivalOne = Label(
            self.containerFrameOne,
            text=data["arrival"]["gate"],
            width=20,
            bg="#8ecae6",
            wraplength=100,
        )
        gateArrivalOne.grid(row=6, column=2)
        # row6---------------------------------------------------
        # row7---------------------------------------------------
        travelTimeLabelOne = Label(
            self.containerFrameOne,
            text="Travel Time",
            width=18,
            bg="#8ecae6",
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
            bg="#8ecae6",
        )
        travelTimeOne.grid(row=7, column=1, pady=7, columnspan=2)
        # row7---------------------------------------------------
        # row8---------------------------------------------------
        airlineLabelOne = Label(
            self.containerFrameOne, text="Airline", width=18, bg="#8ecae6"
        )
        airlineLabelOne.grid(row=8, column=0)
        airlineOne = Label(
            self.containerFrameOne,
            text=data["airlineName"],
            width=20,
            height=4,
            font="Halevtia 12",
            wraplength=100,
            bg="#8ecae6",
        )
        airlineOne.grid(row=8, column=1, pady=7, columnspan=2)
        # row8---------------------------------------------------
        # row9---------------------------------------------------
        flightNumberLabelOne = Label(
            self.containerFrameOne, text="Flight Number", width=18, bg="#8ecae6"
        )
        flightNumberLabelOne.grid(row=9, column=0)
        flightNumberOne = Label(
            self.containerFrameOne,
            text=data["flightNumber"],
            width=20,
            height=4,
            font="Halevtia 12",
            wraplength=100,
            bg="#8ecae6",
        )
        flightNumberOne.grid(row=9, column=1, pady=7, columnspan=2)
        # row9---------------------------------------------------
        # row10--------------------------------------------------
        selectSeatLabel = Label(
            self.containerFrameOne,
            text="Select your Seat",
            bg="#8ecae6",
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
            command=lambda d=data, dT=deptTime, aT=arrTime, c=cost: self.confirmBooking(
                d, dT, aT, c
            ),
        )
        self.bookTickets.grid(row=12, column=0, columnspan=3, rowspan=2, pady=20)
        self.app.mainloop()

    def displayFlights(self):
        if self.intVar.get() == 0:
            self.scrollFrame.destroy()
        self.scrollFrame = Frame(self.searchPage, width=450)
        self.intVar.set(0)
        self.canvas = Canvas(self.scrollFrame, width=450)
        self.scrollBar = Scrollbar(
            self.scrollFrame, orient=VERTICAL, command=self.canvas.yview
        )
        self.containerFrame = Frame(self.canvas, padx=10, width=380)
        self.canvas.create_window((0, 0), window=self.containerFrame, anchor="nw")
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
            self.flightDisplayFrame = Frame(
                self.containerFrame,
                bg="#B9BFC7",
                padx=20,
                pady=10,
                width=210,
            )
            # row0 ----------------------------------------
            self.emptySpace1 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#B9BFC7",
            )
            self.emptySpace1.grid(row=0, column=0, pady=10)

            # airline Name
            self.airlineName = Label(
                self.flightDisplayFrame,
                text=flightData["airlineName"],
                font="Helvetica 12 bold",
                bg="#B9BFC7",
            )
            self.airlineName.grid(row=0, column=1, pady=10)

            self.emptySpace2 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#B9BFC7",
            )
            self.emptySpace2.grid(row=0, column=2, pady=10)
            # row0 ----------------------------------------
            # row1 ----------------------------------------
            # Airport Departure
            self.airportDeparture = Label(
                self.flightDisplayFrame,
                text=flightData["departure"]["airport"],
                bg="#B9BFC7",
                font="Helvetica 9 bold",
                wraplength=150,
            )
            self.airportDeparture.grid(row=1, column=0, pady=10)

            self.emptySpace3 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#B9BFC7",
            )
            self.emptySpace3.grid(row=1, column=1, pady=10)

            # Airport Arrival
            self.airportArrival = Label(
                self.flightDisplayFrame,
                text=flightData["arrival"]["airport"],
                bg="#B9BFC7",
                font="Helvetica 9 bold",
                wraplength=100,
            )
            self.airportArrival.grid(row=1, column=2, pady=10)
            # row1 ----------------------------------------

            # row2 ----------------------------------------
            # timezone Departure
            self.timezoneDeparture = Label(
                self.flightDisplayFrame,
                text=flightData["departure"]["timezone"],
                bg="#B9BFC7",
                font="Helvetica 8 bold",
                wraplength=150,
            )
            self.timezoneDeparture.grid(row=2, column=0, pady=10)

            self.emptySpace4 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#B9BFC7",
            )
            self.emptySpace4.grid(row=2, column=1, pady=10)

            # timezone Arrival
            self.timezoneArrival = Label(
                self.flightDisplayFrame,
                text=flightData["arrival"]["timezone"],
                bg="#B9BFC7",
                font="Helvetica 8 bold",
                wraplength=130,
            )
            self.timezoneArrival.grid(row=2, column=2, pady=10)
            # row2 ----------------------------------------

            # row3 ----------------------------------------
            # time Departure
            self.departureTime = Label(
                self.flightDisplayFrame,
                text=self.convertDepartureTime.strftime("%Y/%m/%d  %H:%M:%S"),
                bg="#B9BFC7",
                font="Helvetica 8 bold",
                wraplength=100,
            )
            self.departureTime.grid(row=3, column=0, pady=10)

            self.emptySpace5 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#B9BFC7",
            )
            self.emptySpace5.grid(row=3, column=1, pady=10)

            # time Arrival
            self.arrivalTime = Label(
                self.flightDisplayFrame,
                text=self.convertArrivalTime.strftime("%Y/%m/%d  %H:%M:%S"),
                bg="#B9BFC7",
                font="Helvetica 8 bold",
                wraplength=100,
            )
            self.arrivalTime.grid(row=3, column=2, pady=10)
            # row3 ----------------------------------------

            # row4 ----------------------------------------
            self.emptySpace6 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#B9BFC7",
            )
            self.tripCost = random.randint(20000, 35000)
            self.emptySpace6.grid(row=4, column=0, pady=10)
            self.totalCost = Label(
                self.flightDisplayFrame,
                text="Cost : " + str(self.tripCost),
                font="Helvetica 12 bold",
                bg="#B9BFC7",
            )
            self.emptySpace7 = Label(
                self.flightDisplayFrame,
                text="                                 ",
                bg="#B9BFC7",
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
                    self.totalCost,
                ),
            )
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
        self.searchPage = Frame(self.parent, bg="#51575A", padx=10, pady=10)
        self.flightData = flightCollection.find()
        self.searchPage.grid(row=0, column=0)
        for flight in self.flightData:
            self.allFlights[flight["date"]] = flight["data"]
            self.date.append(flight["date"])
        self.frameForPack = Frame(self.searchPage)
        # date list
        self.selectedDate = StringVar()
        self.selectedDate.set("Select Date")
        self.dateOption = OptionMenu(self.frameForPack, self.selectedDate, *self.date)
        self.dateOption.pack()
        self.getFromTo = Button(
            self.frameForPack,
            text="Get",
            activebackground="#d34745",
            activeforeground="#fff",
            bg="#333945",
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
        self.signInPage = Frame(self.parent, bg="#51575A", padx=100, pady=100)

        # Email
        self.emailLabel = Label(self.signInPage, text="Email", bg="#51575A", fg="#fff")
        self.emailLabel.grid(row=0, column=0)
        self.emailInput = Entry(self.signInPage)
        self.emailInput.grid(row=0, column=1)

        # Password
        self.passwordLabel = Label(
            self.signInPage, text="Password", bg="#51575A", padx=10, fg="#fff"
        )
        self.passwordLabel.grid(row=1, column=0)
        self.passwordInput = Entry(self.signInPage, show="*")
        self.passwordInput.grid(row=1, column=1, pady=5)

        # Signin Button
        self.signInButton = Button(
            self.signInPage,
            text="Sign In",
            activebackground="#d34745",
            activeforeground="#fff",
            bg="#333945",
            fg="#fff",
            relief=RAISED,
            bd=4,
            command=self.siginUser,
        )
        self.signInButton.grid(row=2, column=1, columnspan=1, pady=20)
        # Back Button
        self.back = Button(
            self.signInPage,
            text="Back",
            activebackground="#403835",
            activeforeground="#fff",
            bg="#4B1A23",
            fg="#fff",
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
            self.registerPage, text=self.var1.get(), command=self.datePicker
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
            bg="#51575A",
            padx=100,
            pady=100,
        )
        self.registerPage.grid(row=0, column=0)
        # Name
        self.nameLabel = Label(
            self.registerPage,
            text="Name",
            bg="#51575A",
            fg="#fff",
            padx=10,
        )
        self.nameLabel.grid(row=0, column=0)
        self.nameInput = Entry(self.registerPage)
        self.nameInput.grid(row=0, column=1, pady=5)
        # Email
        self.emailLabel = Label(
            self.registerPage, text="Email", bg="#51575A", fg="#fff"
        )
        self.emailLabel.grid(row=1, column=0)
        self.emailInput = Entry(self.registerPage)
        self.emailInput.grid(row=1, column=1)
        # Password
        self.passwordLabel = Label(
            self.registerPage, text="Password", bg="#51575A", padx=10, fg="#fff"
        )
        self.passwordLabel.grid(row=2, column=0)
        self.passwordInput = Entry(self.registerPage, show="*")
        self.passwordInput.grid(row=2, column=1, pady=5)
        # DOB
        self.var1 = StringVar()
        self.var1.set("Select")
        self.DOBLabel = Label(
            self.registerPage, text="DOB", bg="#51575A", padx=10, fg="#fff"
        )
        self.DOBLabel.grid(row=3, column=0)
        self.DOBInput = Button(
            self.registerPage, text=self.var1.get(), command=self.datePicker
        )
        self.DOBInput.grid(row=3, column=1, pady=5)
        # Gender
        self.genderLabel = Label(
            self.registerPage, text="Gender", bg="#51575A", padx=10, fg="#fff"
        )
        self.genderLabel.grid(column=0, row=4, pady=10)
        self.genderVar = IntVar()
        self.maleButton = Radiobutton(
            self.registerPage, text="Male", variable=self.genderVar, value=1
        )
        self.femaleButton = Radiobutton(
            self.registerPage, text="Female", variable=self.genderVar, value=2
        )
        self.maleButton.grid(row=4, column=1, pady=10)
        self.femaleButton.grid(row=4, column=2, pady=10)
        # Phone Number
        self.numberLabel = Label(
            self.registerPage, text="Phone Number", bg="#51575A", padx=10, fg="#fff"
        )
        self.numberLabel.grid(column=0, row=5)
        self.numberInput = Entry(self.registerPage)
        self.numberInput.grid(row=5, column=1)
        # Register Button
        self.registerButton = Button(
            self.registerPage,
            text="Register",
            activebackground="#403835",
            activeforeground="#fff",
            bg="#333945",
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
            activebackground="#403835",
            activeforeground="#fff",
            bg="#4B1A23",
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
        self.index = Frame(self.parent, bg="#38447C")
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
