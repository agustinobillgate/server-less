from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Res_line, Queasy, Guest, Reslin_queasy

def precheckin_update_databl(res_number:int, resline_number:int, est_at:int, pickrequest:bool, pickdetail:str, room_preferences:str, spesial_req:str, guest_phnumber:str, guest_nationality:str, guest_country:str, guest_region:str, agreed_term:bool, purpose_of_stay:str):
    mess_result = ""
    segm__purcode:int = 0
    res_line = queasy = guest = reslin_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, segm__purcode, res_line, queasy, guest, reslin_queasy


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

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == res_number) &  (Res_line.reslinnr == resline_number)).first()

    if res_line:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 143) &  (func.lower(Queasy.char3) == (purpose_of_stay).lower())).first()

        if queasy:
            segm__purcode = queasy.number1

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

        if guest:
            guest.mobil_telefon = guest_phnumber
            guest.nation1 = guest_nationality
            guest.land = guest_country
            guest.geburt_ort2 = guest_region


        res_line.abreisezeit = est_at
        res_line.zimmer_wunsch = res_line.zimmer_wunsch +\
                "PCIFLAG == YES|PICKUP == " + to_string(pickrequest) +\
                "|pickdetail == " + pickdetail +\
                "|ROOMREF == " + room_preferences +\
                "|TERM == " + to_string(agreed_term) +\
                ";SEGM__PUR" + to_string(segm__purcode) +\
                ";"

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "specialRequest") &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

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