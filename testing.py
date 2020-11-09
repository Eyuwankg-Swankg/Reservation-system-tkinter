from tkinter import *
from string import ascii_uppercase
import datetime

data = {
    "departure": {
        "airport": "Tianjin Binhai International",
        "timezone": "Asia/Shanghai",
        "terminal": None,
        "iata": "TSN",
        "departureUTCTime": [2020, 11, 8, 18, 50],
        "gate": None,
    },
    "arrival": {
        "airport": "Wuxi",
        "timezone": "Asia/Shanghai",
        "terminal": "T2",
        "iata": "WUX",
        "arrivalUTCTime": [2020, 11, 8, 20, 30],
        "gate": None,
    },
    "travelTime": {"hours": 1, "minutes": 40},
    "airlineName": "Longhao Airlines",
    "flightNumber": "4028",
}
app = Tk()
app.geometry("450x400")
canvasOne = Canvas(app, width=450, bg="#8ecae6")
scrollBarOne = Scrollbar(app, orient=VERTICAL, command=canvasOne.yview)
containerFrameOne = Frame(canvasOne, padx=10, width=380, bg="#8ecae6")
canvasOne.create_window((0, 0), window=containerFrameOne, anchor="nw")
scrollBarOne.pack(side=RIGHT, fill=Y)
canvasOne.pack(fill=BOTH, expand=1, side=LEFT)
canvasOne.configure(yscrollcommand=scrollBarOne.set)
canvasOne.bind(
    "<Configure>",
    lambda e: canvasOne.configure(scrollregion=canvasOne.bbox("all")),
)
# row0---------------------------------------------------
emptySpaceOne1 = Label(containerFrameOne, text="", width=15, bg="#8ecae6")
emptySpaceOne1.grid(row=0, column=0)
departureLabelOne = Label(containerFrameOne, text="Departure", width=20, bg="#8ecae6")
departureLabelOne.grid(row=0, column=1, pady=20)
arrivalLabelOne = Label(containerFrameOne, text="Arrival", width=20, bg="#8ecae6")
arrivalLabelOne.grid(row=0, column=2)
# row0---------------------------------------------------
# row1---------------------------------------------------
airportOne = Label(containerFrameOne, text="Airport", width=18, bg="#8ecae6")
airportOne.grid(row=1, column=0)
aiportDepartureOne = Label(
    containerFrameOne,
    text=data["departure"]["airport"],
    width=20,
    height=4,
    wraplength=100,
    bg="#8ecae6",
)
aiportDepartureOne.grid(row=1, column=1, pady=7)
airportArrivalOne = Label(
    containerFrameOne,
    text=data["arrival"]["airport"],
    width=20,
    bg="#8ecae6",
    height=4,
    wraplength=100,
)
airportArrivalOne.grid(row=1, column=2)
# row1---------------------------------------------------
# row2---------------------------------------------------
airportCodeOne = Label(containerFrameOne, text="Airport Code", width=18, bg="#8ecae6")
airportCodeOne.grid(row=2, column=0)
airportCodeDepartureOne = Label(
    containerFrameOne,
    text=data["departure"]["iata"],
    width=20,
    height=4,
    wraplength=100,
    bg="#8ecae6",
)
airportCodeDepartureOne.grid(row=2, column=1, pady=7)
airportCodeArrivalOne = Label(
    containerFrameOne,
    text=data["arrival"]["iata"],
    width=20,
    bg="#8ecae6",
    wraplength=100,
)
airportCodeArrivalOne.grid(row=2, column=2)
# row2---------------------------------------------------

# row3---------------------------------------------------
cityOne = Label(containerFrameOne, text="City", width=18, bg="#8ecae6")
cityOne.grid(row=3, column=0)
cityDepartureOne = Label(
    containerFrameOne,
    text=data["departure"]["timezone"],
    width=20,
    height=4,
    wraplength=100,
    bg="#8ecae6",
)
cityDepartureOne.grid(row=3, column=1, pady=7)
cityArrivalOne = Label(
    containerFrameOne,
    text=data["arrival"]["timezone"],
    width=20,
    bg="#8ecae6",
    wraplength=100,
)
cityArrivalOne.grid(row=3, column=2)
# row3---------------------------------------------------
# row4---------------------------------------------------
terminalOne = Label(containerFrameOne, text="Terminal", width=18, bg="#8ecae6")
terminalOne.grid(row=4, column=0)
terminalDepartureOne = Label(
    containerFrameOne,
    text=data["departure"]["terminal"],
    width=20,
    height=4,
    wraplength=100,
    bg="#8ecae6",
)
terminalDepartureOne.grid(row=4, column=1, pady=7)
terminalArrivalOne = Label(
    containerFrameOne,
    text=data["arrival"]["terminal"],
    width=20,
    bg="#8ecae6",
    wraplength=100,
)
terminalArrivalOne.grid(row=4, column=2)
# row4---------------------------------------------------
# row5---------------------------------------------------
conArrTime = datetime.datetime(*data["arrival"]["arrivalUTCTime"])
conDeptTime = datetime.datetime(*data["departure"]["departureUTCTime"])
timeOne = Label(containerFrameOne, text="Time", width=18, bg="#8ecae6")
timeOne.grid(row=5, column=0)
timeDepartureOne = Label(
    containerFrameOne,
    text=conDeptTime.strftime("%d/%m/%Y  %H:%M:%S"),
    width=20,
    height=4,
    wraplength=100,
    bg="#8ecae6",
)
timeDepartureOne.grid(row=5, column=1, pady=7)
timeArrivalOne = Label(
    containerFrameOne,
    text=conArrTime.strftime("%d/%m/%Y  %H:%M:%S"),
    width=20,
    bg="#8ecae6",
    wraplength=100,
)
timeArrivalOne.grid(row=5, column=2)
# row5---------------------------------------------------
# row6---------------------------------------------------
gateOne = Label(containerFrameOne, text="Gate", width=18, bg="#8ecae6")
gateOne.grid(row=6, column=0)
gateDepartureOne = Label(
    containerFrameOne,
    text=data["departure"]["gate"],
    width=20,
    height=4,
    wraplength=100,
    bg="#8ecae6",
)
gateDepartureOne.grid(row=6, column=1, pady=7)
gateArrivalOne = Label(
    containerFrameOne,
    text=data["arrival"]["gate"],
    width=20,
    bg="#8ecae6",
    wraplength=100,
)
gateArrivalOne.grid(row=6, column=2)
# row6---------------------------------------------------
# row7---------------------------------------------------
travelTimeLabelOne = Label(
    containerFrameOne,
    text="Travel Time",
    width=18,
    bg="#8ecae6",
)
travelTimeLabelOne.grid(row=7, column=0)
travelTimeOne = Label(
    containerFrameOne,
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
airlineLabelOne = Label(containerFrameOne, text="Airline", width=18, bg="#8ecae6")
airlineLabelOne.grid(row=8, column=0)
airlineOne = Label(
    containerFrameOne,
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
    containerFrameOne, text="Flight Number", width=18, bg="#8ecae6"
)
flightNumberLabelOne.grid(row=9, column=0)
flightNumberOne = Label(
    containerFrameOne,
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
    containerFrameOne,
    text="Select your Seat",
    bg="#8ecae6",
    font="Halevtia 12 bold",
)
selectSeatLabel.grid(row=10, column=0, columnspan=3, pady=10)
# row10--------------------------------------------------
# row11--------------------------------------------------
# display all the seats----------------------------------
seatWidth = 2
padYAxis = 7
padXAxis = 6
backgroundSeat = "#f9bc60"
seatLayoutContainer = Frame(containerFrameOne, bg="#004643")
for (index, char) in enumerate(ascii_uppercase):
    seatZero = Button(seatLayoutContainer, text="0", width=seatWidth, bg=backgroundSeat)
    seatZero.grid(row=index, column=0, pady=padYAxis, padx=padXAxis)
    seatOne = Button(seatLayoutContainer, text="1", width=seatWidth, bg=backgroundSeat)
    seatOne.grid(row=index, column=1, pady=padYAxis, padx=padXAxis)
    seatTwo = Button(seatLayoutContainer, text="2", width=seatWidth, bg=backgroundSeat)
    seatTwo.grid(row=index, column=2, pady=padYAxis, padx=padXAxis)
    seatIdLabel = Label(seatLayoutContainer, text=char, fg="#fff", bg="#004643")
    seatIdLabel.grid(row=index, column=3, pady=padYAxis, padx=padXAxis)
    seatThree = Button(
        seatLayoutContainer, text="3", width=seatWidth, bg=backgroundSeat
    )
    seatThree.grid(row=index, column=4, pady=padYAxis, padx=padXAxis)
    seatFour = Button(seatLayoutContainer, text="4", width=seatWidth, bg=backgroundSeat)
    seatFour.grid(row=index, column=5, pady=padYAxis, padx=padXAxis)
    seatFive = Button(seatLayoutContainer, text="5", width=seatWidth, bg=backgroundSeat)
    seatFive.grid(row=index, column=6, pady=padYAxis, padx=padXAxis)
seatLayoutContainer.grid(row=11, column=0, columnspan=4, pady=10)
# row11--------------------------------------------------
app.mainloop()
