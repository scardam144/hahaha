import json
from tkinter import Tk, TOP, NE, Frame, BOTH, Canvas, LEFT, BOTTOM
from tkinter import ttk
import random
import time
from concurrent.futures import ProcessPoolExecutor


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


def calculate_layout(canvas_width=0):
    # Set a fixed box height
    rect_height = 60

    # Calculate the number of columns based on canvas width
    num_columns = max(1, canvas_width // 60)  # Set a minimum box width of 250

    # Calculate the actual box width
    rect_width = canvas_width // num_columns

    # Calculate the number of rows needed
    # num_rows = (num_ips + num_columns - 1) // num_columns

    return rect_width, rect_height


def check_ips(ipv6_array, count=0):
    # Clear previous content
    result_text.delete("all")

    # Calculate the layout dynamically based on the number of IPs
    # num_ips = len(ipv6_array)
    rect_width, rect_height = calculate_layout(
        canvas_width=result_text.winfo_width())

    # Define the margin between rectangles
    margin_x = 5
    margin_y = 5

    # Initialize coordinates for the rectangles
    x, y = margin_x, margin_y
    # -------
    a = len(ipv6_array) if len(ipv6_array) < 60 else 50
    print(a)

    with ProcessPoolExecutor(max_workers=a) as executor:
        results = list(executor.map(ping_ip, ipv6_array))

    i = 0
    for is_pingable in results:
        # Draw rectangles with borders and different colors
        color = "green" if is_pingable else "red"
        result_text.create_rectangle(
            x, y, x + rect_width, y + rect_height,
            fill=color, outline="black", width=1
        )

        # Increase the font size and use contrasting text color
        text_color = "white"
        ip = ipv6_array[i]
        result_text.create_text(
            x + rect_width // 2, y + rect_height // 2,
            text=f"{ip[-4:]}",
            fill=text_color, font=("Arial", 10, "bold")
        )

        # Update coordinates for the next rectangle with margin
        x += rect_width + margin_x

        # Move to the next row if the current row is filled
        if x + rect_width + margin_x > result_text.winfo_width() - margin_x:
            x = margin_x
            y += rect_height + margin_y
        i+=1

    # Update the status label
    counter_label.config(text=f"Ping Count: {count}")
    status_label.config(text="Last checked: " + time.strftime("%H:%M:%S"))
    count += 1

    # Schedule the next ping check after 20 seconds
    root.after(10000, lambda: check_ips(ipv6_array, count))


# Function to handle canvas resize events
# def on_canvas_resize(event):
    # check_ips(ipv6_array)


if __name__ == "__main__":

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

    # Bind canvas resize event
    # result_text.bind("<Configure>", on_canvas_resize)

    # Counter label
    counter_label = ttk.Label(root, text="Last count: N/A")
    counter_label.pack(side=TOP, pady=5)

    # Status label
    status_label = ttk.Label(root, text="Last checked: N/A")
    status_label.pack(side=BOTTOM, pady=5)

    # Initial call to check_ips
    ipv6_array = read_file()
    check_ips(ipv6_array)

    root.mainloop()
