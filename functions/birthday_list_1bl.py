#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Res_line

def birthday_list_1bl(pvilanguage:int):

    prepare_cache ([Guest, Res_line])

    bday_available = False
    s_list_data = []
    lvcarea:string = "birthday-list"
    guest = res_line = None

    s_list = sbuff = None

    s_list_data, S_list = create_model("S_list", {"gastnr":int, "name":string, "zinr":string, "bdate":date, "resstat":string, "abreise":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bday_available, s_list_data, lvcarea, guest, res_line
        nonlocal pvilanguage


        nonlocal s_list, sbuff
        nonlocal s_list_data

        return {"bday_available": bday_available, "s-list": s_list_data}

    def create_list():

        nonlocal bday_available, s_list_data, lvcarea, guest, res_line
        nonlocal pvilanguage


        nonlocal s_list, sbuff
        nonlocal s_list_data


        Sbuff = S_list
        sbuff_data = s_list_data

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        for res_line.name, res_line.zinr, res_line.abreise, res_line._recid, guest.gastnr, guest.geburtdatum1, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.abreise, Res_line._recid, Guest.gastnr, Guest.geburtdatum1, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (((get_month(Guest.geburtdatum1) == get_month(get_current_date())) & (get_day(Guest.geburtdatum1) == get_day(get_current_date()))) | ((get_month(Guest.geburtdatum1) == get_month(get_current_date())) & (get_day(Guest.geburtdatum1) == (get_day(get_current_date())) + 1)))).filter(
                 (Res_line.active_flag == 0) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 11)) & (Res_line.ankunft == get_current_date())).order_by(Guest.name, Res_line.zinr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff.gastnr == guest.gastnr), first=True)

            if not sbuff:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.gastnr = guest.gastnr
                s_list.name = res_line.name
                s_list.zinr = res_line.zinr
                s_list.bdate = date_mdy(get_month(guest.geburtdatum1) , get_day(guest.geburtdatum1) , get_year(guest.geburtdatum1))
                s_list.resstat = translateExtended ("Arrival", lvcarea, "")
                s_list.abreise = res_line.abreise


                bday_available = True

        res_line_obj_list = {}
        res_line = Res_line()
        guest = Guest()
        for res_line.name, res_line.zinr, res_line.abreise, res_line._recid, guest.gastnr, guest.geburtdatum1, guest._recid in db_session.query(Res_line.name, Res_line.zinr, Res_line.abreise, Res_line._recid, Guest.gastnr, Guest.geburtdatum1, Guest._recid).join(Guest,(Guest.gastnr == Res_line.gastnrmember) & (((get_month(Guest.geburtdatum1) == get_month(get_current_date())) & (get_day(Guest.geburtdatum1) == get_day(get_current_date()))) | ((get_month(Guest.geburtdatum1) == get_month(get_current_date())) & (get_day(Guest.geburtdatum1) == (get_day(get_current_date())) + 1)))).filter(
                 (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Guest.name, Res_line.zinr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff.gastnr == guest.gastnr and sbuff.resstat.lower()  == ("Inhouse").lower()), first=True)

            if not sbuff:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.gastnr = guest.gastnr
                s_list.name = res_line.name
                s_list.zinr = res_line.zinr
                s_list.bdate = date_mdy(get_month(guest.geburtdatum1) , get_day(guest.geburtdatum1) , get_year(guest.geburtdatum1))
                s_list.resstat = translateExtended ("Inhouse", lvcarea, "")
                s_list.abreise = res_line.abreise


                bday_available = True

    create_list()

    return generate_output()