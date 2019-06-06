import os
from datetime import datetime, timedelta
import screenshot_parse

LAST_PARSED_FILE = "output/last_parsed"
OUTPUT_FILE = "output/parsed_hp.csv"

if __name__ == "__main__":
    last_parsed = 0
    if os.path.isfile(LAST_PARSED_FILE):
        last_parsed = int(open(LAST_PARSED_FILE, "r").read())

    if not os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "w") as f:
            f.write("Pacific Time,HP,Screenshot,Errors\n")

    for file in sorted(os.listdir("input")):
        if not file.endswith(".png"):
            continue

        created_timestamp = os.path.basename(file).split(".")[0]
        if not int(created_timestamp) > last_parsed:
            continue

        result, error = screenshot_parse.parse_onigashima(f"input/{file}")
        created_time = datetime.utcfromtimestamp(int(created_timestamp)) + timedelta(hours=-7)
        with open(OUTPUT_FILE, "a") as f:
            if error:
                f.write(f'{created_time},,https://assets.atlasacademy.io/raid/{file},{error}\n')
            else:
                f.write(f'{created_time},{result},https://assets.atlasacademy.io/raid/{file},\n')

        with open(LAST_PARSED_FILE, "w+") as f:
            f.write(f"{created_timestamp}")

        print(f"{file} {result}")
