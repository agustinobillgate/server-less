#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Res_line, Reslin_queasy

def resv_extend_report_webbl(from_date:date, to_date:date):

    prepare_cache ([Guest, Res_line, Reslin_queasy])

    output_list_list = []
    oldetd:date = None
    newetd:date = None
    i:int = 0
    str:string = ""
    guest = res_line = reslin_queasy = None

    output_list = gmember = None

    output_list_list, Output_list = create_model("Output_list", {"resdate":date, "zinr":string, "resnr":int, "guestname":string, "pax":int, "arrival":date, "olddepart":date, "newdepart":date, "customer":string, "ratecode":string})

    Gmember = create_buffer("Gmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, oldetd, newetd, i, str, guest, res_line, reslin_queasy
        nonlocal from_date, to_date
        nonlocal gmember


        nonlocal output_list, gmember
        nonlocal output_list_list

        return {"output-list": output_list_list}

    for res_line in db_session.query(Res_line).filter(
             ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Res_line._recid).all():

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "reschanges")],"resnr": [(eq, res_line.resnr)],"date2": [(ge, from_date),(le, to_date)]})

        if reslin_queasy:
            oldetd = date_mdy(entry(2, reslin_queasy.char3, ";"))
            newetd = date_mdy(entry(3, reslin_queasy.char3, ";"))

            if oldetd != newetd:
                output_list = Output_list()
                output_list_list.append(output_list)

                output_list.resdate = reslin_queasy.date2
                output_list.zinr = res_line.zinr
                output_list.resnr = reslin_queasy.resnr
                output_list.guestname = gmember.name + ", " + gmember.vorname1 + " " + gmember.anrede1
                output_list.pax = to_int(entry (6, reslin_queasy.char3, ";")) +\
                        to_int(entry (8, reslin_queasy.char3, ";")) +\
                        to_int(entry (10, reslin_queasy.char3, ";"))
                output_list.arrival = date_mdy(entry (0 , reslin_queasy.char3, ";"))
                output_list.olddepart = date_mdy(entry (2 , reslin_queasy.char3, ";"))
                output_list.newdepart = date_mdy(entry (3 , reslin_queasy.char3, ";"))
                output_list.customer = guest.name + ", " + guest.vorname1 + " " + guest.anrede1


                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        output_list.ratecode = substring(str, 6)
                        break

    return generate_output()