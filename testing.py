from tkinter import *
from string import ascii_uppercase
import datetime

data = {
    "departure": {
        "airport": "Shenzhen",
        "timezone": "Asia/Shanghai",
        "terminal": "T3",
        "iata": "SZX",
        "departureUTCTime": [2020, 11, 11, 12, 0],
        "gate": None,
    },
    "arrival": {
        "airport": "Fenghuang International (Phoenix International)",
        "timezone": "Asia/Shanghai",
        "terminal": "T2",
        "iata": "SYX",
        "arrivalUTCTime": [2020, 11, 11, 13, 45],
        "gate": None,
    },
    "travelTime": {"hours": 1, "minutes": 45},
    "airlineName": "Juneyao Airlines",
    "flightNumber": "5131",
    "seatsGraph": [
        [0, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [0, 1, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1],
        [1, 0, 0, 1, 1, 1],
        [0, 1, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 1, 1, 1, 0, 1],
        [0, 0, 1, 1, 1, 1],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0],
        [1, 1, 0, 1, 1, 1],
        [0, 0, 1, 1, 1, 0],
        [1, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 0, 1],
        [0, 1, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0],
    ],
}

bookedSeats = [
    {"row": "H", "column": 4},
    {"row": "I", "column": 4},
    {"row": "I", "column": 5},
    {"row": "I", "column": 3},
    {"row": "I", "column": 2},
    {"row": "H", "column": 2},
    {"row": "H", "column": 1},
    {"row": "H", "column": 0},
    {"row": "I", "column": 0},
    {"row": "J", "column": 0},
]

user = {
    "name": "python",
    "email": "python@gmail.com",
    "password": b"$2b$12$HFhrVice.ZGx2vBohPmwROR0du7lgvbSHwBHIq1krdYgUSireQ2/i",
    "dob": "4/14/20",
    "gender": "Male",
    "phonenumber": "12345789575",
}


class fluck:
    def __init__(self, data, deptTime, arrTime, cost):
        self.app = Tk()
        self.app.geometry("450x400")
        self.canvasTwo = Canvas(self.app, width=450, bg="#8ecae6")
        self.scrollBarTwo = Scrollbar(
            self.app, orient=VERTICAL, command=self.canvasTwo.yview
        )
        self.confirmBookingFrame = Frame(
            self.canvasTwo, padx=10, width=380, bg="#8ecae6"
        )
        self.canvasTwo.create_window(
            (0, 0), window=self.confirmBookingFrame, anchor="nw"
        )
        self.confirmBookingFrame.configure(bg="#232946")
        # self.confirmBookingFrame.pack(fill=BOTH, expand=1, side=LEFT)
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
            text="Confirm Your Bookings",
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
            text=deptTime,
            bg="#232946",
            fg="#fffffe",
            wraplength=150,
        )
        self.confirmDepartureTime.grid(row=6, column=1, padx=40, pady=20)
        # DepartureTime-----------------------------
        self.scrollBarTwo.pack(side=RIGHT, fill=Y)
        self.canvasTwo.pack(fill=BOTH, expand=1, side=LEFT)
        self.canvasTwo.configure(yscrollcommand=self.scrollBarTwo.set)
        self.canvasTwo.bind(
            "<Configure>",
            lambda e: self.canvasTwo.configure(scrollregion=self.canvasTwo.bbox("all")),
        )
        self.app.mainloop()


f = fluck(data, "2020/11/10 21:35:00", "2020/11/11 13:55:00", 23424)
