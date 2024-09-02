from functions.additional_functions import *
import decimal
from datetime import date

def bookengine_pushrate_webbl(rate_list2:[Rate_list2]):
    echotoken = ""
    timestamp = ""
    rlist_list = []
    uuid:bytes = None

    rate_list2 = rlist = None

    rate_list2_list, Rate_list2 = create_model("Rate_list2", {"origcode":str, "rcode":decimal, "berates":decimal, "datum":date})
    rlist_list, Rlist = create_model("Rlist", {"rcode":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal echotoken, timestamp, rlist_list, uuid


        nonlocal rate_list2, rlist
        nonlocal rate_list2_list, rlist_list
        return {"echotoken": echotoken, "timestamp": timestamp, "rlist": rlist_list}

    uuid = generate_uuid()
    echotoken = guid(uuid)
    timestamp = to_string(get_year(get_current_date()) , "9999") + "-" + to_string(get_month(get_current_date()) , "99") + "-" +\
            to_string(get_day(get_current_date()) , "99") + "T" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + "+00:00"

    for rate_list2 in query(rate_list2_list):

        rlist = query(rlist_list, filters=(lambda rlist :rlist.rcode == entry(0, rate_list2.origcode, ":")), first=True)

        if not rlist:
            rlist = Rlist()
            rlist_list.append(rlist)

            rlist.rcode = entry(0, rate_list2.origcode, ":")

    return generate_output()