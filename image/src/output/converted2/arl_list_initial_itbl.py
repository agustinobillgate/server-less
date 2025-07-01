#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.htplogic import htplogic
from models import Htparam, Bediener, Guest, Paramtext

def arl_list_initial_itbl(inp_resname:string, user_init:string):

    prepare_cache ([Htparam, Bediener, Paramtext])

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
    vipnr1 = 999999999
    vipnr2 = 999999999
    vipnr3 = 999999999
    vipnr4 = 999999999
    vipnr5 = 999999999
    vipnr6 = 999999999
    vipnr7 = 999999999
    vipnr8 = 999999999
    vipnr9 = 999999999
    t_guest_list = []
    setup_list_list = []
    htparam = bediener = guest = paramtext = None

    setup_list = t_guest = None

    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":string})
    t_guest_list, T_guest = create_model("T_guest", {"firmen_nr":int, "steuernr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ext_char, long_stay, ci_date, fdate1, fdate2, lname, show_rate, bediener_permissions, feldtype_336, flogical_336, finteger_337, finteger_338, flogical_1111, p_297, p_437, l_param472, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, t_guest_list, setup_list_list, htparam, bediener, guest, paramtext
        nonlocal inp_resname, user_init


        nonlocal setup_list, t_guest
        nonlocal setup_list_list, t_guest_list

        return {"ext_char": ext_char, "long_stay": long_stay, "ci_date": ci_date, "fdate1": fdate1, "fdate2": fdate2, "lname": lname, "show_rate": show_rate, "bediener_permissions": bediener_permissions, "feldtype_336": feldtype_336, "flogical_336": flogical_336, "finteger_337": finteger_337, "finteger_338": finteger_338, "flogical_1111": flogical_1111, "p_297": p_297, "p_437": p_437, "l_param472": l_param472, "vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9, "t-guest": t_guest_list, "setup-list": setup_list_list}

    def bed_setup():

        nonlocal ext_char, long_stay, ci_date, fdate1, fdate2, lname, show_rate, bediener_permissions, feldtype_336, flogical_336, finteger_337, finteger_338, flogical_1111, p_297, p_437, l_param472, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, t_guest_list, setup_list_list, htparam, bediener, guest, paramtext
        nonlocal inp_resname, user_init


        nonlocal setup_list, t_guest
        nonlocal setup_list_list, t_guest_list

        it_exist:bool = False
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
            setup_list = Setup_list()
            setup_list_list.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199
            setup_list.char = substring(paramtext.notes, 0, 1)
            it_exist = True


    p_297 = get_output(htpint(297))
    p_437 = get_output(htplogic(437))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 472)]})

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        l_param472 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 148)]})
    ext_char = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 139)]})
    long_stay = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    fdate1 = ci_date
    fdate2 = ci_date
    lname = inp_resname

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})
    vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})
    vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})
    vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})
    vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})
    vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})
    vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})
    vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})
    vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})
    vipnr9 = htparam.finteger

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if substring(bediener.permissions, 34, 1) != ("0").lower() :
        show_rate = True
    bediener_permissions = bediener.permissions

    guest = get_cache (Guest, {"karteityp": [(ge, 1)],"gastnr": [(gt, 0)],"firmen_nr": [(gt, 0)],"steuernr": [(ne, "")]})
    while None != guest:
        t_guest = T_guest()
        t_guest_list.append(t_guest)

        t_guest.firmen_nr = guest.firmen_nr
        t_guest.steuernr = guest.steuernr

        curr_recid = guest._recid
        guest = db_session.query(Guest).filter(
                 (Guest.karteityp >= 1) & (Guest.gastnr > 0) & (Guest.firmen_nr > 0) & (Guest.steuernr != "") & (Guest._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 336)]})
    feldtype_336 = htparam.feldtyp
    flogical_336 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 337)]})
    finteger_337 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 338)]})
    finteger_338 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1111)]})
    flogical_1111 = htparam.flogical
    bed_setup()

    return generate_output()