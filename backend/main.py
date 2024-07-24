# /project/frontend/home.py
import tkinter as tk
from tkinter import ttk
import sys
import os
from PIL import Image
from PIL import ImageTk

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
        self.create_sidebar()
        self.switch_frame(HomePage)

    def create_sidebar(self):
        # Create the sidebar frame
        sidebar = ttk.Frame(self, width=150, relief=tk.RAISED, borderwidth=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # Load the logo image
        logo_image = tk.PhotoImage(file="friendly-DNS\\backend\\assets\\finally-a-pictue.png")  # Replace with your image path
        logo = tk.Label(sidebar, image=logo_image)
        # logo.image = logo_image 
        logo.pack(pady=20)

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
        mid_top_frame = ttk.Frame(self)
        mid_top_frame.pack(fill=tk.X, padx=10, pady=10)

        avg_load = load_average()
        uptime_str = uptime() 

        element1 = ttk.Label(mid_top_frame, text=avg_load, background="lightgrey", padding=10)
        element2 = ttk.Label(mid_top_frame, text=uptime_str, background="lightgrey", padding=10)

        element1.pack(side=tk.LEFT, padx=5, pady=5)
        element2.pack(side=tk.LEFT, padx=5, pady=5)

class AllServersPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        servers = get_all_servers()
        tree = ttk.Treeview(self, columns=("Hostname", "IP Address"), show='headings')
        
        # Configure the columns
        tree.column("Hostname", anchor=tk.CENTER)
        tree.column("IP Address", anchor=tk.CENTER)
        
        # Set the headers
        tree.heading("Hostname", text="Hostname", anchor=tk.CENTER)
        tree.heading("IP Address", text="IP Address", anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Insert data into the treeview
        for server in servers:
            tree.insert("", "end", values=server)

class LocalServersPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        servers = get_local_servers()
        tree = ttk.Treeview(self, columns=("Hostname", "IP Address"), show='headings')
        
        # Configure the columns
        tree.column("Hostname", anchor=tk.CENTER)
        tree.column("IP Address", anchor=tk.CENTER)
        
        # Set the headers
        tree.heading("Hostname", text="Hostname", anchor=tk.CENTER)
        tree.heading("IP Address", text="IP Address", anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Insert data into the treeview
        for server in servers:
            tree.insert("", "end", values=server)

class Logs(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        all_logs = get_logs()
        tree = ttk.Treeview(self, columns=("Hostname Before", "Hostname After", "IP Address Before", "IP Address After", "Time"), show='headings')
        
        # Configure the columns
        tree.column("Hostname Before", anchor=tk.CENTER)
        tree.column("Hostname After", anchor=tk.CENTER)
        tree.column("IP Address Before", anchor=tk.CENTER)
        tree.column("IP Address After", anchor=tk.CENTER)
        tree.column("Time", anchor=tk.CENTER)
        
        # Set the headers
        tree.heading("Hostname Before", text="Hostname Before", anchor=tk.CENTER)
        tree.heading("Hostname After", text="Hostname After", anchor=tk.CENTER)
        tree.heading("IP Address Before", text="IP Address Before", anchor=tk.CENTER)
        tree.heading("IP Address After", text="IP Address After", anchor=tk.CENTER)
        tree.heading("Time", text="Time", anchor=tk.CENTER)
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # Insert data into the treeview
        for log in all_logs:
            tree.insert("", "end", values=log)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
