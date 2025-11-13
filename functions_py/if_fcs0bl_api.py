#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 13/11/2025
# CM: re-converted from fcs0bl_api.p 
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
import re
from models import Interface, Res_line, Guest, Zimmer

def if_fcs0bl_api(p_type:int, p_status:string):

    prepare_cache ([Interface, Res_line, Guest, Zimmer])

    v_nebenstelle:string = ""
    tt_data_data = []
    interface = res_line = guest = zimmer = None

    tt_data = None

    tt_data_data, Tt_data = create_model("Tt_data", {"date_if":date, "resno":int, "roomno":string, "roomtype":string, "roomstatus":string, "guestname":string, "arrival":date, "departure":date, "status_send":string, "parameters":string, "flags":string, "irecid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_nebenstelle, tt_data_data, interface, res_line, guest, zimmer
        nonlocal p_type, p_status


        nonlocal tt_data
        nonlocal tt_data_data

        return {"tt-data": tt_data_data}

    if p_status == "SUCCESS":
        v_nebenstelle = "*$FCS1$*"
    elif p_status == "FAILED":
        v_nebenstelle = "*$FCS0$*"

    for interface in db_session.query(Interface).filter(
             ((Interface.key == 10) | (Interface.key == 37)) & (matches(Interface.nebenstelle,v_nebenstelle)) & ((Interface.parameters != ("modify").lower()) | ((Interface.parameters == ("modify").lower()) & (Interface.zinr != "")))).order_by(Interface._recid).all():

        tt_data = Tt_data()
        tt_data_data.append(tt_data)
        tt_data.date_if = interface.intdate
        tt_data.roomno = interface.zinr
        tt_data.parameters = interface.parameters
        tt_data.flags = interface.nebenstelle
        
        if matches(interface.nebenstelle, "*$FCS1$*"):
            tt_data.status_send = "SUCCESS"
        else:
            tt_data.status_send = "FAILED"
        tt_data.irecid = to_int(interface._recid)

        if p_type == 1:
            tt_data.resno = interface.resnr

            res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)]})

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    tt_data.guestname = guest.name
                    tt_data.arrival = res_line.ankunft
                    tt_data.departure = res_line.abreise

        if p_type == 2:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, interface.zinr)]})

            if zimmer:
                tt_data.roomtype = zimmer.kbezeich

                if zimmer.zistatus == 0:
                    tt_data.roomstatus = "Vacant Clean Checked"
                elif zimmer.zistatus == 1:
                    tt_data.roomstatus = "Vacant Clean Unchecked"
                elif zimmer.zistatus == 2:
                    tt_data.roomstatus = "Vacant Dirty"
                elif zimmer.zistatus == 3:
                    tt_data.roomstatus = "Expected Departure"
                elif zimmer.zistatus == 4:
                    tt_data.roomstatus = "Occupied Dirty"
                elif zimmer.zistatus == 5:
                    tt_data.roomstatus = "Occupied Cleaned"
                elif zimmer.zistatus == 6:
                    tt_data.roomstatus = "Out of Order"
                elif zimmer.zistatus == 7:
                    tt_data.roomstatus = "Off Market"
                elif zimmer.zistatus == 8:
                    tt_data.roomstatus = "Do Not Disturb"
                else:
                    tt_data.roomstatus = "Unknown"

    return generate_output()