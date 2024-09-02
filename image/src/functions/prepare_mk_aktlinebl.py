from functions.additional_functions import *
import decimal
from models import Akthdr, Akt_code, Akt_kont, Guest, Htparam

def prepare_mk_aktlinebl(aktnr:int, inp_gastnr:int):
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

    t_akthdr_list, T_akthdr = create_model_like(Akthdr, {"akt_code_bezeich":str, "akt_kont_anrede":str, "akt_kont_name":str, "akt_kont_vorname":str})
    t_akt_code_list, T_akt_code = create_model_like(Akt_code)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, guest_gastnr, p_400, p_405, p_406, p_407, t_akthdr_list, t_akt_code_list, akthdr, akt_code, akt_kont, guest, htparam


        nonlocal t_akthdr, t_akt_code
        nonlocal t_akthdr_list, t_akt_code_list
        return {"lname": lname, "guest_gastnr": guest_gastnr, "p_400": p_400, "p_405": p_405, "p_406": p_406, "p_407": p_407, "t-akthdr": t_akthdr_list, "t-akt-code": t_akt_code_list}


    if aktnr != 0:

        akthdr_obj_list = []
        for akthdr, akt_code, akt_kont in db_session.query(Akthdr, Akt_code, Akt_kont).join(Akt_code,(Akt_code.aktiongrup == 2) &  (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) &  (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                (Akthdr.aktnr == aktnr)).all():
            if akthdr._recid in akthdr_obj_list:
                continue
            else:
                akthdr_obj_list.append(akthdr._recid)


            t_akthdr = T_akthdr()
            t_akthdr_list.append(t_akthdr)

            buffer_copy(akthdr, t_akthdr)
            akt_code_bezeich = akt_code.bezeich
            akt_kont_anrede = akt_kont.anrede
            akt_kont_name = akt_kont.name
            akt_kont_vorname = akt_kont.vorname

    if inp_gastnr > 0:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == inp_gastnr)).first()
        lname = guest.name + ", " + guest.anredefirma
        guest_gastnr = guest.gastnr

    for akt_code in db_session.query(Akt_code).filter(
            (Akt_code.aktiongrup == 1)).all():
        t_akt_code = T_akt_code()
        t_akt_code_list.append(t_akt_code)

        buffer_copy(akt_code, t_akt_code)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 400)).first()
    p_400 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 405)).first()
    p_405 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 406)).first()
    p_406 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 407)).first()
    p_407 = htparam.fchar

    return generate_output()