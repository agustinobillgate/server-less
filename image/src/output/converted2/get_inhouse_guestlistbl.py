#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Guest, Nation

def get_inhouse_guestlistbl():

    prepare_cache ([Res_line, Guest, Nation])

    guest_list_list = []
    i:int = 0
    i_counter:int = 0
    str:string = ""
    ci_date:date = None
    active_flag:int = 1
    res_line = guest = nation = None

    guest_list = None

    guest_list_list, Guest_list = create_model("Guest_list", {"resnr":int, "reslinnr":int, "roomnumber":string, "checkindate":date, "checkoutdate":date, "guest_nr":int, "guest_lastname":string, "guest_firstname":string, "guest_title":string, "guest_nation":string, "guest_country":string, "guest_region":string, "guest_mobile":string, "guest_email":string, "guest_bemerk":string, "guest_birthday":date, "recid_resline":int, "wifi_password":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_list_list, i, i_counter, str, ci_date, active_flag, res_line, guest, nation


        nonlocal guest_list
        nonlocal guest_list_list

        return {"guest-list": guest_list_list}


    ci_date = get_output(htpdate(87))

    for res_line in db_session.query(Res_line).filter(
             (Res_line.active_flag == active_flag) & (Res_line.l_zuordnung[inc_value(2)] == 0) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Res_line._recid).all():

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        guest_list = Guest_list()
        guest_list_list.append(guest_list)

        guest_list.resnr = res_line.resnr
        guest_list.reslinnr = res_line.reslinnr
        guest_list.roomnumber = res_line.zinr
        guest_list.checkindate = res_line.ankunft
        guest_list.checkoutdate = res_line.abreise
        guest_list.guest_nr = guest.gastnr
        guest_list.guest_lastname = guest.name
        guest_list.guest_firstname = guest.vorname1
        guest_list.guest_title = guest.anrede1
        guest_list.guest_mobile = guest.mobil_telefon
        guest_list.guest_email = guest.email_adr
        guest_list.guest_bemerk = guest.bemerkung
        guest_list.guest_birthday = guest.geburtdatum1
        guest_list.recid_resline = res_line._recid

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

        if nation:
            guest_list.guest_nation = entry(0, nation.bezeich, ";")

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.land)]})

        if nation:
            guest_list.guest_country = entry(0, nation.bezeich, ";")

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation2)]})

        if nation:
            guest_list.guest_region = entry(0, nation.bezeich, ";")

    return generate_output()