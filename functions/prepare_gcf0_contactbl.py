#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_kont, Guest, Htparam, Queasy

def prepare_gcf0_contactbl(gastnr:int):

    prepare_cache ([Guest, Htparam, Queasy])

    f_title = ""
    main_kont = ""
    p_bezeich = ""
    maincontact = ""
    fname_flag = False
    t_akt_kont_data = []
    akt_kont1_data = []
    t_queasy13_data = []
    akt_kont = guest = htparam = queasy = None

    aktkont_list = akt_kont1 = t_akt_kont = t_queasy13 = None

    aktkont_list_data, Aktkont_list = create_model_like(Akt_kont, {"nat":string, "email":string})
    akt_kont1_data, Akt_kont1 = create_model("Akt_kont1", {"gastnr":int, "name":string, "vorname":string, "anrede":string, "hauptkontakt":bool})
    t_akt_kont_data, T_akt_kont = create_model_like(Akt_kont, {"p_bezeich":string, "rec_id":int})
    t_queasy13_data, T_queasy13 = create_model("T_queasy13", {"number1":int, "char1":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_title, main_kont, p_bezeich, maincontact, fname_flag, t_akt_kont_data, akt_kont1_data, t_queasy13_data, akt_kont, guest, htparam, queasy
        nonlocal gastnr


        nonlocal aktkont_list, akt_kont1, t_akt_kont, t_queasy13
        nonlocal aktkont_list_data, akt_kont1_data, t_akt_kont_data, t_queasy13_data

        return {"f_title": f_title, "main_kont": main_kont, "p_bezeich": p_bezeich, "maincontact": maincontact, "fname_flag": fname_flag, "t-akt-kont": t_akt_kont_data, "akt-kont1": akt_kont1_data, "t-queasy13": t_queasy13_data}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    f_title = f_title + guest.name + ", " + guest.vorname1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 939)]})
    fname_flag = htparam.flogical
    aktkont_list = Aktkont_list()
    aktkont_list_data.append(aktkont_list)


    akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, gastnr)],"hauptkontakt": [(eq, True)]})

    if akt_kont:
        main_kont = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

        queasy = get_cache (Queasy, {"key": [(eq, 13)],"number1": [(eq, akt_kont.pers_bez)]})

        if queasy:
            p_bezeich = queasy.char1
        else:
            p_bezeich = ""
    maincontact = main_kont

    for akt_kont in db_session.query(Akt_kont).filter(
             (Akt_kont.gastnr == gastnr)).order_by(Akt_kont.name).all():
        t_akt_kont = T_akt_kont()
        t_akt_kont_data.append(t_akt_kont)

        buffer_copy(akt_kont, t_akt_kont)
        t_akt_kont.rec_id = akt_kont._recid

        queasy = get_cache (Queasy, {"key": [(eq, 13)],"number1": [(eq, akt_kont.pers_bez)]})

        if queasy:
            t_akt_kont.p_bezeich = queasy.char1
        else:
            t_akt_kont.p_bezeich = ""
        akt_kont1 = Akt_kont1()
        akt_kont1_data.append(akt_kont1)

        akt_kont1.hauptkontakt = akt_kont.hauptkontakt

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 13)).order_by(Queasy._recid).all():
        t_queasy13 = T_queasy13()
        t_queasy13_data.append(t_queasy13)

        t_queasy13.number1 = queasy.number1
        t_queasy13.char1 = queasy.char1

    return generate_output()