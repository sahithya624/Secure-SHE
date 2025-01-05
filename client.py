import random
import customtkinter as tk
import modifyContacts
import sendLocationToAll
import location
import json
import logging

WIDTH = 400
HEIGHT = WIDTH
ID = "Test ID"
logging.basicConfig(filename='db\\log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('twilio').setLevel(logging.WARNING)


class Application:
    def __init__(self):
        self.root = tk.CTk()
        self.root.title("SecureSHE")
        self.root.geometry("840x840")

        self.locationBtn = tk.CTkButton(
            self.root, text="Share GEO Location", width=WIDTH, height=HEIGHT, command=self.sendMyLocation)
        self.addTrustedContacts = tk.CTkButton(
            self.root, text="Add Trusted Contacts", width=WIDTH, height=HEIGHT, command=self.addContacts)
        self.removeTrustedContacts = tk.CTkButton(
            self.root, text="Remove Trusted Contacts", width=WIDTH, height=HEIGHT, command=self.removeContacts)
        self.btn4 = tk.CTkButton(
            self.root, text="Btn 4", width=WIDTH, height=HEIGHT)

        self.locationBtn.grid(row=0, column=0, padx=10, pady=10)
        self.addTrustedContacts.grid(row=0, column=1, padx=10, pady=10)
        self.removeTrustedContacts.grid(row=1, column=0, padx=10, pady=10)
        self.btn4.grid(row=1, column=1, padx=10, pady=10)

        self.root.resizable(False, False)

    def sendMyLocation(self):
        loc = location.GetLocation()
        locationLink = loc.return_location()
        sendLocationToAll.sendLocation(locationLink)

        with open("db\\pending_requests.json") as f:
            data = json.load(f)
        with open("db\\vehicle_database.json") as f1:
            vehicle_data = json.load(f1)

        vehicle = random.choice(list(vehicle_data.keys()))
        data['pending'][ID] = vehicle
        
        vehicle_data[vehicle]['marked'] = True
        with open("db\\vehicle_database.json", "w") as f1:
            json.dump(vehicle_data, f1, indent=4)

        with open("db\\pending_requests.json", 'w') as f:
            json.dump(data, f, indent=4)

        logger.info(f"{ID} requested assistance. Vehicle: {vehicle}")

    def addContacts(self):
        self.root.withdraw()
        self.newWindow = tk.CTkToplevel(self.root)
        self.newWindow.title("Modify Contacts")
        self.newWindow.geometry("400x400")

        self.newWindow.protocol("WM_DELETE_WINDOW", self.closeNewWindow)

        self.label = tk.CTkLabel(
            self.newWindow, text="Add your contacts here", font=("Arial", 20))
        self.label.pack(pady=20)

        self.entry = tk.CTkEntry(self.newWindow, font=("Arial", 15))
        self.entry.pack(pady=10)

        self.confirmationLabel = tk.CTkLabel(
            self.newWindow, text="", font=("Arial", 15))
        self.confirmationLabel.pack(pady=10)

        self.addButton = tk.CTkButton(self.newWindow, text="Add", font=(
            "Arial", 15), command=self.addContact)
        self.addButton.pack(pady=10)

        self.closeButton = tk.CTkButton(self.newWindow, text="Close", font=(
            "Arial", 15), command=self.closeNewWindow)
        self.closeButton.pack(pady=10)

    def addContact(self):
        contact = self.entry.get()

        if not contact.isdigit():
            self.confirmationLabel.configure(text=f"Invalid format")
            return

        if (len(contact) == 12 and contact[0:3] != "+91") or len(contact) != 10:
            self.confirmationLabel.configure(text=f"Invalid length")
            return

        modifyContacts.addContact(contact)
        self.confirmationLabel.configure(text=f"Added {contact}")

    def removeContacts(self):
        self.root.withdraw()
        self.newWindow = tk.CTkToplevel(self.root)
        self.newWindow.title("Modify Contacts")
        self.newWindow.geometry("400x400")

        self.newWindow.protocol("WM_DELETE_WINDOW", self.closeNewWindow)

        self.label = tk.CTkLabel(
            self.newWindow, text="Remove your contact here", font=("Arial", 20))
        self.label.pack(pady=20)

        self.entry = tk.CTkEntry(self.newWindow, font=("Arial", 15))
        self.entry.pack(pady=10)

        self.confirmationLabel = tk.CTkLabel(
            self.newWindow, text="", font=("Arial", 15))
        self.confirmationLabel.pack(pady=10)

        self.removeButton = tk.CTkButton(self.newWindow, text="Remove", font=(
            "Arial", 15), command=self.removeContact)
        self.removeButton.pack(pady=10)

        self.closeButton = tk.CTkButton(self.newWindow, text="Close", font=(
            "Arial", 15), command=self.closeNewWindow)
        self.closeButton.pack(pady=10)

    def removeContact(self):
        contact = self.entry.get()

        if not contact.isdigit():
            self.confirmationLabel.configure(text=f"Invalid format")
            return

        if (len(contact) == 12 and contact[0:3] != "+91") or len(contact) != 10:
            self.confirmationLabel.configure(text=f"Invalid length")
            return

        modifyContacts.removeContact(contact)
        self.confirmationLabel.configure(text=f"Removed {contact}")
        self.closeButton.pack(pady=10)

    def closeNewWindow(self):
        self.newWindow.destroy()
        self.root.deiconify()

    def run(self):
        self.root.mainloop()


app = Application()
app.run()
