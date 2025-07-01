#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr, Akt_code, Guest, Akt_kont

def prepare_chg_akthdrbl(aktnr:int):

    prepare_cache ([Guest, Akt_kont])

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
        nonlocal aktnr


        nonlocal akthdr1, t_akt_code
        nonlocal akthdr1_list, t_akt_code_list

        return {"lname": lname, "namekontakt": namekontakt, "kontakt_nr": kontakt_nr, "comment": comment, "avail_guest": avail_guest, "guest_gastnr": guest_gastnr, "akthdr1": akthdr1_list, "t-akt-code": t_akt_code_list}

    def create_akthdr():

        nonlocal lname, namekontakt, kontakt_nr, comment, avail_guest, guest_gastnr, akthdr1_list, t_akt_code_list, akthdr, akt_code, guest, akt_kont
        nonlocal aktnr


        nonlocal akthdr1, t_akt_code
        nonlocal akthdr1_list, t_akt_code_list


        akthdr1 = Akthdr1()
        akthdr1_list.append(akthdr1)

        buffer_copy(akthdr, akthdr1)

    akthdr = get_cache (Akthdr, {"aktnr": [(eq, aktnr)]})

    if akthdr:
        create_akthdr()

        guest = get_cache (Guest, {"gastnr": [(eq, akthdr.gastnr)]})

        if guest:
            lname = guest.name + ", " + guest.anredefirma
            avail_guest = True
            guest_gastnr = guest.gastnr

            akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)],"kontakt_nr": [(eq, akthdr.kontakt_nr)]})

            if akt_kont:
                namekontakt = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
                kontakt_nr = akt_kont.kontakt_nr
            comment = akthdr.bemerk

    for akt_code in db_session.query(Akt_code).order_by(Akt_code._recid).all():
        t_akt_code = T_akt_code()
        t_akt_code_list.append(t_akt_code)

        buffer_copy(akt_code, t_akt_code)

    return generate_output()