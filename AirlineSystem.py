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
    def __init__(self, parent):
        self.parent = parent
        self.searchPage = Frame(self.parent, bg="#51575A", padx=100, pady=100)
        self.flightData = flightCollection.find()
        self.searchPage.grid(row=0, column=0)
        for flight in self.flightData:
            print(flight["date"])


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
            bg="#31449E",
            fg="#fff",
            relief=RAISED,
            bd=4,
            command=self.siginUser,
        )
        self.signInButton.grid(row=2, column=1, columnspan=1, pady=20)
        self.signInPage.grid(row=0, column=0)


# email password name dob nationality gender
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
        self.registerPage = Frame(self.parent, bg="#51575A", padx=100, pady=100)
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
            bg="#E7D5B5",
            fg="#000",
            relief=RAISED,
            bd=4,
            padx=20,
            pady=5,
            command=self.registerUser,
        )
        self.registerButton.grid(row=6, column=1, pady=20)
        #Back Button
        


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
