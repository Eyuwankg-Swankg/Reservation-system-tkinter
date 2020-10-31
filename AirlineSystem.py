from tkinter import *
from PIL import ImageTk, Image, ImageFile
import pymongo

ImageFile.LOAD_TRUNCATED_IMAGES = True

# intialize DB
mongoDB = pymongo.MongoClient(
    "mongodb+srv://Eyuwankg:eyuwankg@mern.kvhji.mongodb.net/OOAD?retryWrites=true&w=majority"
)
db = mongoDB["OOAD"]
profiles = db["profiles"]
# Intialize Home Page for all Frames
Home = Tk()
IndexPageImage = ImageTk.PhotoImage(Image.open("./HomePage.jpg"))


# SignIn
class SignIn:
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

        # Signin
        self.signInButton = Button(
            self.signInPage,
            text="Sign In",
            activebackground="#d34745",
            activeforeground="#fff",
            bg="#31449E",
            fg="#fff",
            relief=RAISED,
            bd=4,
        )
        self.signInButton.grid(row=2, column=1, columnspan=1, pady=20)
        self.signInPage.grid(row=0, column=0)


# email password name dob nationality gender
# Register
class Register:
    def __init__(self, parent):
        self.parent = parent
        self.registerPage = Frame(self.parent, bg="blue")
        self.registerPage.grid(row=0, column=0)


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