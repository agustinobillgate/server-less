from functions.additional_functions import *
import decimal
from models import Akthdr, Akt_code, Guest, Akt_kont

def prepare_chg_akthdrbl(aktnr:int):
    lname = ""
    namekontakt = ""
    kontakt_nr = 0
    comment = ""
    avail_guest = False
    guest_gastnr = 0
    akthdr1_list = []
    t_akt_code_list = []
    akthdr = akt_code = guest = akt_kont = None

    akthdr1 = t_akt_code = None

    akthdr1_list, Akthdr1 = create_model_like(Akthdr)
    t_akt_code_list, T_akt_code = create_model_like(Akt_code)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, namekontakt, kontakt_nr, comment, avail_guest, guest_gastnr, akthdr1_list, t_akt_code_list, akthdr, akt_code, guest, akt_kont


        nonlocal akthdr1, t_akt_code
        nonlocal akthdr1_list, t_akt_code_list
        return {"lname": lname, "namekontakt": namekontakt, "kontakt_nr": kontakt_nr, "comment": comment, "avail_guest": avail_guest, "guest_gastnr": guest_gastnr, "akthdr1": akthdr1_list, "t-akt-code": t_akt_code_list}

    def create_akthdr():

        nonlocal lname, namekontakt, kontakt_nr, comment, avail_guest, guest_gastnr, akthdr1_list, t_akt_code_list, akthdr, akt_code, guest, akt_kont


        nonlocal akthdr1, t_akt_code
        nonlocal akthdr1_list, t_akt_code_list


        akthdr1 = Akthdr1()
        akthdr1_list.append(akthdr1)

        buffer_copy(akthdr, akthdr1)


    akthdr = db_session.query(Akthdr).filter(
            (Akthdr.aktnr == aktnr)).first()
    create_akthdr()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == akthdr.gastnr)).first()
    lname = guest.name + ", " + guest.anredefirma
    avail_guest = True
    guest_gastnr = guest.gastnr

    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == guest.gastnr) &  (Akt_kont.kontakt_nr == akthdr1.kontakt_nr)).first()

    if akt_kont:
        namekontakt = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        kontakt_nr = akt_kont.kontakt_nr
    comment = akthdr1.bemerk

    for akt_code in db_session.query(Akt_code).all():
        t_akt_code = T_akt_code()
        t_akt_code_list.append(t_akt_code)

        buffer_copy(akt_code, t_akt_code)

    return generate_output()