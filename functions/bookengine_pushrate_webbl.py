#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date

rate_list2_data, Rate_list2 = create_model("Rate_list2", {"origcode":string, "rcode":[Decimal,31], "berates":[Decimal,31], "datum":date})

def bookengine_pushrate_webbl(rate_list2_data:[Rate_list2]):
    echotoken = ""
    timestamp = ""
    rlist_data = []
    uuid:bytes = None

    rate_list2 = rlist = None

    rlist_data, Rlist = create_model("Rlist", {"rcode":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal echotoken, timestamp, rlist_data, uuid
        nonlocal rate_list2_data


        nonlocal rate_list2, rlist
        nonlocal rlist_data

        return {"echotoken": echotoken, "timestamp": timestamp, "rlist": rlist_data}

    uuid = generate_uuid()
    echotoken = guid(uuid)
    timestamp = to_string(get_year(get_current_date()) , "9999") + "-" + to_string(get_month(get_current_date()) , "99") + "-" +\
            to_string(get_day(get_current_date()) , "99") + "T" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + "+00:00"

    for rate_list2 in query(rate_list2_data):

        rlist = query(rlist_data, filters=(lambda rlist: rlist.rcode == entry(0, rate_list2.origcode, ":")), first=True)

        if not rlist:
            rlist = Rlist()
            rlist_data.append(rlist)

            rlist.rcode = entry(0, rate_list2.origcode, ":")

    return generate_output()