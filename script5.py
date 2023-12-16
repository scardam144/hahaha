from json import load
from tkinter import Tk, TOP, NE, Frame, BOTH, Canvas, LEFT, ttk, RIGHT, PhotoImage
from random import randint
from time import strftime
from math import sqrt, ceil
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageTk


# import cProfile

# import subprocess
root = Tk()
frame = Frame(root)
result_text = Canvas(frame, bg="white")
counter_label = ttk.Label(root, text="Last count: N/A")
status_label = ttk.Label(root, text="Last checked: N/A")


def ping_ip(ip):
    # Simulate ping result (replace this with actual ping implementation)
    ping_result = [True, False]
    status = randint(0, 1)
    # ping_command = ["ping6", "-c", "4", ip]
    # result = subprocess.run(ping_command, capture_output=True, text=True)
    # print(result)
    # if "100% packet loss" not in result.stdout:
    #       return True
    # else:
    #       return False

    return ping_result[status]


def read_file():
    with open("ipv6.json", "r") as file:
        data = load(file)
    ipv6_array = data["ipv6"]
    return ipv6_array


def calculate_layout(canvas_width, canvas_height, num_ips):
    # Calculate the maximum box width and height based on canvas and no of IP
    val = sqrt(num_ips)
    # print(math.ceil(val))
    max_rect_width = canvas_width / max(1, ceil(val))
    max_rect_height = canvas_height / max(1, round(val))

    return abs(max_rect_width-8), abs(max_rect_height-4)


def check_ips(ipv6_array, count=0):
    # Clear previous content
    result_text.delete("all")
    # Calculate the layout dynamically based on the canvas size and no. of IP's
    rect_width, rect_height = calculate_layout(
        result_text.winfo_width(), result_text.winfo_height(), len(ipv6_array)
    )
    meter_logo_path = "meteR_logo.png"
    pil_image = Image.open(meter_logo_path)
    pil_image = pil_image.resize(
        (round(rect_height/4), round(rect_height/4)), Image.LANCZOS)
    # Resize as needed
    meter_logo = ImageTk.PhotoImage(pil_image)
    mer = PhotoImage(pil_image)
    # Store the reference to the PhotoImage object to prevent garbage
    print(type(meter_logo))
    print(meter_logo)
    print(mer)
    result_text.image = meter_logo

    # Define the margin between rectangles
    margin_x = 4
    margin_y = 4

    # Initialize coordinates for the rectangles
    x, y = margin_x, margin_y
    # count_workers = len(ipv6_array) if len(ipv6_array) < 60 else 50

    # Multiple process should be created to make execution faster
    # with ProcessPoolExecutor(max_workers=count_workers) as executor:
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(ping_ip, ipv6_array))

    for ip, is_pingable in zip(ipv6_array, results):
        # is_pingable = ping_ip(ip)
        # Draw rectangles with borders and different colors
        color = "green" if is_pingable else "red"
        result_text.create_rectangle(
            x, y, x + rect_width, y + rect_height,
            fill=color, outline="black", width=1
        )

        # Draw meter logo in the top-left corner
        result_text.create_image(
            x + 1, y + 1,
            anchor="nw", image=meter_logo
        )

        # Increase the font size and use contrasting text color
        text_color = "white" if is_pingable else "white"
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

    # Update the status label
    counter_label.config(text=f"Ping Count: {count}")
    status_label.config(text="Last checked: " + strftime("%H:%M:%S"))
    count += 1

    # Schedule the next ping check after 20 seconds
    root.after(10000, lambda: check_ips(ipv6_array, count))


def main():
    root.title("FWDevops DMS System")
    root.geometry(
        f"{root.winfo_screenwidth()}x{root.winfo_screenheight()-80}+0+0")
    # Quit button at the top
    quit_button = ttk.Button(root, text="Quit", command=root.destroy)
    quit_button.pack(side=TOP, padx=20, pady=3, anchor=NE)

    # Title label
    title_label = ttk.Label(root, text="FWDevops DMS System", font=12)
    title_label.pack(side=TOP, padx=20, pady=0)

    # Frame to contain the Canvas widget for scrolling
    frame.pack(fill=BOTH, expand=True)

    # Canvas widget to draw colored rectangles
    result_text.pack(side=LEFT, fill=BOTH, expand=True)

    # Counter label
    counter_label.pack(side=RIGHT, padx=20, pady=10)

    # Status label
    status_label.pack(side=RIGHT, padx=20, pady=10)

    # Initial call to check_ips
    ipv6_array = read_file()
    root.after(200, lambda: check_ips(ipv6_array))
    # check_ips(ipv6_array)

    root.mainloop()


if __name__ == "__main__":
    # GUI setup
    # cProfile.run("main()", sort="cumulative")
    main()
