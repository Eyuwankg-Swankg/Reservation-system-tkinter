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
import keyring

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

# Search Page
class SearchPage:
    allFlights = {}
    date = []
    departure = set()
    arrival = set()

    def finishBooking(self):
        messagebox.showinfo(
            "Success",
            "Booking Confirmed , Check {0} for Ticket".format(self.emailInput.get()),
        )

    def confirmBooking(self, data, deptTime, arrTime, cost):
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
            command=self.finishBooking,
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

    def showFlightInfo(self, data, deptTime, arrTime, cost):
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
            command=lambda d=data, dT=deptTime, aT=arrTime, c=cost: self.confirmBooking(
                d, dT, aT, c
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
                    self.totalCost,
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
        self.flightData = flightCollection.find()
        self.searchPage.pack(fill=BOTH, expand=1)
        for flight in self.flightData:
            self.allFlights[flight["date"]] = flight["data"]
            self.date.append(flight["date"])
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
