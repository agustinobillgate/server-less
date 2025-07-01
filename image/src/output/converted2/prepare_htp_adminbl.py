#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Paramtext

def prepare_htp_adminbl():

    prepare_cache ([Paramtext])

    rest_flag = False
    s_list_list = []
    htp_list = []
    htgrp_list = []
    htp_list_list = []
    fl_assign:bool = False
    gnr:int = 31
    anz_htp:int = 70
    arr:List[int] = [124, 126, 128, 129, 130, 131, 132, 133, 136, 137, 138, 0, 140, 141, 142, 143, 144, 146, 147, 148, 149, 150, 151, 152, 153, 161, 158, 159, 125, 160, 162]
    htp_arr:List[int] = [318, 84, 87, 592, 117, 119, 120, 121, 124, 1001, 47, 97, 137, 139, 146, 159, 166, 218, 226, 250, 391, 559, 677, 1108, 48, 125, 130, 131, 145, 149, 150, 151, 154, 156, 157, 158, 198, 227, 228, 229, 241, 255, 264, 270, 478, 295, 162, 233, 260, 265, 302, 113, 114, 115, 76, 434, 435, 440, 441, 442, 587, 1116, 2313, 2315, 273, 143, 144, 377, 0, 0]
    i:int = 0
    htparam = paramtext = None

    s_list = htp_list = htgrp = htp = None

    s_list_list, S_list = create_model("S_list", {"nr":int})
    htp_list_list, Htp_list = create_model_like(Htparam)
    htgrp_list, Htgrp = create_model("Htgrp", {"number":int, "bezeich":string})
    htp_list, Htp = create_model("Htp", {"reihenfolge":int, "number":int, "bezeich":string, "typ":int, "logv":bool, "lupdate":date, "note":string, "wert":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, i, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list

        return {"rest_flag": rest_flag, "s-list": s_list_list, "htp": htp_list, "htgrp": htgrp_list, "htp-list": htp_list_list}

    def create_htplist():

        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, i, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 40)).order_by(Htparam._recid).all():
            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            buffer_copy(htparam, htp_list)


    def create_htgrp():

        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list

        i:int = 0

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 161)]})

        if not paramtext:
            paramtext = Paramtext()
            db_session.add(paramtext)

            paramtext.txtnr = 161
            paramtext.number = 35
            paramtext.ptexte = "Centralized Mgmt Reporting System"


        for i in range(1,gnr + 1) :

            if arr[i - 1] != 0:

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, arr[i - 1])]})

                if paramtext:
                    htgrp = Htgrp()
                    htgrp_list.append(htgrp)

                    htgrp.number = paramtext.number
                    htgrp.bezeich = paramtext.ptexte


    def create_htp(i:int):

        nonlocal rest_flag, s_list_list, htp_list, htgrp_list, htp_list_list, fl_assign, gnr, anz_htp, arr, htp_arr, htparam, paramtext


        nonlocal s_list, htp_list, htgrp, htp
        nonlocal s_list_list, htp_list_list, htgrp_list, htp_list

        passwd_ok:bool = True
        do_it:bool = False
        htp_list.clear()

        for htparam in db_session.query(Htparam).filter(
                     (Htparam.paramgruppe == i)).order_by(Htparam.paramnr).all():
            do_it = True

            if rest_flag:

                s_list = query(s_list_list, filters=(lambda s_list: s_list.nr == htparam.paramnr), first=True)

                if s_list:
                    do_it = False

            if do_it:
                htp = Htp()
                htp_list.append(htp)

                htp.reihenfolge = htparam.reihenfolge
                htp.number = htparam.paramnr
                htp.bezeich = htparam.bezeichnung
                htp.lupdate = htparam.lupdate
                htp.note = htparam.fdefault

                if htparam.feldtyp == 1:
                    htp.wert = to_string(htparam.finteger)

                elif htparam.feldtyp == 2:
                    htp.wert = to_string(htparam.fdecimal)

                elif htparam.feldtyp == 3:
                    htp.wert = to_string(htparam.fdate)

                elif htparam.feldtyp == 4:
                    htp.wert = to_string(htparam.flogical)
                    htp.logv = htparam.flogical

                elif htparam.feldtyp == 5:
                    htp.wert = to_string(htparam.fchar)
                htp.typ = htparam.feldtyp

    htparam = get_cache (Htparam, {"paramnr": [(eq, 996)]})

    if not htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1015)]})

        if not htparam.flogical:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 990)]})

            if htparam.flogical:
                rest_flag = True
                arr[8] = 0
                arr[13] = 0
                arr[15] = 0
                arr[17] = 0
                arr[18] = 0
                arr[19] = 0
                for i in range(1,anz_htp + 1) :

                    if htp_arr[i - 1] != 0:
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.nr = htp_arr[i - 1]

    htparam = get_cache (Htparam, {"paramnr": [(eq, 981)]})

    if not htparam.flogical:
        arr[18] = 0
    create_htgrp()

    htgrp = query(htgrp_list, first=True)

    if htgrp and htgrp.number != 10 and htgrp.number != 99 and htgrp.number != 100:
        create_htp(htgrp.number)
    create_htplist()

    return generate_output()