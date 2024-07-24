# /project/frontend/home.py
import tkinter as tk
from tkinter import ttk
import sys
import os
from PIL import Image, ImageTk

# Adjust the system path to import from the backend directory
#sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from backend_func import *
from database_func import *
# from backend.database_init import * might not need this, gonna start the database in the backend_init probably
from backend_init import *

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Friendly DNS")
        self.geometry("1280x720")
        self._frame = None
        #self.iconbitmap("friendly-DNS\\backend\\assets\SmileyFace.png")
        self.create_sidebar()
        self.switch_frame(HomePage)

    def create_sidebar(self):
        # Create the sidebar frame
        sidebar = ttk.Frame(self, width=150, relief=tk.RAISED, borderwidth=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Load the logo image
        #logo_image = tk.PhotoImage(file="friendly-DNS\\backend\\assets\Friendly-DNS-logo.png")  # Replace with your image path
        img = Image.open("friendly-DNS\\backend\\assets\Friendly-DNS-logo.png")
        img = img.resize((250, 50), Image.ANTIALIAS)
        #logo = tk.Label(sidebar, image=logo_image)
        # logo.image = logo_image 
        #logo.pack(pady=20)

            # Convert to PhotoImage
        photo_img = ImageTk.PhotoImage(img)

        # Create a label to hold the image
        logo_label = ttk.Label(sidebar, image=photo_img)
        logo_label.image = photo_img  # Keep a reference!
        logo_label.pack(side="top", pady=10)  # Pack at the top of the window

        # Add the sidebar buttons
        home_button = ttk.Button(sidebar, text="Home", command=lambda: self.switch_frame(HomePage))
        all_servers_button = ttk.Button(sidebar, text="All Servers", command=lambda: self.switch_frame(AllServersPage))
        local_servers_button = ttk.Button(sidebar, text="Local Servers", command=lambda: self.switch_frame(LocalServersPage))
        logs_button = ttk.Button(sidebar, text="Logs", command=lambda: self.switch_frame(Logs))
        
        home_button.pack(fill=tk.X, padx=5, pady=5)
        all_servers_button.pack(fill=tk.X, padx=5, pady=5)
        local_servers_button.pack(fill=tk.X, padx=5, pady=5)
        logs_button.pack(fill=tk.X, padx=5, pady=5)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

class HomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        '''mid_top_frame = ttk.Frame(self)
        mid_top_frame.pack(fill=tk.X, padx=10, pady=10)

        avg_load = 
        uptime_str = 

        load_system = ttk.Label(mid_top_frame, text=avg_load, background="lightgrey", padding=10)
        uptime_system = ttk.Label(mid_top_frame, text=uptime_str, background="lightgrey", padding=10)

        load_system.pack(side=tk.LEFT, padx=20, pady=5)
        uptime_system.pack(side=tk.LEFT, padx=20, pady=5)'''

        # Frame for load average and uptime
        mid_top_frame = ttk.Frame(self)
        mid_top_frame.pack(fill=tk.X, padx=10, pady=10)

        avg_load = "Load Average:   " + load_average()
        uptime_str = uptime() 
        
        load_system = ttk.Label(mid_top_frame, text=avg_load, background="lightgrey", padding=10)
        uptime_system = ttk.Label(mid_top_frame, text=uptime_str, background="lightgrey", padding=10)

        load_system.pack(side=tk.LEFT, padx=20, pady=5)
        uptime_system.pack(side=tk.LEFT, padx=20, pady=5)

        # Add a title label below the load and uptime widgets
        title_label = ttk.Label(self, text="Welcome to Friendly DNS", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=20)  # Adding some padding for visual separation

        # Description text
        text_label = ttk.Label(self, text="This program was created by Maria Eduarda Joazeiro Gomes for my Senior Design project (Summer 2024). \n\nThe idea of this project is to provide networking beginners with a simple UI that will allow them to easily manage a Linux VM acting as a DNS server on their network", font=('Helvetica', 12), wraplength=500, justify=tk.CENTER)
        text_label.pack(pady=20)

        my_system_info = grab_system_info()
        ttk.Label(self, text=f"CPU: {my_system_info['cpu']}", font=('Helvetica', 10)).pack(anchor=tk.W)
        ttk.Label(self, text=f"RAM: {my_system_info['ram']}", font=('Helvetica', 10)).pack(anchor=tk.W)
        ttk.Label(self, text=f"OS: {my_system_info['os']}", font=('Helvetica', 10)).pack(anchor=tk.W)

class AllServersPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = None  # Initialize tree as None
        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        add_button = ttk.Button(top_frame, text="Add", command=self.add_entry)
        delete_button = ttk.Button(top_frame, text="Delete", command=self.delete_entry)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("Hostname", "IP Address"), show='headings')
        self.tree.column("Hostname", anchor=tk.CENTER)
        self.tree.column("IP Address", anchor=tk.CENTER)
        self.tree.heading("Hostname", text="Hostname", anchor=tk.CENTER)
        self.tree.heading("IP Address", text="IP Address", anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load initial data from the servers
        servers = get_all_servers()
        for server in servers:
            self.tree.insert("", "end", values=server)

    def add_entry(self):
        popup = AddDeletePopup(self, "Add Entry", "Enter hostname and IP address:")
        self.wait_window(popup.top)
        if popup.result:
            hostname, ip_address = popup.result
            add_all_server(hostname, ip_address)  # Function to add server to the backend database
            self.tree.insert("", "end", values=(hostname, ip_address))  # Insert into the treeview

    def delete_entry(self):
        popup = AddDeletePopup(self, "Delete Entry", "Enter IP address to delete:")
        self.wait_window(popup.top)
        if popup.result:
            ip_address = popup.result[0]
            remove_all_server(ip_address)  # Function to remove server from the backend database
            # Remove from the treeview
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[1] == ip_address:
                    self.tree.delete(item)
                    break

class LocalServersPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.tree = None  # Initialize tree as None
        self.create_widgets()

    def create_widgets(self):
        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        add_button = ttk.Button(top_frame, text="Add", command=self.add_entry)
        delete_button = ttk.Button(top_frame, text="Delete", command=self.delete_entry)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=("Hostname", "IP Address"), show='headings')
        self.tree.column("Hostname", anchor=tk.CENTER)
        self.tree.column("IP Address", anchor=tk.CENTER)
        self.tree.heading("Hostname", text="Hostname", anchor=tk.CENTER)
        self.tree.heading("IP Address", text="IP Address", anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Load initial data from the servers
        servers = get_local_servers()
        for server in servers:
            self.tree.insert("", "end", values=server)

    def add_entry(self):
        popup = AddDeletePopup(self, "Add Entry", "Enter hostname and IP address:")
        self.wait_window(popup.top)
        if popup.result:
            hostname, ip_address = popup.result
            add_local_server(hostname, ip_address)  # Function to add server to the backend database
            self.tree.insert("", "end", values=(hostname, ip_address))  # Insert into the treeview

    def delete_entry(self):
        popup = AddDeletePopup(self, "Delete Entry", "Enter IP address to delete:")
        self.wait_window(popup.top)
        if popup.result:
            ip_address = popup.result[0]
            remove_local_server(ip_address)  # Function to remove server from the backend database
            # Remove from the treeview
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[1] == ip_address:
                    self.tree.delete(item)
                    break

class Logs(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        all_logs = get_logs()
        tree = ttk.Treeview(self, columns=("Hostname", "IP Address", "Action", "Time"), show='headings')
        
        # Configure the columns
        tree.column("Hostname", anchor=tk.CENTER)
        tree.column("IP Address", anchor=tk.CENTER)
        tree.column("Action", anchor=tk.CENTER)
        tree.column("Time", anchor=tk.CENTER)
        
        # Set the headers
        tree.heading("Hostname", text="Hostname", anchor=tk.CENTER)
        tree.heading("IP Address", text="IP Address", anchor=tk.CENTER)
        tree.heading("Action", text="Action", anchor=tk.CENTER)
        tree.heading("Time", text="Time", anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Insert data into the treeview
        for log in all_logs:
            tree.insert("", "end", values=log)

class AddDeletePopup:
    def __init__(self, parent, title, label_text):
        top = self.top = tk.Toplevel(parent)
        top.title(title)
        top.geometry("300x150")  # Set a fixed size for the popup

        self.label = tk.Label(top, text=label_text)
        self.label.pack(padx=10, pady=10)

        self.entry1 = ttk.Entry(top)
        self.entry1.pack(padx=10, pady=5)

        # If it's an add operation, ask for both hostname and IP
        if "Add" in title:
            self.entry2 = ttk.Entry(top)
            self.entry2.pack(padx=10, pady=5)
        
        self.ok_button = ttk.Button(top, text="OK", command=self.ok)
        self.ok_button.pack(pady=10)

        self.cancel_button = ttk.Button(top, text="Cancel", command=self.cancel)
        self.cancel_button.pack(pady=5)

        self.result = None

    def ok(self):
        # Gather the results from the entries
        if hasattr(self, 'entry2'):
            self.result = (self.entry1.get(), self.entry2.get())
        else:
            self.result = (self.entry1.get(),)
        self.top.destroy()

    def cancel(self):
        # Close the popup without doing anything
        self.top.destroy()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
