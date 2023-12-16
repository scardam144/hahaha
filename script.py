import json
import subprocess
import time

count = 0
with open("ipv6.json", "r") as file:
    data = json.load(file)

ipv6_array = data["ipv6"]
while True:
    for ip in ipv6_array:
        ping_command = ["ping6", "-c", "4", ip]
        result = subprocess.run(ping_command, capture_output=True, text=True)
        # print(result)
        if "100% packet loss" not in result.stdout:
            print(f"Ping to {ip} was successful. True")
        else:
            print(f"Ping to {ip} had packet loss. False")

    # Sleeping for 10sec and then repeating the same proccess.
    count += 1
    print(f"{count} iteration completed.")
    time.sleep(10)
