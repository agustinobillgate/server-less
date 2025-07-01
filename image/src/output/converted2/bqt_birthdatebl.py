#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran, Akt_kont, Guest

def bqt_birthdatebl(from_mm:int, from_dd:int, to_mm:int, to_dd:int):

    prepare_cache ([Akt_kont, Guest])

    birth_list_list = []
    from_date:int = 0
    to_date:int = 0
    count:int = 0
    stopped:bool = False
    bk_veran = akt_kont = guest = None

    birth_list = None

    birth_list_list, Birth_list = create_model("Birth_list", {"company":string, "name":string, "geburtdatum":date, "geburt_ort1":string, "telephone":string, "email":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal birth_list_list, from_date, to_date, count, stopped, bk_veran, akt_kont, guest
        nonlocal from_mm, from_dd, to_mm, to_dd


        nonlocal birth_list
        nonlocal birth_list_list

        return {"birth-list": birth_list_list}


    from_date = from_mm * 100 + from_dd

    if from_mm <= to_mm:
        to_date = to_mm * 100 + to_dd
    else:
        to_date = (to_mm + 12) * 100 + to_dd
    birth_list_list.clear()

    guest_obj_list = {}
    for guest, bk_veran, akt_kont in db_session.query(Guest, Bk_veran, Akt_kont).join(Bk_veran,(Bk_veran.gastnr == Guest.gastnr)).join(Akt_kont,(Akt_kont.gastnr == Guest.gastnr)).filter(
             (Guest.karteityp == 1)).order_by(Guest._recid).all():
        if guest_obj_list.get(guest._recid):
            continue
        else:
            guest_obj_list[guest._recid] = True

        if (get_month(akt_kont.geburtdatum1) * 100 + get_day(akt_kont.geburtdatum1)) >= from_date and (get_month(akt_kont.geburtdatum1) * 100 + get_day(akt_kont.geburtdatum1)) <= to_date:
            birth_list = Birth_list()
            birth_list_list.append(birth_list)

            birth_list.company = guest.name
            birth_list.name = akt_kont.name + ", " + akt_kont.vorname +\
                    " " + akt_kont.anrede
            birth_list.geburtdatum = akt_kont.geburtdatum1
            birth_list.geburt_ort1 = akt_kont.geburt_ort1
            birth_list.telephone = akt_kont.telefon
            birth_list.email = akt_kont.email_adr

    return generate_output()