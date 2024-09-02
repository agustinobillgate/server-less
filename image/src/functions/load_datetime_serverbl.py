from functions.additional_functions import *
import decimal
from datetime import date

def format_time(time_value):
    # Convert seconds to timedelta
    time_delta = timedelta(seconds=time_value)

    # Create a base date (1st January 1970, which is the epoch)
    base_date = datetime(1970, 1, 1)

    # Add the timedelta to the base date to get the final datetime object
    final_datetime = base_date + time_delta

    # Format the datetime object
    formatted_time = final_datetime.strftime('%H:%M:%S')

    return formatted_time

def load_datetime_serverbl():
    datetime_server = ""
    bill_date:date = None
    curr_zeit:int = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal datetime_server, bill_date, curr_zeit
        return {"datetime_server": datetime_server}

    curr_zeit = get_current_time_in_seconds()
    current_date_str = to_string(get_current_date(), "%d/%m/%y")
    current_time_str = format_time(curr_zeit)
    
    datetime_server = f"{current_date_str} {current_time_str}"

    print("Datetime_server:", datetime_server)


    

    return generate_output()