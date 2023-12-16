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


def calculate_layout(num_ips, max_columns=3, canvas_width=0):
    # Calculate the number of rows and columns dynamically
    num_columns = min(num_ips, max_columns)
    # Adjusted for margin and space for scrollbar
    rect_width = (canvas_width - 40) // num_columns
    rect_height = 70  # Fixed box height to ensure a constant minimum height

    return rect_width, rect_height


def check_ips(ipv6_array):
    # Clear previous content
    result_text.delete("all")

    # Calculate the layout dynamically based on the number of IPs and canvas width
    num_ips = len(ipv6_array)
    rect_width, rect_height = calculate_layout(num_ips, canvas_width=result_text.winfo_width())

    # Define the margin between rectangles
    margin = 10

    # Initialize coordinates for the rectangles
    x, y = 10, 10

    for ip in ipv6_array:
        is_pingable = ping_ip(ip)

        # Draw rectangles with borders and different colors
        color = "green" if is_pingable else "red"
        result_text.create_rectangle(
            x, y, x + rect_width, y + rect_height,
            fill=color, outline="black", width=1
        )

        # Increase the font size and use contrasting text color
        text_color = "white" if is_pingable else "white"
        result_text.create_text(
            x + rect_width // 2, y + rect_height // 2,
            text=f"{ip}: {'Pingable' if is_pingable else 'Not Reachable'}",
            fill=text_color, font=("Arial", 10, "bold")
        )

        # Update coordinates for the next rectangle with margin
        x += rect_width + margin

        # Move to the next row if the current row is filled
        if x + rect_width + margin > (result_text.winfo_width()):
            x = 10
            y += rect_height + margin

    # Update the status label
    status_label.config(text="Last checked: " + time.strftime("%H:%M:%S"))

    # Configure the canvas scroll region
    result_text.config(scrollregion=result_text.bbox("all"))

    # Schedule the next ping check after 20 seconds
    root.after(10000, lambda: check_ips(ipv6_array))


# Function to handle mouse wheel events for scrolling
def on_mouse_wheel(event):
    result_text.yview_scroll(-1 * (event.delta // 120), "units")


# Function to handle canvas resize events
def on_canvas_resize(event):
    check_ips(ipv6_array)


# GUI setup
root = Tk()
root.title("IPv6 Ping Result")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()-80}+0+0")

# Quit button at the top
quit_button = ttk.Button(root, text="Quit", command=root.destroy)
quit_button.pack(side=TOP, padx=20, pady=10, anchor=NE)


# Frame to contain the Canvas widget for scrolling
frame = Frame(root)
frame.pack(fill=BOTH, expand=True)

# Canvas widget to draw colored rectangles
result_text = Canvas(frame, bg="white")
result_text.pack(side=LEFT, fill=BOTH, expand=True)

# Scrollbar
scrollbar = Scrollbar(frame, command=result_text.yview, width=25)
scrollbar.pack(side=RIGHT, fill=Y)
result_text.configure(yscrollcommand=scrollbar.set)

# Bind mouse wheel event to the canvas
result_text.bind("<MouseWheel>", on_mouse_wheel)

# Bind canvas resize event
result_text.bind("<Configure>", on_canvas_resize)

# Status label
status_label = ttk.Label(root, text="Last checked: N/A")
status_label.pack(side=BOTTOM, pady=5)

# Initial call to check_ips
ipv6_array = read_file()
check_ips(ipv6_array)

root.mainloop()
