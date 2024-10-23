from functions.additional_functions import *
import decimal
from models import Bk_veran, Akt_kont, Guest, Queasy

def bqtlist_contcbl():
    t_out_list = []
    bk_veran = akt_kont = guest = queasy = None

    t_out = None

    t_out_list, T_out = create_model("T_out", {"gastnr":int, "company":str, "anrede":str, "vorname":str, "name":str, "abteilung":str, "religion":str, "geburtdatum1":date, "telefon":str, "durchwahl":str, "email_adr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_out_list, bk_veran, akt_kont, guest, queasy


        nonlocal t_out
        nonlocal t_out_list
        return {"t-out": t_out_list}


    t_out_list.clear()

    guest_obj_list = []
    for guest, bk_veran, akt_kont in db_session.query(Guest, Bk_veran, Akt_kont).join(Bk_veran,(Bk_veran.gastnr == Guest.gastnr)).join(Akt_kont,(Guest.gastnr == Akt_kont.gastnr)).filter(
             (Guest.karteityp == 1)).order_by(Guest._recid).all():
        if guest._recid in guest_obj_list:
            continue
        else:
            guest_obj_list.append(guest._recid)

        if guest:
            t_out = T_out()
            t_out_list.append(t_out)

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