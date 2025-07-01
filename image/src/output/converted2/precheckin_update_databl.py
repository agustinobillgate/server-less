#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Queasy, Guest, Reslin_queasy

def precheckin_update_databl(res_number:int, resline_number:int, est_at:int, pickrequest:bool, pickdetail:string, room_preferences:string, spesial_req:string, guest_phnumber:string, guest_nationality:string, guest_country:string, guest_region:string, agreed_term:bool, purpose_of_stay:string):

    prepare_cache ([Res_line, Queasy, Guest, Reslin_queasy])

    mess_result = ""
    segm__purcode:int = 0
    res_line = queasy = guest = reslin_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, segm__purcode, res_line, queasy, guest, reslin_queasy
        nonlocal res_number, resline_number, est_at, pickrequest, pickdetail, room_preferences, spesial_req, guest_phnumber, guest_nationality, guest_country, guest_region, agreed_term, purpose_of_stay

        return {"mess_result": mess_result}


    if res_number == 0 or res_number == None or resline_number == 0 or resline_number == None:
        mess_result = "1 - Reservation Number and Line can't be null!"

        return generate_output()

    if purpose_of_stay == "" or purpose_of_stay == None:
        mess_result = "2 - Purpose Of Stay can't be null!"

        return generate_output()

    if pickdetail == None:
        pickdetail = ""

    if room_preferences == None:
        room_preferences = ""

    if spesial_req == None:
        spesial_req = ""

    if guest_phnumber == None:
        guest_phnumber = ""

    if guest_nationality == None:
        guest_nationality = ""

    if guest_country == None:
        guest_country = ""

    if guest_region == None:
        guest_region = ""

    res_line = get_cache (Res_line, {"resnr": [(eq, res_number)],"reslinnr": [(eq, resline_number)]})

    if res_line:

        queasy = get_cache (Queasy, {"key": [(eq, 143)],"char3": [(eq, purpose_of_stay)]})

        if queasy:
            segm__purcode = queasy.number1

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            guest.mobil_telefon = guest_phnumber
            guest.nation1 = guest_nationality
            guest.land = guest_country
            guest.geburt_ort2 = guest_region


        res_line.abreisezeit = est_at
        res_line.zimmer_wunsch = res_line.zimmer_wunsch +\
                "PCIFLAG=YES|PICKUP=" + to_string(pickrequest) +\
                "|pickdetail=" + pickdetail +\
                "|ROOMREF=" + room_preferences +\
                "|TERM=" + to_string(agreed_term) +\
                ";SEGM_PUR" + to_string(segm__purcode) +\
                ";"

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if reslin_queasy:
            reslin_queasy.char3 = reslin_queasy.char3 + "," + spesial_req


        else:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "specialRequest"
            reslin_queasy.resnr = res_line.resnr
            reslin_queasy.reslinnr = res_line.reslinnr


        mess_result = "0 - update data success"

    return generate_output()