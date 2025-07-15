#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Akt_kont, Guest, Queasy

def bqtlist_contcbl():

    prepare_cache ([Akt_kont, Guest, Queasy])

    t_out_data = []
    bk_veran = akt_kont = guest = queasy = None

    t_out = None

    t_out_data, T_out = create_model("T_out", {"gastnr":int, "company":string, "anrede":string, "vorname":string, "name":string, "abteilung":string, "religion":string, "geburtdatum1":date, "telefon":string, "durchwahl":string, "email_adr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_out_data, bk_veran, akt_kont, guest, queasy


        nonlocal t_out
        nonlocal t_out_data

        return {"t-out": t_out_data}


    t_out_data.clear()

    guest_obj_list = {}
    for guest, bk_veran, akt_kont in db_session.query(Guest, Bk_veran, Akt_kont).join(Bk_veran,(Bk_veran.gastnr == Guest.gastnr)).join(Akt_kont,(Guest.gastnr == Akt_kont.gastnr)).filter(
             (Guest.karteityp == 1)).order_by(Guest._recid).all():
        if guest_obj_list.get(guest._recid):
            continue
        else:
            guest_obj_list[guest._recid] = True

        if guest:
            t_out = T_out()
            t_out_data.append(t_out)

            t_out.gastnr = akt_kont.gastnr
            t_out.company = guest.name
            t_out.anrede = akt_kont.anrede
            t_out.vorname = akt_kont.vorname
            t_out.name = akt_kont.name
            t_out.abteilung = akt_kont.abteilung
            t_out.geburtdatum1 = akt_kont.geburtdatum1
            t_out.telefon = akt_kont.telefon
            t_out.durchwahl = akt_kont.durchwahl
            t_out.email_adr = akt_kont.email_adr

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 149) & (to_int(Queasy.char1) == akt_kont.pers_bez)).first()

        if queasy:
            t_out.religion = queasy.char3

    return generate_output()