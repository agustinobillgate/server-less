
#---------------------------------
# uvicorn webview_log:app --reload
# uvicorn webview_log:app --reload
#---------------------------------

import matplotlib
matplotlib.use("Agg")  # must be first to prevent Tkinter backend
from fastapi import FastAPI, Response
import pandas as pd
import matplotlib.pyplot as plt
import io, re
from datetime import datetime


app = FastAPI(title="CPU Log API")

LOG_FILE = "cpu_stats_20schema.txt"

# --- Helper untuk parsing log ---
def parse_cpu_log(filepath: str):
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
    with open(filepath) as f:
        for line in f:
            m = pattern.search(line)
            if m:
                data = m.groupdict()
                data["datetime"] = datetime.strptime(data["datetime"], "%Y%m%d-%H:%M:%S")
                for key in ["us", "sy", "ni", "id", "wa", "hi", "si", "st"]:
                    data[key] = float(data[key])
                records.append(data)

    return pd.DataFrame(records)


# --- Endpoint 1: Return data JSON ---
@app.get("/cpu/data")
def get_cpu_data():
    df = parse_cpu_log(LOG_FILE)
    if df.empty:
        return {"message": "No data found"}
    return df.to_dict(orient="records")


# --- Endpoint 2: Return chart PNG ---
@app.get("/cpu/chart")
def get_cpu_chart():
    df = parse_cpu_log(LOG_FILE)

    if df.empty:
        return Response(content="No data found in log file.", media_type="text/plain")

    # Gunakan Figure langsung, bukan plt global
    from matplotlib.figure import Figure
    import io

    fig = Figure(figsize=(10, 5))
    ax = fig.subplots()

    # Plot data
    ax.plot(df["datetime"], df["us"], label="User (%)")
    ax.plot(df["datetime"], df["sy"], label="System (%)")
    ax.plot(df["datetime"], 100 - df["id"], label="Total Usage (%)", linewidth=2)

    ax.set_title("CPU Usage Over Time")
    ax.set_xlabel("Time")
    ax.set_ylabel("CPU %")
    ax.legend()
    ax.grid(True)

    # Simpan ke buffer
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)

    return Response(content=buf.getvalue(), media_type="image/png")


