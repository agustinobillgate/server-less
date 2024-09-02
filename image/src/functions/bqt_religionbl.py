from functions.additional_functions import *
import decimal
from models import Bk_veran, Guest, Akt_kont, Queasy

def bqt_religionbl(int:int, from_mm:int, from_dd:int, to_mm:int, to_dd:int):
    religion_list = []
    from_date:int = 0
    to_date:int = 0
    count:int = 0
    stopped:bool = False
    bk_veran = guest = akt_kont = queasy = None

    religion = None

    religion_list, Religion = create_model("Religion", {"gastnr":int, "company":str, "name":str, "pers_bez":str, "telephone":str, "email":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal religion_list, from_date, to_date, count, stopped, bk_veran, guest, akt_kont, queasy


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

        guest_obj_list = []
        for guest, bk_veran in db_session.query(Guest, Bk_veran).join(Bk_veran,(Bk_veran.gastnr == Guest.gastnr)).filter(
                (Guest.karteityp == 1)).all():
            if guest._recid in guest_obj_list:
                continue
            else:
                guest_obj_list.append(guest._recid)

            for akt_kont in db_session.query(Akt_kont).filter(
                        (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.pers_bez == int)).all():
                religion = Religion()
                religion_list.append(religion)

                religion.gastnr = guest.gastnr
                religion.company = guest.name
                religion.name = akt_kont.name + ", " + akt_kont.vorname +\
                        " " + akt_kont.anrede
                religion.telephone = akt_kont.telefon
                religion.email = akt_kont.email_adr

                queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 149) &  (Queasy.char1 == to_string(akt_kont.pers_bez))).first()

                if queasy:
                    religion.pers_bez = queasy.char3
                ELSE
    else:

        guest_obj_list = []
        for guest, bk_veran in db_session.query(Guest, Bk_veran).join(Bk_veran,(Bk_veran.gastnr == Guest.gastnr)).filter(
                (Guest.karteityp == 1)).all():
            if guest._recid in guest_obj_list:
                continue
            else:
                guest_obj_list.append(guest._recid)

            for akt_kont in db_session.query(Akt_kont).filter(
                        (Akt_kont.gastnr == guest.gastnr)).all():
                religion = Religion()
                religion_list.append(religion)

                religion.gastnr = guest.gastnr
                religion.company = guest.name
                religion.name = akt_kont.name + ", " + akt_kont.vorname +\
                        " " + akt_kont.anrede
                religion.telephone = akt_kont.telefon
                religion.email = akt_kont.email_adr

                queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 149) &  (Queasy.char1 == to_string(akt_kont.pers_bez))).first()

                if queasy:
                    religion.pers_bez = queasy.char3
                ELSE

    return generate_output()