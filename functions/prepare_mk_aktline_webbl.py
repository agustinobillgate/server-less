#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr, Akt_code, Akt_line, Akt_kont, Guest, Htparam

def prepare_mk_aktline_webbl(aktnr:int, inp_gastnr:int, user_init:string):

    prepare_cache ([Akt_kont, Guest, Htparam])

    lname = ""
    guest_gastnr = 0
    p_400 = ""
    p_405 = ""
    p_406 = ""
    p_407 = ""
    zeit = ""
    dauer = ""
    t_akthdr_data = []
    t_akt_code_data = []
    akt_line1_data = []
    akthdr = akt_code = akt_line = akt_kont = guest = htparam = None

    t_akthdr = t_akt_code = akt_line1 = None

    t_akthdr_data, T_akthdr = create_model_like(Akthdr, {"akt_code_bezeich":string, "akt_kont_anrede":string, "akt_kont_name":string, "akt_kont_vorname":string})
    t_akt_code_data, T_akt_code = create_model_like(Akt_code)
    akt_line1_data, Akt_line1 = create_model_like(Akt_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, guest_gastnr, p_400, p_405, p_406, p_407, zeit, dauer, t_akthdr_data, t_akt_code_data, akt_line1_data, akthdr, akt_code, akt_line, akt_kont, guest, htparam
        nonlocal aktnr, inp_gastnr, user_init


        nonlocal t_akthdr, t_akt_code, akt_line1
        nonlocal t_akthdr_data, t_akt_code_data, akt_line1_data

        return {"lname": lname, "guest_gastnr": guest_gastnr, "p_400": p_400, "p_405": p_405, "p_406": p_406, "p_407": p_407, "zeit": zeit, "dauer": dauer, "t-akthdr": t_akthdr_data, "t-akt-code": t_akt_code_data, "akt-line1": akt_line1_data}

    if aktnr != 0:

        akthdr_obj_list = {}
        for akthdr, akt_code, akt_kont in db_session.query(Akthdr, Akt_code, Akt_kont).join(Akt_code,(Akt_code.aktiongrup == 2) & (Akt_code.aktionscode == Akthdr.stufe)).join(Akt_kont,(Akt_kont.gastnr == Akthdr.gastnr) & (Akt_kont.kontakt_nr == Akthdr.kontakt_nr)).filter(
                 (Akthdr.aktnr == aktnr)).order_by(Akthdr._recid).all():
            if akthdr_obj_list.get(akthdr._recid):
                continue
            else:
                akthdr_obj_list[akthdr._recid] = True


            t_akthdr = T_akthdr()
            t_akthdr_data.append(t_akthdr)

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
        t_akt_code_data.append(t_akt_code)

        buffer_copy(akt_code, t_akt_code)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 400)]})
    p_400 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 405)]})
    p_405 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 406)]})
    p_406 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 407)]})
    p_407 = htparam.fchar
    akt_line1 = Akt_line1()
    akt_line1_data.append(akt_line1)


    if aktnr != 0:

        for t_akthdr in query(t_akthdr_data):
            akt_line1.regard = "Follow up on the " + t_akthdr.bezeich +\
                    " opportunity, " + akt_code_bezeich + " stage"


            akt_line1.kontakt = akt_kont_name + ", " + akt_kont_vorname +\
                    " " + akt_kont_anrede


    akt_line1.aktnr = aktnr
    akt_line1.userinit = user_init
    akt_line1.datum = get_current_date()
    zeit = substring(to_string(get_current_time_in_seconds(), "HH:MM") , 0, 2) +\
            substring(to_string(get_current_time_in_seconds(), "HH:MM") , 3, 2)
    akt_line1.zeit = to_int(substring(zeit, 0, 2)) * 3600 +\
            to_int(substring(zeit, 2, 2)) * 60
    dauer = zeit
    akt_line1.dauer = akt_line1.zeit

    if inp_gastnr > 0:
        akt_line1.gastnr = inp_gastnr


        akt_line1.gastnr = guest_gastnr

    return generate_output()