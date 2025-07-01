#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr, Akt_code, Akt_kont, Guest, Htparam

def prepare_mk_aktlinebl(aktnr:int, inp_gastnr:int):

    prepare_cache ([Akt_kont, Guest, Htparam])

    lname = ""
    guest_gastnr = 0
    p_400 = ""
    p_405 = ""
    p_406 = ""
    p_407 = ""
    t_akthdr_list = []
    t_akt_code_list = []
    akthdr = akt_code = akt_kont = guest = htparam = None

    t_akthdr = t_akt_code = None

    t_akthdr_list, T_akthdr = create_model_like(Akthdr, {"akt_code_bezeich":string, "akt_kont_anrede":string, "akt_kont_name":string, "akt_kont_vorname":string})
    t_akt_code_list, T_akt_code = create_model_like(Akt_code)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, guest_gastnr, p_400, p_405, p_406, p_407, t_akthdr_list, t_akt_code_list, akthdr, akt_code, akt_kont, guest, htparam
        nonlocal aktnr, inp_gastnr


        nonlocal t_akthdr, t_akt_code
        nonlocal t_akthdr_list, t_akt_code_list

        return {"lname": lname, "guest_gastnr": guest_gastnr, "p_400": p_400, "p_405": p_405, "p_406": p_406, "p_407": p_407, "t-akthdr": t_akthdr_list, "t-akt-code": t_akt_code_list}


    if aktnr != 0:

        akthdr_obj_list = {}
        for akthdr, akt_code, akt_kont in db_session.query(Akthdr, Akt_code, Akt_kont).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                 (Akthdr.aktnr == aktnr)).order_by(Akthdr._recid).all():
            if akthdr_obj_list.get(akthdr._recid):
                continue
            else:
                akthdr_obj_list[akthdr._recid] = True


            t_akthdr = T_akthdr()
            t_akthdr_list.append(t_akthdr)

            buffer_copy(akthdr, t_akthdr)
            akt_code_bezeich = akt_code.bezeich
            akt_kont_anrede = akt_kont.anrede
            akt_kont_name = akt_kont.name
            akt_kont_vorname = akt_kont.vorname

    if inp_gastnr > 0:

        guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})
        lname = guest.name + ", " + guest.anredefirma
        guest_gastnr = guest.gastnr

    for akt_code in db_session.query(Akt_code).filter(
             (Akt_code.aktiongrup == 1)).order_by(Akt_code.aktionscode).all():
        t_akt_code = T_akt_code()
        t_akt_code_list.append(t_akt_code)

        buffer_copy(akt_code, t_akt_code)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 400)]})
    p_400 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 405)]})
    p_405 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 406)]})
    p_406 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 407)]})
    p_407 = htparam.fchar

    return generate_output()