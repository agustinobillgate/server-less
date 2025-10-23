import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Ganti ini dengan path file log kamu
LOG_FILE = "cpu_stats_20schema.txt"

# Regex untuk ambil data
pattern = re.compile(
    r"(?P<datetime>\d{8}-\d{2}:\d{2}:\d{2}) %Cpu\(s\):\s+"
    r"(?P<us>[\d\.]+) us,\s+"
    r"(?P<sy>[\d\.]+) sy,\s+"
    r"(?P<ni>[\d\.]+) ni,\s+"
    r"(?P<id>[\d\.]+) id,\s+"
    r"(?P<wa>[\d\.]+) wa,\s+"
    r"(?P<hi>[\d\.]+) hi,\s+"
    r"(?P<si>[\d\.]+) si,\s+"
    r"(?P<st>[\d\.]+) st"
)

records = []

with open(LOG_FILE) as f:
    for line in f:
        m = pattern.search(line)
        if m:
            data = m.groupdict()
            # Convert datetime
            data["datetime"] = datetime.strptime(data["datetime"], "%Y%m%d-%H:%M:%S")
            # Convert numeric
            for key in ["us", "sy", "ni", "id", "wa", "hi", "si", "st"]:
                data[key] = float(data[key])
            records.append(data)

# Buat DataFrame
df = pd.DataFrame(records)

if df.empty:
    print("Tidak ada data terbaca dari log.")
else:
    # Plot grafik CPU usage
    plt.figure(figsize=(10,5))
    plt.plot(df["datetime"], df["us"], label="User (%)")
    plt.plot(df["datetime"], df["sy"], label="System (%)")
    plt.plot(df["datetime"], 100 - df["id"], label="Total Usage (%)", linewidth=2)

    plt.title("CPU Usage Over Time")
    plt.xlabel("Time")
    plt.ylabel("CPU %")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
