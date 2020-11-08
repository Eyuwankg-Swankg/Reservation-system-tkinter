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

    def displayFlights(self):
        if self.intVar.get() == 0:
            self.scrollFrame.destroy()
        self.scrollFrame = Frame(self.searchPage, width=500)
        self.intVar.set(0)
        self.canvas = Canvas(self.scrollFrame, width=500)
        self.scrollBar = Scrollbar(
            self.scrollFrame, orient=VERTICAL, command=self.canvas.yview
        )
        self.containerFrame = Frame(self.canvas, padx=10, width=400)
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
                self.selectedDate.get()
                != self.convertDepartureTime.strftime("%Y-%m-%d")
                or (self.departureSelected.get() != flightData["departure"]["timezone"])
                or (self.arrivalSelected.get() != flightData["arrival"]["timezone"])
            ):
                continue
            self.flightDisplayFrame = Frame(
                self.containerFrame, bg="#B9BFC7", padx=20, pady=10, width=210
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
                wraplength=150,
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
                wraplength=150,
            )
            self.timezoneArrival.grid(row=2, column=2, pady=10)
            # row2 ----------------------------------------

            # row3 ----------------------------------------
            # time Departure
            self.departureTime = Label(
                self.flightDisplayFrame,
                text=self.convertDepartureTime.astimezone(tz.tzlocal()).strftime(
                    "%H : %M : %S"
                ),
                bg="#B9BFC7",
                font="Helvetica 8 bold",
                wraplength=150,
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
                text=self.convertArrivalTime.astimezone(tz.tzlocal()).strftime(
                    "%H : %M : %S"
                ),
                bg="#B9BFC7",
                font="Helvetica 8 bold",
                wraplength=150,
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

            self.flightDisplayFrame.pack(fill=BOTH, pady=10)
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

    def __init__(self, parent):
        self.parent = parent
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
        self.search = SearchPage(self.parent)

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
