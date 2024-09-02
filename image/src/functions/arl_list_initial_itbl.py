from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Htparam, Bediener, Guest, Paramtext

def arl_list_initial_itbl(inp_resname:str, user_init:str):
    ext_char = ""
    long_stay = 0
    ci_date = None
    fdate1 = None
    fdate2 = None
    lname = ""
    show_rate = False
    bediener_permissions = ""
    feldtype_336 = 0
    flogical_336 = False
    finteger_337 = 0
    finteger_338 = 0
    flogical_1111 = False
    p_297 = 0
    p_437 = False
    l_param472 = False
    vipnr1 = 0
    vipnr2 = 0
    vipnr3 = 0
    vipnr4 = 0
    vipnr5 = 0
    vipnr6 = 0
    vipnr7 = 0
    vipnr8 = 0
    vipnr9 = 0
    t_guest_list = []
    setup_list_list = []
    htparam = bediener = guest = paramtext = None

    setup_list = t_guest = None

    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})
    t_guest_list, T_guest = create_model("T_guest", {"firmen_nr":int, "steuernr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ext_char, long_stay, ci_date, fdate1, fdate2, lname, show_rate, bediener_permissions, feldtype_336, flogical_336, finteger_337, finteger_338, flogical_1111, p_297, p_437, l_param472, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, t_guest_list, setup_list_list, htparam, bediener, guest, paramtext


        nonlocal setup_list, t_guest
        nonlocal setup_list_list, t_guest_list
        return {"ext_char": ext_char, "long_stay": long_stay, "ci_date": ci_date, "fdate1": fdate1, "fdate2": fdate2, "lname": lname, "show_rate": show_rate, "bediener_permissions": bediener_permissions, "feldtype_336": feldtype_336, "flogical_336": flogical_336, "finteger_337": finteger_337, "finteger_338": finteger_338, "flogical_1111": flogical_1111, "p_297": p_297, "p_437": p_437, "l_param472": l_param472, "vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9, "t-guest": t_guest_list, "setup-list": setup_list_list}

    def bed_setup():

        nonlocal ext_char, long_stay, ci_date, fdate1, fdate2, lname, show_rate, bediener_permissions, feldtype_336, flogical_336, finteger_337, finteger_338, flogical_1111, p_297, p_437, l_param472, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, t_guest_list, setup_list_list, htparam, bediener, guest, paramtext


        nonlocal setup_list, t_guest
        nonlocal setup_list_list, t_guest_list

        it_exist:bool = False
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
            setup_list = Setup_list()
            setup_list_list.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199
            setup_list.char = substring(paramtext.notes, 0, 1)
            it_exist = True

    p_297 = get_output(htpint(297))
    p_437 = get_output(htplogic(437))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 472)).first()

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        l_param472 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 148)).first()
    ext_char = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 139)).first()
    long_stay = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    fdate1 = ci_date
    fdate2 = ci_date
    lname = inp_resname

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()
    vipnr1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()
    vipnr2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()
    vipnr3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()
    vipnr4 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()
    vipnr5 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()
    vipnr6 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()
    vipnr7 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()
    vipnr8 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()
    vipnr9 = htparam.finteger

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    if substring(bediener.permissions, 34, 1) != "0":
        show_rate = True
    bediener_permissions = bediener.permissions

    for guest in db_session.query(Guest).filter(
            (Guest.karteityp >= 1) &  (Guest.gastnr > 0) &  (Guest.firmen_nr > 0) &  (Guest.steuernr != "")).all():
        t_guest = T_guest()
        t_guest_list.append(t_guest)

        t_guest.firmen_nr = guest.firmen_nr
        t_guest.steuernr = guest.steuernr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 336)).first()
    feldtype_336 = htparam.feldtyp
    flogical_336 = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 337)).first()
    finteger_337 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 338)).first()
    finteger_338 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1111)).first()
    flogical_1111 = htparam.flogical
    bed_setup()

    return generate_output()