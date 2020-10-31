from tkinter import *
import pymongo

mongoDB = pymongo.MongoClient(
    "mongodb+srv://Eyuwankg:eyuwankg@mern.kvhji.mongodb.net/mern?retryWrites=true&w=majority"
)
db = mongoDB["mern"]
tasks = db["tasks"]


class Home:
    def __init__(self, parent):
        self.root = parent
        self.homeFrame = Frame(self.root)
        self.homeFrame.grid(row=0, column=0)
        self.inputLabel = Label(self.homeFrame, text="Enter Your Task")
        self.inputLabel.grid(row=0, column=0)
        self.input = Entry(self.homeFrame)
        self.input.grid(row=0, column=1)
        self.add = Button(self.homeFrame, text="Add", command=self.addTask)
        self.add.grid(row=0, column=3)
        self.displayTasks()

    def displayTasks(self):
        self.conatinerFrame = Frame(self.homeFrame)
        for (index, task) in enumerate(tasks.find()):
            self.taskSelf = task
            self.taskFrame = Frame(self.conatinerFrame)
            self.taskLabel = Label(self.taskFrame, text=str(task["task"]))

            self.deleteButton = Button(
                self.taskFrame,
                text="delete",
                command=lambda: self.deleteTask(self.taskSelf["_id"]),
            )
            self.taskLabel.grid(row=0, column=0)
            self.deleteButton.grid(row=0, column=3)
            self.taskFrame.grid(row=index, column=0)
        self.conatinerFrame.grid(row=1, column=0)

    def addTask(self):
        tasks.insert_one({"task": self.input.get()})
        self.input.delete(0, END)
        self.conatinerFrame.grid_forget()
        self.displayTasks()

    def deleteTask(self, id):
        tasks.delete_one({"_id": id})
        self.conatinerFrame.grid_forget()
        self.displayTasks()


class TKinter:
    def __init__(self, parent):
        self.home = Home(parent)


root = Tk()
root.title("Airline Reservation System")
app = TKinter(root)
root.mainloop()
