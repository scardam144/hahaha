import json
from tkinter import *
from tkinter import ttk
import random
import time

def ping_ip(ip):
    # Simulate ping result (replace this with actual ping implementation)
    ping_result = [True, False]
    status = random.randint(0, 1)
    return ping_result[status]

def read_file():
    with open("ipv6.json", "r") as file:
        data = json.load(file)

    ipv6_array = data["ipv6"]
    return ipv6_array

def check_ips(ipv6_array):
    # Clear previous content
    result_text.delete("all")

    # Define initial y-coordinate for the rectangles and text
    y = 10

    for ip in ipv6_array:
        is_pingable = ping_ip(ip)

        # Draw rectangles with different colors
        color = "green" if is_pingable else "red"
        result_text.create_rectangle(10, y, 490, y + 20, fill=color)
        result_text.create_text(250, y + 10, text=f"{ip}: {is_pingable}", fill="white")

        # Increment y-coordinate for the next rectangle and text
        y += 25  # Adjust this value based on your desired vertical spacing

    # Update the status label
    status_label.config(text="Last checked: " + time.strftime("%H:%M:%S"))

    # Schedule the next ping check after 20 seconds
    root.after(20000, lambda: check_ips(ipv6_array))

# GUI setup
root = Tk()
root.title("IPv6 Ping Result")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()-80}+0+0")

# Top Frame for buttons
top_frame = ttk.Frame(root)
top_frame.pack(side=TOP, fill=X)

# Buttons
#check_button = ttk.Button(top_frame, text="Check IPs", command=lambda: check_ips(ipv6_array))
#check_button.pack(side=LEFT, padx=10, pady=10)

quit_button = ttk.Button(top_frame, text="Quit", command=root.destroy)
quit_button.pack(side=RIGHT, padx=10, pady=10)

# Canvas widget to draw colored rectangles
result_text = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()-200, bg="white")
result_text.pack(fill=BOTH, expand=True)

# Status label
status_label = ttk.Label(root, text="Last checked: N/A")
status_label.pack(side=BOTTOM, pady=5)

# Initial call to check_ips
ipv6_array = read_file()
check_ips(ipv6_array)

root.mainloop()
