#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Guest, Akt_kont, Queasy

def bqt_religionbl(int:int, from_mm:int, from_dd:int, to_mm:int, to_dd:int):

    prepare_cache ([Guest, Akt_kont, Queasy])

    religion_list = []
    from_date:int = 0
    to_date:int = 0
    count:int = 0
    stopped:bool = False
    bk_veran = guest = akt_kont = queasy = None

    religion = None

    religion_list, Religion = create_model("Religion", {"gastnr":int, "company":string, "name":string, "pers_bez":string, "telephone":string, "email":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal religion_list, from_date, to_date, count, stopped, bk_veran, guest, akt_kont, queasy
        nonlocal int, from_mm, from_dd, to_mm, to_dd


        nonlocal religion
        nonlocal religion_list

        return {"religion": religion_list}


    from_date = from_mm * 100 + from_dd

    if from_mm <= to_mm:
        to_date = to_mm * 100 + to_dd
    else:
        to_date = (to_mm + 12) * 100 + to_dd
    religion_list.clear()

    if int != 0:

        guest_obj_list = {}
        for guest, bk_veran in db_session.query(Guest, Bk_veran).join(Bk_veran,(Bk_veran.gastnr == Guest.gastnr)).filter(
                 (Guest.karteityp == 1)).order_by(Guest._recid).all():
            if guest_obj_list.get(guest._recid):
                continue
            else:
                guest_obj_list[guest._recid] = True

            for akt_kont in db_session.query(Akt_kont).filter(
                         (Akt_kont.gastnr == guest.gastnr) & (Akt_kont.pers_bez == int)).order_by(Akt_kont._recid).all():
                religion = Religion()
                religion_list.append(religion)

                religion.gastnr = guest.gastnr
                religion.company = guest.name
                religion.name = akt_kont.name + ", " + akt_kont.vorname +\
                        " " + akt_kont.anrede
                religion.telephone = akt_kont.telefon
                religion.email = akt_kont.email_adr

                queasy = get_cache (Queasy, {"key": [(eq, 149)],"char1": [(eq, to_string(akt_kont.pers_bez))]})

                if queasy:
                    religion.pers_bez = queasy.char3
    else:

        guest_obj_list = {}
        for guest, bk_veran in db_session.query(Guest, Bk_veran).join(Bk_veran,(Bk_veran.gastnr == Guest.gastnr)).filter(
                 (Guest.karteityp == 1)).order_by(Guest._recid).all():
            if guest_obj_list.get(guest._recid):
                continue
            else:
                guest_obj_list[guest._recid] = True

            for akt_kont in db_session.query(Akt_kont).filter(
                         (Akt_kont.gastnr == guest.gastnr)).order_by(Akt_kont._recid).all():
                religion = Religion()
                religion_list.append(religion)

                religion.gastnr = guest.gastnr
                religion.company = guest.name
                religion.name = akt_kont.name + ", " + akt_kont.vorname +\
                        " " + akt_kont.anrede
                religion.telephone = akt_kont.telefon
                religion.email = akt_kont.email_adr

                queasy = get_cache (Queasy, {"key": [(eq, 149)],"char1": [(eq, to_string(akt_kont.pers_bez))]})

                if queasy:
                    religion.pers_bez = queasy.char3

    return generate_output()