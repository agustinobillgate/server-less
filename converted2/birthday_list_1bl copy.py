from functions.additional_functions import *
import decimal
from datetime import date
from models import Guest, Res_line

def birthday_list_1bl(pvilanguage:int):
    bday_available = False
    s_list_list = []
    lvcarea:str = "birthday-list"
    guest = res_line = None

    s_list = sbuff = None

    s_list_list, S_list = create_model("S_list", {"gastnr":int, "name":str, "zinr":str, "bdate":date, "resstat":str, "abreise":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bday_available, s_list_list, lvcarea, guest, res_line
        nonlocal pvilanguage


        nonlocal s_list, sbuff
        nonlocal s_list_list
        return {"bday_available": bday_available, "s-list": s_list_list}

    def create_list():

        nonlocal bday_available, s_list_list, lvcarea, guest, res_line
        nonlocal pvilanguage


        nonlocal s_list, sbuff
        nonlocal s_list_list


        Sbuff = S_list
        sbuff_list = s_list_list

        res_line_obj_list = []
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (((get_month(Guest.geburtdatum1) == get_month(get_current_date())) &  (get_day(Guest.geburtdatum1) == get_day(get_current_date()))) |  ((get_month(Guest.geburtdatum1) == get_month(get_current_date())) &  (get_day(Guest.geburtdatum1) == (get_day(get_current_date())) + 1)))).filter(
                (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == get_current_date())).order_by(Guest.name, Res_line.zinr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if not sbuff or not(sbuff.gastnr == guest.gastnr):
                sbuff = query(sbuff_list, filters=(lambda sbuff: sbuff.gastnr == guest.gastnr), first=True)

            if not sbuff:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.gastnr = guest.gastnr
                s_list.name = res_line.NAME
                s_list.zinr = res_line.zinr
                s_list.bdate = date_mdy(get_month(guest.geburtdatum1) , get_day(guest.geburtdatum1) , get_year(guest.geburtdatum1))
                s_list.resstat = translateExtended ("Arrival", lvcarea, "")
                s_list.abreise = res_line.abreise


                bday_available = True

        res_line_obj_list = []
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (((get_month(Guest.geburtdatum1) == get_month(get_current_date())) &  (get_day(Guest.geburtdatum1) == get_day(get_current_date()))) |  ((get_month(Guest.geburtdatum1) == get_month(get_current_date())) &  (get_day(Guest.geburtdatum1) == (get_day(get_current_date())) + 1)))).filter(
                (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13))).order_by(Guest.name, Res_line.zinr).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if not sbuff or not(sbuff.gastnr == guest.gastnr and sbuff.resstat.lower()  == ("Inhouse").lower()):
                sbuff = query(sbuff_list, filters=(lambda sbuff: sbuff.gastnr == guest.gastnr and sbuff.resstat.lower()  == ("Inhouse").lower()), first=True)

            if not sbuff:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.gastnr = guest.gastnr
                s_list.name = res_line.NAME
                s_list.zinr = res_line.zinr
                s_list.bdate = date_mdy(get_month(guest.geburtdatum1) , get_day(guest.geburtdatum1) , get_year(guest.geburtdatum1))
                s_list.resstat = translateExtended ("Inhouse", lvcarea, "")
                s_list.abreise = res_line.abreise


                bday_available = True

    create_list()

    return generate_output()