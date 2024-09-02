from functions.additional_functions import *
import decimal
from models import Akt_kont, Guest, Htparam, Queasy

def prepare_gcf0_contactbl(gastnr:int):
    f_title = ""
    main_kont = ""
    p_bezeich = ""
    maincontact = ""
    fname_flag = False
    t_akt_kont_list = []
    akt_kont1_list = []
    t_queasy13_list = []
    akt_kont = guest = htparam = queasy = None

    aktkont_list = akt_kont1 = t_akt_kont = t_queasy13 = None

    aktkont_list_list, Aktkont_list = create_model_like(Akt_kont, {"nat":str, "email":str})
    akt_kont1_list, Akt_kont1 = create_model("Akt_kont1", {"gastnr":int, "name":str, "vorname":str, "anrede":str, "hauptkontakt":bool})
    t_akt_kont_list, T_akt_kont = create_model_like(Akt_kont, {"p_bezeich":str, "rec_id":int})
    t_queasy13_list, T_queasy13 = create_model("T_queasy13", {"number1":int, "char1":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_title, main_kont, p_bezeich, maincontact, fname_flag, t_akt_kont_list, akt_kont1_list, t_queasy13_list, akt_kont, guest, htparam, queasy


        nonlocal aktkont_list, akt_kont1, t_akt_kont, t_queasy13
        nonlocal aktkont_list_list, akt_kont1_list, t_akt_kont_list, t_queasy13_list
        return {"f_title": f_title, "main_kont": main_kont, "p_bezeich": p_bezeich, "maincontact": maincontact, "fname_flag": fname_flag, "t-akt-kont": t_akt_kont_list, "akt-kont1": akt_kont1_list, "t-queasy13": t_queasy13_list}


    guest = db_session.query(Guest).filter((Guest.gastnr == gastnr)).first()
    if guest:
        f_title = f_title + guest.name + ", " + guest.vorname1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 939)).first()
    if htparam:
        fname_flag = htparam.flogical
    
    aktkont_list = Aktkont_list()
    aktkont_list_list.append(aktkont_list)


    akt_kont = db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == gastnr) &  (Akt_kont.hauptkontakt)).first()

    if akt_kont:
        main_kont = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 13) &  (Queasy.number1 == akt_kont.pers_bez)).first()

        if queasy:
            p_bezeich = queasy.char1
        else:
            p_bezeich = ""
    maincontact = main_kont

    for akt_kont in db_session.query(Akt_kont).filter(
            (Akt_kont.gastnr == gastnr)).all():
        t_akt_kont = T_akt_kont()
        t_akt_kont_list.append(t_akt_kont)

        buffer_copy(akt_kont, t_akt_kont)
        t_akt_kont.rec_id = akt_kont._recid

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 13) &  (Queasy.number1 == akt_kont.pers_bez)).first()

        if queasy:
            t_akt_kont.p_bezeich = queasy.char1
        else:
            t_akt_kont.p_bezeich = ""
        akt_kont1 = Akt_kont1()
        akt_kont1_list.append(akt_kont1)

        akt_kont1.hauptkontakt = akt_kont.hauptkontakt

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 13)).all():
        t_queasy13 = T_queasy13()
        t_queasy13_list.append(t_queasy13)

        t_queasy13.number1 = queasy.number1
        t_queasy13.char1 = queasy.char1

    return generate_output()