import logging
from tkinter import ttk
import customtkinter as tk
import json
import folium
import webbrowser
import time
import threading

WIDTH = 400
HEIGHT = WIDTH
logging.basicConfig(filename='db\\log.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('twilio').setLevel(logging.WARNING)


class Application:
    def __init__(self):
        self.root = tk.CTk()
        self.root.title("Admin App")
        self.root.geometry("840x840")

        self.locationBtn = tk.CTkButton(
            self.root, text="Get Details", width=WIDTH, height=HEIGHT, command=self.getDetails)
        self.showLocations = tk.CTkButton(
            self.root, text="Show Locations", width=WIDTH, height=HEIGHT, command=self.getLocations)
        self.activeRequest = tk.CTkButton(
            self.root, text="Active Requests", width=WIDTH, height=HEIGHT, command=self.activeRequests)
        self.requestLog = tk.CTkButton(
            self.root, text="Requests Log", width=WIDTH, height=HEIGHT, command=self.getLog)

        self.locationBtn.grid(row=0, column=0, padx=10, pady=10)
        self.showLocations.grid(row=0, column=1, padx=10, pady=10)
        self.activeRequest.grid(row=1, column=0, padx=10, pady=10)
        self.requestLog.grid(row=1, column=1, padx=10, pady=10)

        self.root.resizable(False, False)

    def getDetails(self):
        self.root.withdraw()
        self.newWindow = tk.CTkToplevel(self.root)
        self.newWindow.title("Get Details")

        self.newWindow.protocol("WM_DELETE_WINDOW", self.closeNewWindow)

        with open("db\\vehicle_database.json", "r") as f:
            data = json.load(f)

        tree = ttk.Treeview(self.newWindow)

        tree['columns'] = ['ID'] + list(next(iter(data.values())).keys())

        for col in tree['columns']:
            tree.column(col, width=100)
            tree.heading(col, text=col)

        for id, item in data.items():
            values = [id] + list(item.values())
            tree.insert('', 'end', text="Item {}".format(id), values=values)

        tree.pack()

    def update_map(self):
        while not self.stop_thread:
            with open("db\\vehicle_database.json", "r") as f:
                data = json.load(f)

            map = folium.Map(location=[22.5, 82.2], zoom_start=5)

            for user in data:
                location = data[user]['location']
                icon = folium.Icon(
                    color="red" if data[user]['marked'] else "green", icon="MARKED" if data[user]['marked'] else "")
                folium.Marker(location, icon=icon).add_to(map)

            html = map._repr_html_()

            with open('db\\map.html', 'w') as f:
                f.write(html)

            time.sleep(0.5)

    def getLocations(self):
        self.root.withdraw()
        self.newWindow = tk.CTkToplevel(self.root)
        self.newWindow.title("Get Details")

        self.newWindow.protocol("WM_DELETE_WINDOW", self.closeNewWindow)

        self.stop_thread = False
        self.map_thread = threading.Thread(target=self.update_map)
        self.map_thread.start()

        threading.Thread(target=self.update_map).start()

        webbrowser.open_new_tab('db\\map.html')

        self.closeButton = tk.CTkButton(self.newWindow, text="Close", font=(
            "Arial", 15), command=self.closeNewWindow)
        self.closeButton.pack(pady=10)

    def activeRequests(self):
        self.root.withdraw()
        self.newWindow = tk.CTkToplevel(self.root)
        self.newWindow.title("Active Requests")

        self.newWindow.protocol("WM_DELETE_WINDOW", self.closeNewWindow)

        with open("db\\pending_requests.json", "r") as f:
            data = json.load(f)

        pending_requests = data.get("pending", {})

        for id, vehicle in pending_requests.items():
            button = tk.CTkButton(self.newWindow, text=f"Resolve {id}", font=(
                "Arial", 15), command=lambda request_id=id, vehicle=vehicle: self.resolveRequest(request_id, vehicle))
            button.pack(pady=10)

        self.closeButton = tk.CTkButton(self.newWindow, text="Close", font=(
            "Arial", 15), command=self.closeNewWindow)
        self.closeButton.pack(pady=10)

    def resolveRequest(self, request_id, vehicle):
        with open("db\\pending_requests.json", "r+") as f:
            data = json.load(f)
            if request_id in data["pending"]:
                resolved_request = data["pending"].pop(request_id)
                data["resolved"].append(resolved_request)
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
                self.newWindow.destroy()
                self.root.deiconify()

        with open("db\\vehicle_database.json", "r") as f:
            data = json.load(f)
        data[vehicle]['marked'] = False

        with open("db\\vehicle_database.json", 'w') as f:
            json.dump(data, f, indent=4)

        logger.info(f"{request_id} is resolved")

    def getLog(self):
        self.root.withdraw()
        self.newWindow = tk.CTkToplevel(self.root)
        self.newWindow.title("Log")
        self.newWindow.geometry("700x400")

        self.newWindow.protocol("WM_DELETE_WINDOW", self.closeNewWindow)

        with open("db\\log.log") as f:
            data = f.read()

        scrollbar = tk.CTkScrollbar(self.newWindow)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_area = tk.CTkTextbox(self.newWindow, yscrollcommand=scrollbar.set)
        text_area.pack(fill=tk.BOTH)
        text_area.insert(tk.END, data)

        scrollbar.configure(command=text_area.yview)

        self.closeButton = tk.CTkButton(self.newWindow, text="Close", font=(
            "Arial", 15), command=self.closeNewWindow)
        self.closeButton.pack(pady=10)

    def closeNewWindow(self):
        self.stop_thread = True
        if hasattr(self, 'map_thread') and self.map_thread:
            self.map_thread.join(timeout=0.5)
        if hasattr(self, 'newWindow') and self.newWindow:
            self.newWindow.destroy()
        self.root.deiconify()

    def run(self):
        self.root.mainloop()


app = Application()
app.run()
